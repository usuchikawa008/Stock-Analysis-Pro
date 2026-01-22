import yfinance as yf
import pandas as pd
import numpy as np
from ta.momentum import RSIIndicator
from ta.trend import MACD, SMAIndicator, EMAIndicator
from ta.volume import VolumeWeightedAveragePrice
from ta.volatility import BollingerBands
from datetime import datetime, timedelta
import config

class StockAnalyzer:
    def __init__(self, market='VN'):
        """
        market: 'VN' cho thị trường Việt Nam, 'US' cho thị trường Mỹ
        """
        self.market = market
        self.stocks = config.VN_STOCKS if market == 'VN' else config.US_STOCKS
        
    def get_stock_data(self, symbol, period_days=365):
        """Lấy dữ liệu cổ phiếu"""
        try:
            if self.market == 'VN':
                # Thêm .VN cho thị trường Việt Nam trên Yahoo Finance
                ticker = f"{symbol}.VN"
            else:
                ticker = symbol
            
            end_date = datetime.now()
            start_date = end_date - timedelta(days=period_days)
            
            stock = yf.Ticker(ticker)
            df = stock.history(start=start_date, end=end_date)
            
            if df.empty:
                return None
            
            return df
        except Exception as e:
            print(f"Error getting data for {symbol}: {e}")
            return None
    
    def calculate_technical_indicators(self, df):
        """Tính toán các chỉ báo kỹ thuật"""
        if df is None or df.empty:
            return None
        
        # RSI
        rsi = RSIIndicator(close=df['Close'], window=14)
        df['RSI'] = rsi.rsi()
        
        # MACD
        macd = MACD(close=df['Close'])
        df['MACD'] = macd.macd()
        df['MACD_Signal'] = macd.macd_signal()
        df['MACD_Diff'] = macd.macd_diff()
        
        # Moving Averages
        df['SMA_20'] = SMAIndicator(close=df['Close'], window=20).sma_indicator()
        df['SMA_50'] = SMAIndicator(close=df['Close'], window=50).sma_indicator()
        df['SMA_200'] = SMAIndicator(close=df['Close'], window=200).sma_indicator()
        df['EMA_12'] = EMAIndicator(close=df['Close'], window=12).ema_indicator()
        df['EMA_26'] = EMAIndicator(close=df['Close'], window=26).ema_indicator()
        
        # Bollinger Bands
        bollinger = BollingerBands(close=df['Close'])
        df['BB_High'] = bollinger.bollinger_hband()
        df['BB_Low'] = bollinger.bollinger_lband()
        df['BB_Mid'] = bollinger.bollinger_mavg()
        
        # Volume average
        df['Volume_MA_20'] = df['Volume'].rolling(window=20).mean()
        
        return df
    
    def calculate_swing_score(self, df):
        """Tính điểm cho lướt sóng"""
        if df is None or len(df) < 50:
            return 0
        
        score = 0
        latest = df.iloc[-1]
        recent = df.tail(20)
        
        # 1. Volatility Score (0-25 điểm)
        returns = df['Close'].pct_change()
        volatility = returns.std() * 100
        if 2 < volatility < 5:  # Biến động vừa phải
            score += 25
        elif 1.5 < volatility <= 2 or 5 <= volatility < 7:
            score += 15
        elif volatility >= 1:
            score += 5
        
        # 2. RSI Score (0-20 điểm)
        rsi = latest['RSI']
        if config.RSI_OPTIMAL_LOW <= rsi <= config.RSI_OPTIMAL_HIGH:
            score += 20
        elif config.RSI_OVERSOLD <= rsi < config.RSI_OPTIMAL_LOW:
            score += 15  # Sắp tăng
        elif config.RSI_OPTIMAL_HIGH < rsi <= config.RSI_OVERBOUGHT:
            score += 10
        
        # 3. MACD Score (0-20 điểm)
        if latest['MACD'] > latest['MACD_Signal']:
            score += 10
        if latest['MACD_Diff'] > 0:
            score += 10
        
        # 4. Volume Score (0-15 điểm)
        if latest['Volume'] > latest['Volume_MA_20'] * 1.2:
            score += 15
        elif latest['Volume'] > latest['Volume_MA_20']:
            score += 10
        
        # 5. Short-term Trend Score (0-20 điểm)
        if latest['Close'] > latest['SMA_20'] > latest['SMA_50']:
            score += 20
        elif latest['Close'] > latest['SMA_20']:
            score += 10
        
        return score
    
    def calculate_longterm_score(self, df):
        """Tính điểm cho đầu tư dài hạn"""
        if df is None or len(df) < 200:
            return 0
        
        score = 0
        latest = df.iloc[-1]
        
        # 1. Long-term Trend (0-30 điểm)
        if latest['Close'] > latest['SMA_50'] > latest['SMA_200']:
            score += 30
        elif latest['Close'] > latest['SMA_200']:
            score += 20
        elif latest['SMA_50'] > latest['SMA_200']:
            score += 10
        
        # 2. Stability Score (0-25 điểm)
        returns = df['Close'].pct_change()
        volatility = returns.std() * 100
        if volatility < 2:  # Biến động thấp
            score += 25
        elif volatility < 3:
            score += 15
        elif volatility < 4:
            score += 10
        
        # 3. Fundamentals (0-20 điểm) - Dựa trên price action
        recent_30 = df.tail(30)
        uptrend_days = sum(recent_30['Close'] > recent_30['Close'].shift(1))
        if uptrend_days > 18:  # >60% ngày tăng
            score += 20
        elif uptrend_days > 15:
            score += 15
        elif uptrend_days > 12:
            score += 10
        
        # 4. Volume Quality (0-15 điểm)
        avg_volume = df['Volume'].tail(90).mean()
        if avg_volume > df['Volume'].tail(180).mean():
            score += 15
        elif avg_volume > df['Volume'].tail(365).mean():
            score += 10
        
        # 5. Momentum (0-10 điểm)
        if latest['RSI'] > 50 and latest['RSI'] < 70:
            score += 10
        elif latest['RSI'] > 45:
            score += 5
        
        return score
    
    def get_buy_sell_signals(self, symbol, df, strategy='swing'):
        """Tạo gợi ý điểm mua/bán"""
        if df is None or df.empty:
            return None
        
        latest = df.iloc[-1]
        signals = {
            'current_price': latest['Close'],
            'rsi': latest['RSI'],
            'macd': latest['MACD'],
            'macd_signal': latest['MACD_Signal']
        }
        
        if strategy == 'swing':
            # Lướt sóng
            signals['buy_zone'] = [
                latest['BB_Low'],
                latest['SMA_20'] * 0.98
            ]
            signals['sell_zone'] = [
                latest['BB_High'],
                latest['SMA_20'] * 1.03
            ]
            signals['stop_loss'] = latest['Close'] * 0.95  # Stop loss 5%
            signals['take_profit'] = latest['Close'] * 1.08  # Take profit 8%
            
            # Khuyến nghị
            if latest['RSI'] < 35 and latest['Close'] < latest['BB_Low']:
                signals['recommendation'] = 'MUA MẠNH - RSI oversold & giá dưới BB dưới'
                signals['action'] = 'BUY'
            elif latest['RSI'] < 45 and latest['MACD'] > latest['MACD_Signal']:
                signals['recommendation'] = 'MUA - RSI thấp & MACD tích cực'
                signals['action'] = 'BUY'
            elif latest['RSI'] > 70 or latest['Close'] > latest['BB_High']:
                signals['recommendation'] = 'BÁN - RSI overbought hoặc giá cao'
                signals['action'] = 'SELL'
            else:
                signals['recommendation'] = 'GIỮ - Chờ tín hiệu rõ ràng hơn'
                signals['action'] = 'HOLD'
        else:
            # Đầu tư dài hạn
            signals['support_level'] = latest['SMA_200']
            signals['target_price'] = latest['Close'] * 1.3  # Mục tiêu 30%
            signals['accumulation_zone'] = [
                latest['SMA_50'] * 0.95,
                latest['SMA_50'] * 1.05
            ]
            
            # Khuyến nghị
            if (latest['Close'] > latest['SMA_50'] > latest['SMA_200'] and 
                latest['RSI'] > 50 and latest['RSI'] < 70):
                signals['recommendation'] = 'MUA - Xu hướng tăng mạnh dài hạn'
                signals['action'] = 'BUY'
            elif latest['Close'] < latest['SMA_200'] and latest['RSI'] < 40:
                signals['recommendation'] = 'TÍCH LŨY - Giá tốt cho dài hạn'
                signals['action'] = 'ACCUMULATE'
            elif latest['Close'] > latest['SMA_200'] * 1.5:
                signals['recommendation'] = 'CÂN NHẮC CHỐT LỜI - Giá đã tăng mạnh'
                signals['action'] = 'CONSIDER_SELL'
            else:
                signals['recommendation'] = 'GIỮ - Chờ thời điểm tốt hơn'
                signals['action'] = 'HOLD'
        
        return signals
    
    def analyze_all_stocks(self, strategy='swing', top_n=5):
        """Phân tích tất cả cổ phiếu và trả về top N"""
        results = []
        period = config.SWING_PERIOD if strategy == 'swing' else config.LONGTERM_PERIOD
        
        print(f"Đang phân tích {len(self.stocks)} cổ phiếu cho chiến lược {strategy}...")
        
        for i, symbol in enumerate(self.stocks):
            print(f"Phân tích {symbol}... ({i+1}/{len(self.stocks)})")
            
            df = self.get_stock_data(symbol, period_days=period + 100)
            if df is None or len(df) < 50:
                continue
            
            df = self.calculate_technical_indicators(df)
            
            if strategy == 'swing':
                score = self.calculate_swing_score(df)
            else:
                score = self.calculate_longterm_score(df)
            
            signals = self.get_buy_sell_signals(symbol, df, strategy)
            
            if signals:
                results.append({
                    'symbol': symbol,
                    'score': score,
                    'data': df,
                    'signals': signals
                })
        
        # Sắp xếp theo điểm
        results.sort(key=lambda x: x['score'], reverse=True)
        
        return results[:top_n]
