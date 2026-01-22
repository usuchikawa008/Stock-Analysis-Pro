"""
Console version - Không cần UI, chạy trực tiếp
"""
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from ta.momentum import RSIIndicator
from ta.trend import MACD, SMAIndicator
from ta.volatility import BollingerBands

# Danh sách cổ phiếu VN
VN_STOCKS = [
    'VNM', 'VIC', 'HPG', 'VHM', 'TCB', 'VCB', 'BID', 'CTG', 'MWG', 'FPT',
    'MSN', 'VPB', 'GAS', 'PLX', 'VRE', 'MBB', 'SSI', 'HDB', 'STB', 'POW',
    'ACB', 'TPB', 'VJC', 'SAB', 'REE', 'PNJ', 'KDH', 'GVR', 'BCM', 'VPI',
    'DGC', 'DXG', 'NVL', 'PDR', 'VCI', 'HCM', 'GMD', 'DIG', 'TCH', 'PC1',
    'VHC', 'DCM', 'DHG', 'NT2', 'SBT', 'PHR', 'LGC', 'DPM', 'HSG', 'TNG'
]

def get_stock_data(symbol, days=100):
    """Lấy dữ liệu cổ phiếu"""
    try:
        ticker = f"{symbol}.VN"
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        stock = yf.Ticker(ticker)
        df = stock.history(start=start_date, end=end_date)
        
        if df.empty:
            return None
        return df
    except:
        return None

def calculate_indicators(df):
    """Tính các chỉ báo kỹ thuật"""
    if df is None or len(df) < 20:
        return None
    
    # RSI
    rsi = RSIIndicator(close=df['Close'], window=14)
    df['RSI'] = rsi.rsi()
    
    # MACD
    macd = MACD(close=df['Close'])
    df['MACD'] = macd.macd()
    df['MACD_Signal'] = macd.macd_signal()
    
    # SMA
    df['SMA_20'] = SMAIndicator(close=df['Close'], window=20).sma_indicator()
    df['SMA_50'] = SMAIndicator(close=df['Close'], window=50).sma_indicator()
    
    # Bollinger Bands
    bollinger = BollingerBands(close=df['Close'])
    df['BB_High'] = bollinger.bollinger_hband()
    df['BB_Low'] = bollinger.bollinger_lband()
    
    return df

def calculate_score(df, strategy='swing'):
    """Tính điểm"""
    if df is None or len(df) < 50:
        return 0
    
    score = 0
    latest = df.iloc[-1]
    
    if strategy == 'swing':
        # Volatility
        returns = df['Close'].pct_change()
        volatility = returns.std() * 100
        if 2 < volatility < 5:
            score += 25
        elif volatility >= 1.5:
            score += 15
        
        # RSI
        rsi = latest['RSI']
        if 35 <= rsi <= 65:
            score += 20
        elif 30 <= rsi < 35:
            score += 15
        
        # MACD
        if latest['MACD'] > latest['MACD_Signal']:
            score += 20
        
        # Trend
        if latest['Close'] > latest['SMA_20'] > latest['SMA_50']:
            score += 20
        elif latest['Close'] > latest['SMA_20']:
            score += 10
        
    else:  # longterm
        # Long-term trend
        if 'SMA_50' in df.columns and pd.notna(latest['SMA_50']):
            if latest['Close'] > latest['SMA_50']:
                score += 30
        
        # Stability
        returns = df['Close'].pct_change()
        volatility = returns.std() * 100
        if volatility < 2:
            score += 25
        elif volatility < 3:
            score += 15
        
        # Recent performance
        recent_30 = df.tail(30)
        uptrend_days = sum(recent_30['Close'] > recent_30['Close'].shift(1))
        if uptrend_days > 18:
            score += 20
        elif uptrend_days > 15:
            score += 15
    
    return score

