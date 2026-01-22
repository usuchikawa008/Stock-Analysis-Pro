# 🚀 Hướng Dẫn Deploy Lên Streamlit Community Cloud (MIỄN PHÍ)

## ✅ Streamlit Community Cloud HOÀN TOÀN MIỄN PHÍ!

### 📋 Yêu cầu:
- ✅ Tài khoản GitHub (miễn phí)
- ✅ Tài khoản Streamlit Community Cloud (miễn phí)
- ✅ Code đã hoạt động tốt ở local

## 🔧 Bước 1: Tạo GitHub Repository

### Cách 1: Dùng Git Command Line
```bash
# Khởi tạo git (nếu chưa có)
cd C:\work\Stock
git init

# Add tất cả files
git add .

# Commit
git commit -m "Initial commit - Stock Analysis Pro"

# Tạo repo trên GitHub.com rồi link vào
# Vào https://github.com/new để tạo repo mới (ví dụ: stock-analysis-vn)

# Link remote repository
git remote add origin https://github.com/<username>/stock-analysis-vn.git

# Push code lên
git branch -M main
git push -u origin main
```

### Cách 2: Dùng GitHub Desktop (Dễ hơn!)
1. Tải GitHub Desktop: https://desktop.github.com/
2. Mở GitHub Desktop
3. File → Add Local Repository → Chọn thư mục `C:\work\Stock`
4. "Publish repository" để đẩy lên GitHub
5. Chọn tên repo (VD: stock-analysis-vn)
6. Bỏ tick "Keep this code private" nếu muốn public
7. Click "Publish repository"

## 🌐 Bước 2: Deploy Lên Streamlit Community Cloud

### 2.1. Đăng ký tài khoản (MIỄN PHÍ)
1. Vào https://share.streamlit.io/
2. Sign in với GitHub account
3. Authorize Streamlit (cho phép truy cập repos)

### 2.2. Deploy App
1. Click "New app"
2. Chọn:
   - **Repository:** stock-analysis-vn (repo vừa tạo)
   - **Branch:** main
   - **Main file path:** app.py
3. Click "Deploy!"
4. Đợi 3-5 phút để deploy

### 2.3. URL của bạn
App sẽ có URL dạng:
```
https://<username>-stock-analysis-vn.streamlit.app/
```

## 📦 Files Quan Trọng (Đã có sẵn)

✅ **requirements.txt** - Các thư viện cần thiết
✅ **app.py** - File chính của ứng dụng
✅ **.gitignore** - Loại trừ files không cần thiết
✅ **README.md** - Mô tả dự án

## ⚡ Tự động Update

Mỗi khi bạn push code mới lên GitHub:
```bash
git add .
git commit -m "Update features"
git push
```

App trên Streamlit sẽ **TỰ ĐỘNG deploy lại** trong vài phút! 🎉

## 🎁 Giới Hạn Free Tier

**Streamlit Community Cloud FREE bao gồm:**
- ✅ Unlimited apps (không giới hạn số app)
- ✅ Unlimited viewers (không giới hạn người xem)
- ✅ 1 GB RAM per app
- ✅ 1 CPU core per app
- ✅ Auto SSL (HTTPS)
- ✅ Custom domain (có thể dùng domain riêng)
- ✅ GitHub integration

**Lưu ý:**
- App sẽ sleep sau 7 ngày không dùng (wake up tự động khi truy cập)
- Max 3 apps cùng lúc cho tài khoản free
- Nếu app dùng quá 1GB RAM sẽ bị restart

## 🔒 Nếu Muốn Private App

App miễn phí là **public** (ai cũng truy cập được).

Nếu muốn private:
- Cần upgrade lên Streamlit for Teams ($250/tháng)
- Hoặc tự host (VPS, Heroku, AWS...)

## 🚀 Tối Ưu Hiệu Suất

Để app chạy nhanh hơn trên free tier:

1. **Cache dữ liệu:**
   - Sử dụng `@st.cache_data` cho functions tốn thời gian
   - Giảm số lượng API calls

2. **Giảm RAM usage:**
   - Chỉ load dữ liệu cần thiết
   - Clear cache khi không dùng

3. **Optimize code:**
   - Giảm số lượng cổ phiếu phân tích đồng thời
   - Sử dụng pagination

## 📞 Support

Nếu gặp vấn đề:
- Docs: https://docs.streamlit.io/streamlit-community-cloud
- Forum: https://discuss.streamlit.io/
- GitHub Issues: https://github.com/streamlit/streamlit/issues

## 🎯 Next Steps

Sau khi deploy thành công:
1. Share URL với bạn bè
2. Thêm vào portfolio/CV
3. Customize domain (nếu có)
4. Monitor usage trong dashboard

---

**Chúc bạn deploy thành công! 🚀📈**
