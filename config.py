# Cấu hình ứng dụng phân tích cổ phiếu

# Danh sách cổ phiếu VN để phân tích (Hơn 100 mã)
VN_STOCKS = [
    # VN30 - 30 cổ phiếu vốn hóa lớn nhất
    'VNM', 'VIC', 'HPG', 'VHM', 'TCB', 'VCB', 'BID', 'CTG', 'MWG', 'FPT',
    'MSN', 'VPB', 'GAS', 'PLX', 'VRE', 'MBB', 'SSI', 'HDB', 'STB', 'POW',
    'ACB', 'TPB', 'VJC', 'SAB', 'GVR', 'BCM', 'VPI', 'VHC', 'NVL', 'KDH',
    
    # Blue-chip và Mid-cap tiềm năng
    'REE', 'PNJ', 'DGC', 'DXG', 'PDR', 'VCI', 'HCM', 'GMD', 'DIG', 'TCH',
    'PC1', 'DCM', 'DHG', 'NT2', 'SBT', 'PHR', 'LGC', 'DPM', 'HSG', 'TNG',
    
    # Ngân hàng
    'SHB', 'EIB', 'VIB', 'LPB', 'OCB', 'MSB', 'BAB', 'NAB', 'PGB', 'BVB',
    
    # Bất động sản
    'NLG', 'HDG', 'CEO', 'HDC', 'ITA', 'LDG', 'NTL', 'PDN', 'QCG',
    'SCR', 'SZC', 'TDC', 'TDH',
    
    # Chứng khoán
    'AGR', 'BSI', 'CTS', 'FTS', 'IVS', 'ORS', 'SHS', 'VDS',
    'VIX', 'VND',
    
    # Công nghệ - Viễn thông
    'CMG', 'DGW', 'ELC', 'ICT', 'SAM', 'SGT', 'VGI', 'VTC', 'ITD', 'FOX',
    
    # Bán lẻ
    'FRT', 'PET', 'SFI', 'VGC',
    
    # Thực phẩm - Đồ uống
    'KDC', 'MCH', 'BAF', 'HNG', 'LAF', 'QNS',
    'TLG', 'VCF',
    
    # Dược phẩm
    'IMP', 'DMC', 'DP1', 'DP2', 'DP3', 'DVN', 'PME', 'TRA',
    
    # Thép - Vật liệu xây dựng
    'BMP', 'HT1', 'NKG', 'POM', 'TLH', 'VCS', 'VGS',
    
    # Năng lượng - Điện
    'PGV', 'SBA', 'VSH',
    
    # Thủy sản
    'AAM', 'ABT', 'ACL', 'AGF', 'ANV', 'CMX', 'FMC', 'IDI', 'MPC', 'TS4',
    
    # Dệt may
    'GIL', 'MSH', 'STK', 'TCM', 'VGT',
    
    # Cao su - Nhựa
    'CSM', 'DPR', 'DRC', 'TRC',
    
    # Hàng không - Du lịch
    'ACV', 'VNG', 'PDC', 'PVT', 'TCT', 'VTO'
]

# Danh sách cổ phiếu quốc tế để phân tích
US_STOCKS = [
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA', 'JPM', 'V', 'WMT',
    'MA', 'PG', 'UNH', 'HD', 'DIS', 'BAC', 'ADBE', 'NFLX', 'CRM', 'INTC',
    'AMD', 'PYPL', 'TMO', 'COST', 'ABT', 'AVGO', 'NKE', 'PFE', 'MRK', 'CSCO'
]

# Số lượng cổ phiếu top hiển thị
TOP_N = 5

# Thời gian phân tích (số ngày)
SWING_PERIOD = 60  # Lướt sóng: 2-3 tháng
LONGTERM_PERIOD = 365  # Dài hạn: 1 năm

# Ngưỡng điểm cho các tiêu chí
SCORE_WEIGHTS = {
    'swing': {
        'volatility': 0.25,      # Biến động cao
        'rsi': 0.20,             # RSI trong vùng cơ hội
        'macd': 0.20,            # MACD tích cực
        'volume': 0.15,          # Volume tăng
        'trend': 0.20            # Xu hướng ngắn hạn
    },
    'longterm': {
        'trend': 0.30,           # Xu hướng dài hạn mạnh
        'stability': 0.25,       # Ổn định
        'fundamentals': 0.20,    # Cơ bản tốt
        'volume': 0.15,          # Thanh khoản tốt
        'momentum': 0.10         # Động lượng tích cực
    }
}

# Ngưỡng RSI
RSI_OVERSOLD = 30
RSI_OVERBOUGHT = 70
RSI_OPTIMAL_LOW = 35
RSI_OPTIMAL_HIGH = 65