def get_signals(df, strategy='swing'):
    """Gợi ý mua/bán"""
    if df is None:
        return None
    
    latest = df.iloc[-1]
    signals = {
        'price': latest['Close'],
        'rsi': latest['RSI']
    }
    
    if strategy == 'swing':
        signals['buy_zone'] = f"{latest['BB_Low']:.0f} - {latest['SMA_20']*0.98:.0f}"
        signals['sell_zone'] = f"{latest['BB_High']:.0f} - {latest['SMA_20']*1.03:.0f}"
        signals['stop_loss'] = f"{latest['Close']*0.95:.0f}"
        signals['take_profit'] = f"{latest['Close']*1.08:.0f}"
        
        if latest['RSI'] < 35 and latest['Close'] < latest['BB_Low']:
            signals['action'] = 'MUA MẠNH'
        elif latest['RSI'] < 45 and latest['MACD'] > latest['MACD_Signal']:
            signals['action'] = 'MUA'
        elif latest['RSI'] > 70:
            signals['action'] = 'BÁN'
        else:
            signals['action'] = 'GIỮ'
    else:
        signals['target'] = f"{latest['Close']*1.3:.0f}"
        if latest['Close'] > latest['SMA_50'] and 50 < latest['RSI'] < 70:
            signals['action'] = 'MUA - Xu hướng tốt'
        elif latest['RSI'] < 40:
            signals['action'] = 'TÍCH LŨY'
        else:
            signals['action'] = 'GIỮ'
    
    return signals

def analyze_stocks(strategy='swing', top_n=5):
    """Phân tích và trả về top cổ phiếu"""
    print(f"\n{'='*60}")
    print(f"  PHÂN TÍCH CỔ PHIẾU VIỆT NAM")
    print(f"  Chiến lược: {'Lướt sóng' if strategy=='swing' else 'Dài hạn'}")    print(f"  Tổng số: {len(VN_STOCKS)} cổ phiếu")    print(f"{'='*60}\n")
    
    results = []
    total = len(VN_STOCKS)
    
    for i, symbol in enumerate(VN_STOCKS):
        print(f"[{i+1}/{total}] Đang phân tích {symbol}...", end='\r')
        
        df = get_stock_data(symbol, days=150)
        if df is None or len(df) < 50:
            continue
        
        df = calculate_indicators(df)
        if df is None:
            continue
        
        score = calculate_score(df, strategy)
        signals = get_signals(df, strategy)
        
        if signals:
            results.append({
                'symbol': symbol,
                'score': score,
                'signals': signals
            })
    
    print(f"\n{'='*60}")
    results.sort(key=lambda x: x['score'], reverse=True)
    return results[:top_n]

def print_results(results, strategy='swing'):
    """In kết quả"""
    print(f"\n{'='*60}")
    print(f"  TOP {len(results)} CỔ PHIẾU {'LƯỚT SÓNG' if strategy=='swing' else 'ĐẦU TƯ DÀI HẠN'}")
    print(f"{'='*60}\n")
    
    for i, stock in enumerate(results):
        symbol = stock['symbol']
        score = stock['score']
        signals = stock['signals']
        
        print(f"\n#{i+1}. {symbol} - Điểm: {score}/100")
        print(f"  Giá hiện tại: {signals['price']:.0f} VNĐ")
        print(f"  RSI: {signals['rsi']:.1f}")
        print(f"  Khuyến nghị: {signals['action']}")
        
        if strategy == 'swing':
            print(f"  Vùng mua: {signals['buy_zone']} VNĐ")
            print(f"  Vùng bán: {signals['sell_zone']} VNĐ")
            print(f"  Stop Loss: {signals['stop_loss']} VNĐ")
            print(f"  Take Profit: {signals['take_profit']} VNĐ")
        else:
            print(f"  Mục tiêu: {signals['target']} VNĐ")

