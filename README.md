# Scrcpy Helper  

### English Section  

**Language:** Currently supports Vietnamese only.  
**Platform:** Windows (requires scrcpy and ADB installed).  

**Note:** This application is specifically designed for Vietnamese users. English support is not available at this time.  

---

### Vietnamese Section  

**Ngôn ngữ:** Tiếng Việt  

Scrcpy Helper là một ứng dụng hỗ trợ sử dụng **scrcpy** trên Windows. Nó cung cấp giao diện người dùng trực quan để quản lý và tùy chỉnh các chế độ sử dụng của scrcpy, bao gồm:  

- **Kết nối qua Wifi:** Hỗ trợ kết nối thiết bị qua WiFi (gỡ lỗi không dây, ghép nối đơn giản)
- **Chạy Scrcpy:** Chọn chế độ **scrcpy** phù hợp đã được cài đặt sẵn (Chỉ xem, Điều khiển, Livestream, Dex, Camera, v.v.).  
- **Tùy chỉnh lệnh:** Tự cấu hình các thông số như độ phân giải, bitrate, FPS, buffer, v.v.  
- **Active Shizuku:** Kích hoạt Shizuku để chạy các ứng dụng yêu cầu quyền truy cập đặc biệt.  
- **Quản lý thiết bị:** Xem danh sách thiết bị đã kết nối

**Yêu cầu:**  
1. Máy tính cần cài đặt sẵn **scrcpy** và **ADB**.  
2. Kết nối thiết bị qua USB hoặc Wifi.

---

## Hướng dẫn sử dụng chi tiết  

### Cài đặt ban đầu  
1. **Cài đặt ADB và scrcpy**  
   - Tải scrcpy từ [scrcpy GitHub](https://github.com/Genymobile/scrcpy).  
   - Tải file release scrcpyhelper.exe và copy vào thư mục đã giải nén của scrcpy

2. **Kiểm tra kết nối thiết bị**  
   - Bật chế độ **USB Debugging** trên thiết bị Android.  
   - Kết nối thiết bị qua cáp USB.

---

### Sử dụng các tính năng  

#### 1. **Danh sách thiết bị**  
- Nhấn nút **"Danh sách thiết bị"** để hiển thị danh sách các thiết bị đã kết nối qua ADB.  

#### 2. **Kết nối qua Wifi**  
- Nhấn **"Kết nối qua Wifi"** để kết nối thiết bị không dây.  
  - Yêu cầu: Thiết bị phải kết nối vào cùng 1 mạng WiFi với PC và đã kết nối USB với PC này.
  - Sau khi kết nối hoàn tất, bạn có thể tháo dây USB.  

#### 3. **Chạy Scrcpy**  
- Nhấn **"Chạy Scrcpy"** để chọn chế độ:  
  - **View Only Mode:** Chỉ xem màn hình, không điều khiển.  
  - **Control Mode:** Điều khiển và tương tác với thiết bị.  
  - **Livestream Mode:** Chiếu màn hình chuyên dụng cho livestream, đã được tối ưu để truyền tải mượt mà trên WiFi và USB
  - **Dex Mode¹:** Kích hoạt chế độ Desktop màn hình rời trên một số thiết bị hỗ trợ.  
  - **Camera Mode:** Sử dụng camera của thiết bị.  
  - **Tùy chỉnh lệnh:** Cấu hình tùy chỉnh theo nhu cầu.  

#### 4. **Tùy chỉnh lệnh**  
- Nhấn **"Tùy chỉnh lệnh"**, nhập các thông số như:  
  - **Độ phân giải:** Chiều ngang màn hình (vd: 1366).  
  - **Bitrate:** Tốc độ dữ liệu truyền (vd: 5m).  
  - **FPS:** Số khung hình trên giây (vd: 60).  
  - **Buffer²:** Buffer âm thanh/video (ms).  
  - Tùy chọn bổ sung: Bật bàn phím, chuột, tắt âm thanh.  

#### 5. **Active Shizuku**  
- Nhấn **"Active Shizuku"** để chạy script kích hoạt Shizuku.  
  - Điều kiện: Thiết bị phải cài đặt ứng dụng Shizuku

#### 6. **Khởi động lại ADB Server**  
- Nhấn **"Khởi động lại ADB Server"** để reset dịch vụ ADB.  

#### 7. **Thoát ứng dụng**  
- Nhấn **"Thoát"** để đóng ứng dụng.  

---

### Lưu ý  
- **ADB Debugging:** Thiết bị cần bật chế độ gỡ lỗi USB trong mục Developer Options.  
- **Kết nối Wifi:** Cần đảm bảo thiết bị và PC dùng chung một mạng Wifi.
- **Dex Mode¹:** Là chế độ Desktop, có sẵn của Android, chế độ này cung cấp giao diện tương tự Samsung Dex (cần vào tuỳ chọn nhà phát triển và bật **buộc giao diện máy tính trên màn hình ngoài**), một số máy sẽ không hoạt động đúng cách!
- **Buffer²:** Là khoảng thời gian delay để bảo đảm truyền nhận gói được mượt mà

Nếu gặp vấn đề, vui lòng kiểm tra kết nối và đảm bảo cấu hình đúng.  
