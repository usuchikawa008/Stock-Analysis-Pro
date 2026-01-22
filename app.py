import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from stock_analyzer import StockAnalyzer
import config

# Cấu hình trang
st.set_page_config(
    page_title="Stock Analysis Pro",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS tùy chỉnh
st.markdown("""
<style>
    .big-font {
        font-size:20px !important;
        font-weight: bold;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .buy-signal {
        background-color: #d4edda;
        color: #155724;
        padding: 10px;
        border-radius: 5px;
        font-weight: bold;
    }
    .sell-signal {
        background-color: #f8d7da;
        color: #721c24;
        padding: 10px;
        border-radius: 5px;
        font-weight: bold;
    }
    .hold-signal {
        background-color: #fff3cd;
        color: #856404;
        padding: 10px;
        border-radius: 5px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

def create_candlestick_chart(df, symbol, signals):
    """Tạo biểu đồ nến với chỉ báo kỹ thuật"""
    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        subplot_titles=(f'{symbol} - Price & Indicators', 'MACD', 'RSI'),
        row_heights=[0.6, 0.2, 0.2]
    )
    
    # Candlestick
    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name='Price'
        ),
        row=1, col=1
    )
    
    # Moving Averages
    fig.add_trace(
        go.Scatter(x=df.index, y=df['SMA_20'], name='SMA 20',
                  line=dict(color='orange', width=1)),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=df.index, y=df['SMA_50'], name='SMA 50',
                  line=dict(color='blue', width=1)),
        row=1, col=1
    )
    
    # Bollinger Bands
    fig.add_trace(
        go.Scatter(x=df.index, y=df['BB_High'], name='BB High',
                  line=dict(color='gray', width=1, dash='dash')),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=df.index, y=df['BB_Low'], name='BB Low',
                  line=dict(color='gray', width=1, dash='dash')),
        row=1, col=1
    )
    
    # MACD
    fig.add_trace(
        go.Scatter(x=df.index, y=df['MACD'], name='MACD',
                  line=dict(color='blue', width=1)),
        row=2, col=1
    )
    fig.add_trace(
        go.Scatter(x=df.index, y=df['MACD_Signal'], name='Signal',
                  line=dict(color='red', width=1)),
        row=2, col=1
    )
    fig.add_trace(
        go.Bar(x=df.index, y=df['MACD_Diff'], name='MACD Histogram'),
        row=2, col=1
    )
    
    # RSI
    fig.add_trace(
        go.Scatter(x=df.index, y=df['RSI'], name='RSI',
                  line=dict(color='purple', width=2)),
        row=3, col=1
    )
    fig.add_hline(y=70, line_dash="dash", line_color="red", row=3, col=1)
    fig.add_hline(y=30, line_dash="dash", line_color="green", row=3, col=1)
    
    # Layout
    fig.update_layout(
        height=800,
        showlegend=True,
        xaxis_rangeslider_visible=False,
        hovermode='x unified'
    )
    
    fig.update_xaxes(title_text="Date", row=3, col=1)
    fig.update_yaxes(title_text="Price", row=1, col=1)
    fig.update_yaxes(title_text="MACD", row=2, col=1)
    fig.update_yaxes(title_text="RSI", row=3, col=1)
    
    return fig

def display_stock_details(stock_data):
    """Hiển thị chi tiết cổ phiếu với gợi ý mua/bán"""
    symbol = stock_data['symbol']
    signals = stock_data['signals']
    df = stock_data['data']
    
    st.header(f"📊 Chi tiết: {symbol}")
    
    # Thông tin tổng quan
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Giá hiện tại", f"${signals['current_price']:.2f}")
    with col2:
        st.metric("RSI", f"{signals['rsi']:.2f}")
    with col3:
        st.metric("MACD", f"{signals['macd']:.4f}")
    with col4:
        st.metric("Điểm đánh giá", f"{stock_data['score']}/100")
    
    # Khuyến nghị
    st.subheader("🎯 Khuyến nghị giao dịch")
    
    action = signals['action']
    if action in ['BUY', 'ACCUMULATE']:
        st.markdown(f"<div class='buy-signal'>✅ {signals['recommendation']}</div>",
                   unsafe_allow_html=True)
    elif action in ['SELL', 'CONSIDER_SELL']:
        st.markdown(f"<div class='sell-signal'>⚠️ {signals['recommendation']}</div>",
                   unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='hold-signal'>⏸️ {signals['recommendation']}</div>",
                   unsafe_allow_html=True)
    
    st.write("")
    
    # Điểm mua/bán chi tiết
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💰 Điểm mua (Buy Zone)")
        if 'buy_zone' in signals:
            st.write(f"**Vùng mua tốt:** ${signals['buy_zone'][0]:.2f} - ${signals['buy_zone'][1]:.2f}")
            st.write(f"**Stop Loss:** ${signals['stop_loss']:.2f} (-5%)")
        elif 'accumulation_zone' in signals:
            st.write(f"**Vùng tích lũy:** ${signals['accumulation_zone'][0]:.2f} - ${signals['accumulation_zone'][1]:.2f}")
            st.write(f"**Hỗ trợ mạnh:** ${signals['support_level']:.2f}")
    
    with col2:
        st.subheader("💎 Điểm bán (Sell Zone)")
        if 'sell_zone' in signals:
            st.write(f"**Vùng bán:** ${signals['sell_zone'][0]:.2f} - ${signals['sell_zone'][1]:.2f}")
            st.write(f"**Take Profit:** ${signals['take_profit']:.2f} (+8%)")
        elif 'target_price' in signals:
            st.write(f"**Mục tiêu giá:** ${signals['target_price']:.2f} (+30%)")
            st.write(f"**Chiến lược:** Nắm giữ dài hạn, chốt lời từng phần")
    
    # Biểu đồ
    st.subheader("📈 Biểu đồ kỹ thuật")
    chart = create_candlestick_chart(df.tail(100), symbol, signals)
    st.plotly_chart(chart, use_container_width=True)
    
    # Phân tích chi tiết
    with st.expander("📋 Phân tích chi tiết"):
        latest = df.iloc[-1]
        st.write("### Chỉ báo kỹ thuật:")
        st.write(f"- **RSI (14):** {latest['RSI']:.2f} - {'Quá mua' if latest['RSI'] > 70 else 'Quá bán' if latest['RSI'] < 30 else 'Trung lập'}")
        st.write(f"- **MACD:** {latest['MACD']:.4f}")
        st.write(f"- **MACD Signal:** {latest['MACD_Signal']:.4f}")
        st.write(f"- **SMA 20:** ${latest['SMA_20']:.2f}")
        st.write(f"- **SMA 50:** ${latest['SMA_50']:.2f}")
        st.write(f"- **Bollinger Bands:** ${latest['BB_Low']:.2f} - ${latest['BB_High']:.2f}")
        
        st.write("### Xu hướng:")
        if latest['Close'] > latest['SMA_20'] > latest['SMA_50']:
            st.write("✅ Xu hướng tăng mạnh (Giá > SMA20 > SMA50)")
        elif latest['Close'] > latest['SMA_20']:
            st.write("⚠️ Xu hướng tăng ngắn hạn")
        else:
            st.write("⛔ Xu hướng giảm hoặc sideway")

def analyze_single_stock_ui(symbol, strategy):
    """Phân tích 1 cổ phiếu theo mã"""
    analyzer = StockAnalyzer(market='VN')
    
    with st.spinner(f"🔍 Đang phân tích {symbol}..."):
        df = analyzer.get_stock_data(symbol, period_days=150)
        if df is None or len(df) < 50:
            st.error(f"❌ Không thể lấy dữ liệu cho {symbol}. Vui lòng kiểm tra mã cổ phiếu.")
            return None
        
        df = analyzer.calculate_technical_indicators(df)
        if df is None:
            st.error(f"❌ Lỗi tính toán chỉ báo kỹ thuật")
            return None
        
        if strategy == 'swing':
            score = analyzer.calculate_swing_score(df)
        else:
            score = analyzer.calculate_longterm_score(df)
        
        signals = analyzer.get_buy_sell_signals(symbol, df, strategy)
        
        return {
            'symbol': symbol,
            'score': score,
            'data': df,
            'signals': signals
        }

def get_buy_sell_lists(analyzer, strategy, top_n=5):
    """Lấy danh sách top mua và bán"""
    results = analyzer.analyze_all_stocks(strategy=strategy, top_n=len(analyzer.stocks))
    
    buy_stocks = []
    sell_stocks = []
    
    for stock in results:
        action = stock['signals']['action']
        if action in ['BUY', 'ACCUMULATE']:
            buy_stocks.append(stock)
        elif action in ['SELL', 'CONSIDER_SELL']:
            sell_stocks.append(stock)
    
    return buy_stocks[:top_n], sell_stocks[:top_n]

def main():
    st.title("📈 Stock Analysis Pro - Việt Nam")
    st.markdown("### Phân tích cổ phiếu thị trường Việt Nam thông minh")
    
    # Tabs chính
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Top Tổng Hợp", "🔍 Phân Tích Theo Mã", "✅ Top NÊN MUA", "⚠️ Top NÊN BÁN"])
    
    # Sidebar
    st.sidebar.title("⚙️ Cấu hình")
    
    # Mặc định thị trường Việt Nam
    market = 'VN'
    st.sidebar.success("🇻🇳 Thị trường: **Việt Nam**")
    
    # Chọn chiến lược
    strategy = st.sidebar.radio(
        "Chọn chiến lược đầu tư",
        options=['swing', 'longterm'],
        format_func=lambda x: '🌊 Lướt sóng (Swing Trading)' if x == 'swing' else '📊 Đầu tư dài hạn (Long-term)'
    )
    
    # Số lượng cổ phiếu
    top_n = st.sidebar.slider(
        "Số lượng cổ phiếu hiển thị",
        min_value=3,
        max_value=10,
        value=config.TOP_N
    )
    
    # Nút phân tích
    analyze_button = st.sidebar.button("🚀 Bắt đầu phân tích", type="primary")
    
    # Thông tin
    st.sidebar.markdown("---")
    st.sidebar.info(
        f"""
        **Hướng dẫn sử dụng:**
        1. Chọn chiến lược đầu tư
        2. Chọn số lượng cổ phiếu
        3. Nhấn "Bắt đầu phân tích"
        4. Click vào cổ phiếu để xem chi tiết
        5. Xem gợi ý mua/bán
        
        📊 **Hơn {len(config.VN_STOCKS)} cổ phiếu VN**
        🚀 **Phân tích chỉ 1 lần - Nhanh hơn!**
        """
    )
    
    # Khởi tạo session state
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None
    if 'selected_stock' not in st.session_state:
        st.session_state.selected_stock = None
    if 'buy_list' not in st.session_state:
        st.session_state.buy_list = None
    if 'sell_list' not in st.session_state:
        st.session_state.sell_list = None
    if 'selected_buy_stock' not in st.session_state:
        st.session_state.selected_buy_stock = None
    if 'selected_sell_stock' not in st.session_state:
        st.session_state.selected_sell_stock = None
    
    # Phân tích
    if analyze_button:
        st.session_state.selected_stock = None
        
        with st.spinner(f"🔍 Đang phân tích {len(config.VN_STOCKS)} cổ phiếu thị trường..."):
            analyzer = StockAnalyzer(market=market)
            
            # CHỈ PHÂN TÍCH 1 LẦN - lấy tất cả cổ phiếu
            all_results = analyzer.analyze_all_stocks(strategy=strategy, top_n=len(analyzer.stocks))
            
            # Tách ra các danh sách khác nhau
            # Top tổng hợp
            st.session_state.analysis_results = all_results[:top_n]
            
            # Top mua và bán
            buy_list = []
            sell_list = []
            
            for stock in all_results:
                action = stock['signals']['action']
                if action in ['BUY', 'ACCUMULATE']:
                    buy_list.append(stock)
                elif action in ['SELL', 'CONSIDER_SELL']:
                    sell_list.append(stock)
            
            st.session_state.buy_list = buy_list[:top_n]
            st.session_state.sell_list = sell_list[:top_n]
            st.session_state.all_results = all_results  # Lưu toàn bộ để tái sử dụng
        
        st.success(f"✅ Phân tích hoàn tất {len(all_results)} cổ phiếu!")
    
    # TAB 1: Top Tổng Hợp
    with tab1:
        if st.session_state.analysis_results:
            results = st.session_state.analysis_results
            
            if not st.session_state.selected_stock:
                st.header(f"🏆 Top {len(results)} cổ phiếu {'lướt sóng' if strategy == 'swing' else 'đầu tư dài hạn'}")
            
            # Bảng kết quả
            cols = st.columns(len(results))
            
            for idx, (col, stock) in enumerate(zip(cols, results)):
                with col:
                    symbol = stock['symbol']
                    score = stock['score']
                    signals = stock['signals']
                    
                    # Card
                    st.markdown(f"<div class='metric-card'>", unsafe_allow_html=True)
                    st.markdown(f"### #{idx+1} {symbol}")
                    st.metric("Điểm", f"{score}/100")
                    st.metric("Giá", f"${signals['current_price']:.2f}")
                    
                    # Nút xem chi tiết
                    if st.button(f"📊 Chi tiết", key=f"btn_{symbol}"):
                        st.session_state.selected_stock = stock
                        st.rerun()
                    
                    st.markdown("</div>", unsafe_allow_html=True)
            
                # Bảng so sánh
                st.subheader("📊 Bảng so sánh")
                comparison_data = []
                for stock in results:
                    comparison_data.append({
                        'Mã CP': stock['symbol'],
                        'Điểm': stock['score'],
                        'Giá': f"${stock['signals']['current_price']:.2f}",
                        'RSI': f"{stock['signals']['rsi']:.2f}",
                        'Khuyến nghị': stock['signals']['action']
                    })
                
                df_comparison = pd.DataFrame(comparison_data)
                st.dataframe(df_comparison, width='stretch')
            
            else:
                # Hiển thị chi tiết cổ phiếu
                if st.button("⬅️ Quay lại danh sách", key="back_tab1"):
                    st.session_state.selected_stock = None
                    st.rerun()
                
                if st.session_state.selected_stock:
                    display_stock_details(st.session_state.selected_stock)
                else:
                    st.error("❌ Không có dữ liệu cổ phiếu")
        else:
            st.info("👈 Nhấn 'Bắt đầu phân tích' ở sidebar để xem kết quả")
    
    # TAB 2: Phân tích theo mã
    with tab2:
        st.header("🔍 Phân tích Cổ Phiếu Theo Mã")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            symbol_input = st.text_input(
                "Nhập mã cổ phiếu (VD: HPG, VCB, FPT)",
                placeholder="Nhập mã...",
                key="symbol_input"
            ).upper()
        with col2:
            st.write("")
            st.write("")
            analyze_single = st.button("🔍 Phân Tích", type="primary", key="analyze_single")
        
        if analyze_single and symbol_input:
            result = analyze_single_stock_ui(symbol_input, strategy)
            if result:
                st.success(f"✅ Phân tích {symbol_input} hoàn tất!")
                display_stock_details(result)
        elif analyze_single and not symbol_input:
            st.warning("⚠️ Vui lòng nhập mã cổ phiếu")
        else:
            st.info("""
            💡 **Hướng dẫn:**
            1. Nhập mã cổ phiếu VN (không cần .VN)
            2. Chọn chiến lược ở sidebar
            3. Nhấn 'Phân Tích'
            
            **Một số mã phổ biến:** VNM, HPG, VCB, FPT, TCB, VIC, MSN, MWG, GAS, VHM
            """)
    
    # TAB 3: Top NÊN MUA
    with tab3:
        if 'buy_list' in st.session_state and st.session_state.buy_list:
            buy_list = st.session_state.buy_list
            
            st.header(f"✅ Top {len(buy_list)} Cổ Phiếu NÊN MUA")
            st.markdown(f"**Chiến lược:** {'🌊 Lướt sóng' if strategy == 'swing' else '📊 Dài hạn'}")
            
            # Hiển thị cards
            cols = st.columns(min(len(buy_list), 3))
            for idx, stock in enumerate(buy_list[:len(cols)]):
                with cols[idx]:
                    signals = stock['signals']
                    st.markdown(f"<div class='metric-card'>", unsafe_allow_html=True)
                    st.markdown(f"### #{idx+1} {stock['symbol']}")
                    st.metric("Điểm", f"{stock['score']}/100")
                    st.metric("Giá", f"${signals['current_price']:.2f}")
                    st.markdown(f"<div class='buy-signal'>✅ {signals['action']}</div>", unsafe_allow_html=True)
                    
                    if st.button(f"📊 Chi tiết", key=f"buy_detail_{idx}_{stock['symbol']}"):
                        st.session_state.selected_buy_stock = stock
                    
                    st.markdown("</div>", unsafe_allow_html=True)
            
            # Hiển thị chi tiết nếu đã chọn
            if 'selected_buy_stock' in st.session_state and st.session_state.selected_buy_stock:
                st.markdown("---")
                if st.button("⬅️ Ẩn chi tiết", key="hide_buy_detail"):
                    st.session_state.selected_buy_stock = None
                    st.rerun()
                display_stock_details(st.session_state.selected_buy_stock)
            
            # Bảng chi tiết
            st.subheader("📊 Bảng chi tiết")
            buy_data = []
            for stock in buy_list:
                signals = stock['signals']
                buy_data.append({
                    'Mã CP': stock['symbol'],
                    'Điểm': stock['score'],
                    'Giá': f"${signals['current_price']:.2f}",
                    'RSI': f"{signals['rsi']:.2f}",
                    'Lý do': signals['recommendation']
                })
            st.dataframe(pd.DataFrame(buy_data), width='stretch')
        else:
            st.info("👈 Nhấn 'Bắt đầu phân tích' ở sidebar để xem danh sách cổ phiếu nên mua")
    
    # TAB 4: Top NÊN BÁN
    with tab4:
        if 'sell_list' in st.session_state and st.session_state.sell_list:
            sell_list = st.session_state.sell_list
            
            st.header(f"⚠️ Top {len(sell_list)} Cổ Phiếu NÊN BÁN/TRÁNH")
            st.markdown(f"**Chiến lược:** {'🌊 Lướt sóng' if strategy == 'swing' else '📊 Dài hạn'}")
            
            # Hiển thị cards
            cols = st.columns(min(len(sell_list), 3))
            for idx, stock in enumerate(sell_list[:len(cols)]):
                with cols[idx]:
                    signals = stock['signals']
                    st.markdown(f"<div class='metric-card'>", unsafe_allow_html=True)
                    st.markdown(f"### #{idx+1} {stock['symbol']}")
                    st.metric("Điểm", f"{stock['score']}/100")
                    st.metric("Giá", f"${signals['current_price']:.2f}")
                    st.markdown(f"<div class='sell-signal'>⚠️ {signals['action']}</div>", unsafe_allow_html=True)
                    
                    if st.button(f"📊 Chi tiết", key=f"sell_detail_{idx}_{stock['symbol']}"):
                        st.session_state.selected_sell_stock = stock
                    
                    st.markdown("</div>", unsafe_allow_html=True)
            
            # Hiển thị chi tiết nếu đã chọn
            if 'selected_sell_stock' in st.session_state and st.session_state.selected_sell_stock:
                st.markdown("---")
                if st.button("⬅️ Ẩn chi tiết", key="hide_sell_detail"):
                    st.session_state.selected_sell_stock = None
                    st.rerun()
                display_stock_details(st.session_state.selected_sell_stock)
            
            # Bảng chi tiết
            st.subheader("📊 Bảng chi tiết")
            sell_data = []
            for stock in sell_list:
                signals = stock['signals']
                sell_data.append({
                    'Mã CP': stock['symbol'],
                    'Điểm': stock['score'],
                    'Giá': f"${signals['current_price']:.2f}",
                    'RSI': f"{signals['rsi']:.2f}",
                    'Lý do': signals['recommendation']
                })
            st.dataframe(pd.DataFrame(sell_data), width='stretch')
        else:
            st.info("👈 Nhấn 'Bắt đầu phân tích' ở sidebar để xem danh sách cổ phiếu nên bán")
    
    # Footer chung
    if not (st.session_state.analysis_results or 'buy_list' in st.session_state):
        # Màn hình chào mừng
        st.info("👈 Vui lòng cấu hình và nhấn **'Bắt đầu phân tích'** ở sidebar")
        
        st.markdown("""
        ### 🇻🇳 Phân tích chuyên sâu thị trường Việt Nam
        
        Ứng dụng phân tích hơn **50 cổ phiếu** tốt nhất trên HOSE & HNX
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            ### 🌊 Lướt sóng (Swing Trading)
            - ⏱️ Thời gian: 2-3 tuần
            - 📊 Tìm cổ phiếu biến động tốt
            - 🎯 RSI, MACD signals
            - 💰 Stop loss & Take profit rõ ràng
            - 🚀 Phù hợp trader ngắn hạn
            """)
        
        with col2:
            st.markdown("""
            ### 📊 Đầu tư dài hạn
            - ⏱️ Thời gian: 6-12 tháng+
            - 📈 Xu hướng tăng ổn định
            - 💎 Thanh khoản tốt
            - 🎯 Mục tiêu giá cao
            - 🏆 Phù hợp nhà đầu tư giá trị
            """)

if __name__ == "__main__":
    main()