def print_detail(stock, strategy='swing'):
    """In chi tiết 1 cổ phiếu"""
    symbol = stock['symbol']
    signals = stock['signals']
    
    print(f"\n{'='*60}")
    print(f"  CHI TIẾT: {symbol}")
    print(f"{'='*60}")
    print(f"\nGiá hiện tại: {signals['price']:.0f} VNĐ")
    print(f"RSI: {signals['rsi']:.1f}")
    print(f"Điểm: {stock['score']}/100")
    print(f"\nKHUYẾN NGHỊ: {signals['action']}")
    
    if strategy == 'swing':
        print(f"\n💰 ĐIỂM MUA:")
        print(f"  Vùng mua tốt: {signals['buy_zone']} VNĐ")
        print(f"  Stop Loss: {signals['stop_loss']} VNĐ (-5%)")
        print(f"\n💎 ĐIỂM BÁN:")
        print(f"  Vùng bán: {signals['sell_zone']} VNĐ")
        print(f"  Take Profit: {signals['take_profit']} VNĐ (+8%)")
    else:
        print(f"\n📊 MỤC TIÊU DÀI HẠN:")
        print(f"  Target: {signals['target']} VNĐ (+30%)")
    
    print(f"\n{'='*60}\n")

def analyze_single_stock(symbol, strategy='swing'):
    """Phân tích 1 cổ phiếu cụ thể"""
    print(f"\n{'='*60}")
    print(f"  PHÂN TÍCH: {symbol}")
    print(f"  Chiến lược: {'Lướt sóng' if strategy=='swing' else 'Dài hạn'}")
    print(f"{'='*60}\n")
    
    print("Đang tải dữ liệu...")
    df = get_stock_data(symbol, days=150)
    if df is None or len(df) < 50:
        print(f"❌ Không thể lấy dữ liệu cho {symbol}")
        return
    
    df = calculate_indicators(df)
    if df is None:
        print(f"❌ Lỗi tính toán chỉ báo cho {symbol}")
        return
    
    score = calculate_score(df, strategy)
    signals = get_signals(df, strategy)
    
    stock = {
        'symbol': symbol,
        'score': score,
        'signals': signals
    }
    
    print_detail(stock, strategy)

def get_buy_sell_recommendations(strategy='swing', top_n=5):
    """Lấy top cổ phiếu nên mua và nên bán"""
    print(f"\n{'='*60}")
    print(f"  PHÂN TÍCH TOÀN BỘ THỊ TRƯỜNG")
    print(f"  Chiến lược: {'Lướt sóng' if strategy=='swing' else 'Dài hạn'}")
    print(f"{'='*60}\n")
    
    buy_stocks = []
    sell_stocks = []
    total = len(VN_STOCKS)
    
    for i, symbol in enumerate(VN_STOCKS):
        print(f"[{i+1}/{total}] Đang phân tích {symbol}...", end='\r')
        
        df = get_stock_data(symbol, days=150)
        if df is None or len(df) < 50:
            continue
        
        df = calculate_indicators(df)
        if df is None:
            continue
        
        score = calculate_score(df, strategy)
        signals = get_signals(df, strategy)
        
        if signals:
            stock_data = {
                'symbol': symbol,
                'score': score,
                'signals': signals
            }
            
            action = signals['action']
            if 'MUA' in action or action == 'TÍCH LŨY':
                buy_stocks.append(stock_data)
            elif 'BÁN' in action:
                sell_stocks.append(stock_data)
    
    print(f"\n{'='*60}")
    
    # Sắp xếp
    buy_stocks.sort(key=lambda x: x['score'], reverse=True)
    sell_stocks.sort(key=lambda x: x['score'], reverse=False)  # Điểm thấp = nên bán
    
    return buy_stocks[:top_n], sell_stocks[:top_n]

