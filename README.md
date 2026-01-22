# 📈 Stock Analysis Pro

Ứng dụng phân tích cổ phiếu thông minh với giao diện đẹp mắt, hỗ trợ cả lướt sóng và đầu tư dài hạn.

## ✨ Tính năng

### 🎯 Chiến lược đầu tư
- **Lướt sóng (Swing Trading)**: Tìm cổ phiếu có biến động tốt cho giao dịch ngắn hạn (2-3 tuần)
- **Đầu tư dài hạn**: Tìm cổ phiếu có xu hướng tăng ổn định cho nắm giữ lâu dài

### 📊 Phân tích kỹ thuật
- RSI (Relative Strength Index)
- MACD (Moving Average Convergence Divergence)
- Moving Averages (SMA 20, 50, 200)
- Bollinger Bands
- Volume Analysis

### 💎 Gợi ý giao dịch thông minh
- Điểm mua tối ưu
- Điểm bán mục tiêu
- Stop Loss & Take Profit
- Khuyến nghị cụ thể cho từng cổ phiếu

### 🌍 Thị trường
- 🇻🇳 Thị trường Việt Nam (VN30 + hơn 50 cổ phiếu blue-chip và mid-cap)
- Phân tích chuyên sâu HOSE & HNX
- Dữ liệu realtime từ Yahoo Finance

## 🚀 Cài đặt

### 1. Cài đặt Python
Đảm bảo bạn đã cài Python 3.8 trở lên

### 2. Cài đặt thư viện
```bash
pip install -r requirements.txt
```

### 3. Chạy ứng dụng
```bash
streamlit run app.py
```

Ứng dụng sẽ tự động mở trong trình duyệt tại `http://localhost:8501`

## 📖 Hướng dẫn sử dụng

### Bước 1: Chọn cấu hình
1. Mở ứng dụng
2. Ở sidebar bên trái, chọn:
   - **Chiến lược**: Lướt sóng hoặc Đầu tư dài hạn
   - **Số lượng cổ phiếu**: 3-10 cổ phiếu
   (Thị trường mặc định: Việt Nam 🇻🇳)

### Bước 2: Phân tích
1. Nhấn nút **"Bắt đầu phân tích"**
2. Đợi 1-2 phút để hệ thống phân tích
3. Xem danh sách top cổ phiếu được đề xuất

### Bước 3: Xem chi tiết
1. Click vào nút **"Chi tiết"** của cổ phiếu bạn quan tâm
2. Xem:
   - Giá hiện tại & các chỉ báo
   - Khuyến nghị giao dịch (MUA/BÁN/GIỮ)
   - Điểm mua và điểm bán cụ thể
   - Biểu đồ kỹ thuật chi tiết
   - Stop Loss & Take Profit

## 🎓 Giải thích các chỉ số

### RSI (Relative Strength Index)
- **< 30**: Vùng quá bán (oversold) - Cơ hội mua
- **30-70**: Vùng trung lập
- **> 70**: Vùng quá mua (overbought) - Cảnh báo bán

### MACD
- **MACD > Signal**: Tín hiệu tích cực (tăng)
- **MACD < Signal**: Tín hiệu tiêu cực (giảm)
- **Histogram > 0**: Momentum tăng

### Moving Averages
- **Giá > SMA20 > SMA50 > SMA200**: Xu hướng tăng mạnh
- **Golden Cross** (SMA50 cắt lên SMA200): Tín hiệu mua mạnh
- **Death Cross** (SMA50 cắt xuống SMA200): Tín hiệu bán mạnh

### Bollinger Bands
- Giá chạm **BB Lower**: Cơ hội mua
- Giá chạm **BB Upper**: Cảnh báo overbought
- BB **thu hẹp**: Sắp có biến động lớn

## ⚠️ Lưu ý quan trọng

1. **Không phải lời khuyên tài chính**: Đây chỉ là công cụ hỗ trợ, không phải khuyến nghị đầu tư
2. **Luôn nghiên cứu thêm**: Kết hợp với phân tích cơ bản và tin tức
3. **Quản lý rủi ro**: Luôn đặt Stop Loss và không đầu tư quá 5% tài kản vào 1 cổ phiếu
4. **Cập nhật dữ liệu**: Dữ liệu từ Yahoo Finance, có thể có độ trễ

## 🛠️ Kỹ thuật sử dụng

### Công thức tính điểm (Scoring)

#### Lướt sóng (100 điểm tối đa):
- Volatility (25 điểm): Biến động 2-5% là tốt nhất
- RSI (20 điểm): RSI 35-65 là tối ưu
- MACD (20 điểm): MACD > Signal và Histogram > 0
- Volume (15 điểm): Volume > trung bình 20 ngày
- Trend (20 điểm): Giá > SMA20 > SMA50

#### Đầu tư dài hạn (100 điểm tối đa):
- Long-term Trend (30 điểm): Giá > SMA50 > SMA200
- Stability (25 điểm): Volatility < 2% là tốt
- Fundamentals (20 điểm): >60% ngày tăng trong 30 ngày
- Volume Quality (15 điểm): Volume cải thiện theo thời gian
- Momentum (10 điểm): RSI 50-70

## 🔧 Tùy chỉnh

Bạn có thể chỉnh sửa file `config.py` để:
- Thay đổi danh sách cổ phiếu phân tích
- Điều chỉnh các ngưỡng RSI
- Thay đổi trọng số tính điểm
- Cấu hình thời gian phân tích

## 📝 Ví dụ sử dụng

### Kịch bản 1: Tìm cổ phiếu lướt sóng 🌊
```
1. Chọn "Lướt sóng"
2. Top 5 cổ phiếu
3. Nhấn "Phân tích"
4. Chọn cổ phiếu có điểm cao nhất (VD: HPG, TCB)
5. Xem điểm mua (Buy Zone) và Stop Loss
6. Theo dõi RSI & MACD
7. Đặt lệnh theo khuyến nghị
```

### Kịch bản 2: Đầu tư dài hạn 📊
```
1. Chọn "Đầu tư dài hạn"
2. Top 5-10 cổ phiếu
3. Nhấn "Phân tích"
4. Xem cổ phiếu có xu hướng tốt (VD: VNM, VCB, FPT)
5. Xem vùng tích lũy và mục tiêu giá
6. Mua dần dần trong vùng tích lũy
7. Nắm giữ 6-12 tháng
```

## 🤝 Đóng góp

Mọi đóng góp đều được chào đón! Hãy tạo Issue hoặc Pull Request.

## 🌐 Deploy Miễn Phí

Ứng dụng này có thể deploy **HOÀN TOÀN MIỄN PHÍ** lên Streamlit Community Cloud!

### Quick Deploy (3 bước):
1. **Push code lên GitHub** (xem [DEPLOY.md](DEPLOY.md))
2. **Vào https://share.streamlit.io/**
3. **Click "New app" và chọn repo của bạn**

Chi tiết đầy đủ: [DEPLOY.md](DEPLOY.md)

### Demo Online
Sau khi deploy, app sẽ có URL:
```
https://your-username-stock-analysis-vn.streamlit.app
```

## 📄 License

MIT License - Sử dụng tự do cho mục đích cá nhân và thương mại.

## 📧 Liên hệ

Nếu có câu hỏi hoặc góp ý, vui lòng tạo Issue trên GitHub.

---

**Chúc bạn đầu tư thành công! 🚀📈**