def main():
    """Main function"""
    while True:
        print("\n" + "="*60)
        print("  📈 STOCK ANALYSIS PRO - VIỆT NAM")
        print("="*60)
        
        print("\nChọn chức năng:")
        print("1. Phân tích Top cổ phiếu tổng hợp")
        print("2. Phân tích cổ phiếu theo mã (nhập mã)")
        print("3. Top cổ phiếu NÊN MUA")
        print("4. Top cổ phiếu NÊN BÁN")
        print("5. Thoát")
        
        mode = input("\nNhập lựa chọn (1-5): ").strip()
        
        if mode == '5':
            print("\nCảm ơn bạn đã sử dụng! 🚀\n")
            break
        
        if mode == '2':
            # Phân tích theo mã
            symbol = input("\nNhập mã cổ phiếu (VD: HPG, VCB, FPT): ").strip().upper()
            if not symbol:
                print("Mã không hợp lệ!")
                continue
            
            print("\nChọn chiến lược:")
            print("1. Lướt sóng (2-3 tuần)")
            print("2. Dài hạn (6-12 tháng)")
            choice = input("Nhập lựa chọn (1/2): ").strip()
            strategy = 'swing' if choice == '1' else 'longterm'
            
            analyze_single_stock(symbol, strategy)
            input("\nNhấn Enter để tiếp tục...")
            continue
        
        # Chọn chiến lược cho các chức năng khác
        print("\nChọn chiến lược:")
        print("1. Lướt sóng (Swing Trading - 2-3 tuần)")
        print("2. Đầu tư dài hạn (Long-term - 6-12 tháng)")
        
        choice = input("\nNhập lựa chọn (1/2): ").strip()
        strategy = 'swing' if choice == '1' else 'longterm'
    
        # Số lượng cổ phiếu
        try:
            top_n = int(input("Số lượng cổ phiếu (3-10): ").strip())
            top_n = max(3, min(10, top_n))
        except:
            top_n = 5
        
        if mode == '1':
            # Phân tích tổng hợp
            print("\nĐang phân tích...")
            results = analyze_stocks(strategy, top_n)
            print_results(results, strategy)
            
            # Xem chi tiết
            while True:
                print(f"\n{'='*60}")
                choice = input("Xem chi tiết cổ phiếu số (1-{}) hoặc 'q' để quay lại: ".format(len(results))).strip().lower()
                
                if choice == 'q':
                    break
                
                try:
                    idx = int(choice) - 1
                    if 0 <= idx < len(results):
                        print_detail(results[idx], strategy)
                    else:
                        print("Số không hợp lệ!")
                except:
                    print("Vui lòng nhập số hợp lệ!")
        
        elif mode == '3':
            # Top NÊN MUA
            print("\nĐang phân tích thị trường...")
            buy_stocks, _ = get_buy_sell_recommendations(strategy, top_n)
            
            print(f"\n{'='*60}")
            print(f"  TOP {len(buy_stocks)} CỔ PHIẾU NÊN MUA")
            print(f"  Chiến lược: {'Lướt sóng' if strategy=='swing' else 'Dài hạn'}")
            print(f"{'='*60}\n")
            
            for i, stock in enumerate(buy_stocks):
                signals = stock['signals']
                print(f"\n#{i+1}. {stock['symbol']} - Điểm: {stock['score']}/100")
                print(f"  Giá: {signals['price']:.0f} VNĐ")
                print(f"  RSI: {signals['rsi']:.1f}")
                print(f"  ✅ Khuyến nghị: {signals['action']}")
                if strategy == 'swing':
                    print(f"  💰 Vùng mua: {signals['buy_zone']}")
                    print(f"  🛡️ Stop Loss: {signals['stop_loss']} VNĐ")
            
            input("\n\nNhấn Enter để tiếp tục...")
        
        elif mode == '4':
            # Top NÊN BÁN
            print("\nĐang phân tích thị trường...")
            _, sell_stocks = get_buy_sell_recommendations(strategy, top_n)
            
            print(f"\n{'='*60}")
            print(f"  TOP {len(sell_stocks)} CỔ PHIẾU NÊN BÁN/TRÁNH")
            print(f"  Chiến lược: {'Lướt sóng' if strategy=='swing' else 'Dài hạn'}")
            print(f"{'='*60}\n")
            
            for i, stock in enumerate(sell_stocks):
                signals = stock['signals']
                print(f"\n#{i+1}. {stock['symbol']} - Điểm: {stock['score']}/100")
                print(f"  Giá: {signals['price']:.0f} VNĐ")
                print(f"  RSI: {signals['rsi']:.1f}")
                print(f"  ⚠️ Khuyến nghị: {signals['action']}")
                if strategy == 'swing':
                    print(f"  💎 Vùng bán: {signals['sell_zone']}")
            
            input("\n\nNhấn Enter để tiếp tục...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nĐã dừng chương trình. Tạm biệt! 👋\n")
    except Exception as e:
        print(f"\nLỗi: {e}")
        print("Vui lòng kiểm tra kết nối internet và thử lại.\n")
