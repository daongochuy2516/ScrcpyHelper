APPVERSION = "1.0.6"
rawver = int(APPVERSION.replace(".",""))
import tkinter as tk
from tkinter import messagebox
import subprocess
from tkinter import Tk, Toplevel, StringVar, OptionMenu, Button, messagebox
import requests
import webbrowser
from screeninfo import get_monitors

tooltip = None


def getres():
    main_monitor = get_monitors()[0]
    if main_monitor.width >= 1920: 
        width = 1920
    width = main_monitor.width

def setres(opt):
    if opt ==1 :
        run_command(["adb", "shell", "wm", "size", "1080x1920"])
    if opt == 2:
        run_command(["adb", "shell", "wm", "size", "reset"])

def show_tooltip(event, text):
    global tooltip
    tooltip = tk.Toplevel(root)
    tooltip.overrideredirect(True)
    tooltip.geometry(f"+{event.x_root+10}+{event.y_root+10}")
    tk.Label(tooltip, text=text, bg="lightyellow", fg="black", relief="solid", borderwidth=1).pack()

def move_tooltip(event):
    if tooltip:
        tooltip.geometry(f"+{event.x_root+10}+{event.y_root+10}")

def hide_tooltip(event):
    global tooltip
    if tooltip:
        tooltip.destroy()
        tooltip = None

def run_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        if result.returncode != 0:
            messagebox.showerror("Lỗi", f"Error: {result.stderr.strip()}")
            return None
        return result.stdout.strip()
    except Exception as e:
        messagebox.showerror("Lỗi", f"An error occurred: {e}")
        return None

def update_version_label():
    version_output = run_command(["scrcpy", "-v"])
    if version_output:
        version = "Không thể xác định"
        for line in version_output.splitlines():
            if "scrcpy" in line.lower():
                parts = line.split()
                if len(parts) > 1:
                    version = parts[1]
                break
        version_label.config(text=f"Phiên bản Scrcpy: {version}")
    else:
        version_label.config(text="Phiên bản Scrcpy: Không thể xác định")

def scrcpy_mode(mode):
    connection_status = connectiontest()
    commands = {
        "View Only Mode": ["scrcpy", "-m1600", "-b6m", "--max-fps=60", "-n"],
        "Control Mode": ["scrcpy", "-m1600", "-b5m", "--max-fps=60", "--mouse-bind=++++"],
        "Otg Mode": ["scrcpy", "-m1600", "-b5m", "--max-fps=60", "-K", "-M", "--mouse-bind=++++"],
        "Dex Mode": ["scrcpy", "--new-display=1920x1080/256", "--max-fps=60", "-K", "-m1366", "-b8m", "--no-mouse-hover", "--stay-awake", "--mouse-bind=++++"],
        "Livestream Mode": ["scrcpy", "-m1600", "-b6m", "--max-fps=60", "--audio-dup", "--video-buffer=70", "--audio-buffer=70"],
        "Livestream Mode+": ["scrcpy", "-m1920", "-b10m", "--max-fps=60", "--audio-dup", "--video-buffer=70", "--audio-buffer=70"],
        "Camera": ["scrcpy", "--video-source=camera", "--camera-id=0", "--camera-size=1920x1080", "--camera-fps=60", "--video-buffer=70", "--audio-buffer=70"],
        "Camera NoMic": ["scrcpy", "--video-source=camera", "--camera-id=0", "--camera-size=1920x1080", "--camera-fps=60", "--video-buffer=70", "--no-audio"],
        "Camera NoDelay": ["scrcpy", "--video-source=camera", "--camera-id=0", "--camera-size=1920x1080", "--camera-fps=60"],
        "Audio": ["scrcpy", "--no-video" ,"--no-control","--audio-buffer=500"],
        "Full Size": []  # Chế độ mới
    }

    if mode == "Full Size":
        width = getres()
        # Tạo lệnh chế độ Full Size
        commands["Full Size"] = [f"scrcpy", f"-m{width}", "-b6m", "--max-fps=60", "--mouse-bind=++++" ]

    if connection_status == 1:
        root.destroy()
        if mode == "Full Size": setres(1)
        run_command(commands[mode])
        if mode == "Full Size": setres(2)
    elif isinstance(connection_status, tuple) and len(connection_status) == 2:
        device_count, devices = connection_status

        def on_device_select():
            selected_device = selected_device_var.get()
            if selected_device:
                root.destroy()
                if mode == "Full Size": setres(1)
                run_command(" ".join(commands[mode]) + f" -s {selected_device}")
                if mode == "Full Size": setres(2)
            else:
                messagebox.showerror("Lỗi", "Vui lòng chọn thiết bị.")
        
        # GUI chọn thiết bị
        device_selection_win = Toplevel()
        device_selection_win.title("Chọn thiết bị")
        device_selection_win.geometry("300x150")

        tk.Label(device_selection_win, text="Chọn thiết bị để chạy Scrcpy:").pack(pady=10)
        selected_device_var = StringVar(device_selection_win)
        selected_device_var.set(devices[0])

        dropdown = OptionMenu(device_selection_win, selected_device_var, *devices)
        dropdown.pack(pady=5)

        confirm_button = Button(device_selection_win, text="Chọn", command=on_device_select)
        confirm_button.pack(pady=10)
    else:
        messagebox.showerror("Lỗi", "Chưa kết nối thiết bị.")

def custom_scrcpy():
    def connect_custom():
        resolution = res_entry.get()
        bitrate = bit_entry.get()
        max_fps = fps_entry.get()
        buffer = buffer_entry.get()
        k = k_var.get()
        m = m_var.get()
        disable_audio = audio_var.get()
        command = ["scrcpy"]
        command.append("--mouse-bind=++++")

        if resolution:
            try:
                resolution = int(resolution)
                if resolution <= 0:
                    raise ValueError
                command.append(f"-m{resolution}")
            except ValueError:
                messagebox.showerror("Lỗi", "Giá trị độ phân giải phải là số dương hợp lệ.")
                return

        if bitrate:
            try:
                bitrate = int(bitrate)
                if bitrate <= 0:
                    raise ValueError
                command.append(f"-b{bitrate}")
            except ValueError:
                messagebox.showerror("Lỗi", "Giá trị bitrate phải là số dương hợp lệ.")
                return

        if max_fps:
            try:
                max_fps = int(max_fps)
                if max_fps <= 0:
                    raise ValueError
                command.append(f"--max-fps={max_fps}")
            except ValueError:
                messagebox.showerror("Lỗi", "Giá trị FPS phải là số dương hợp lệ.")
                return

        if buffer:
            try:
                buffer = int(buffer)
                if buffer < 0:
                    raise ValueError
                command.append(f"--display-buffer={buffer}")
                command.append(f"--audio-buffer={buffer}")
            except ValueError:
                messagebox.showerror("Lỗi", "Giá trị buffer phải là số dương hợp lệ.")
                return

        if k:
            command.append("-K")
        if m:
            command.append("-M")
            command.append("--mouse-bind=++++")
        if disable_audio:
            command.append("--no-audio") 

        final_command = " ".join(command)
        command_label.config(text=f"Command:\n{final_command}")

        custom_win.destroy()
        root.destroy()
        run_command(command)

    def update_command(event=None):
        resolution = res_entry.get()
        bitrate = bit_entry.get()
        max_fps = fps_entry.get()
        buffer = buffer_entry.get()
        k = k_var.get()
        m = m_var.get()
        disable_audio = audio_var.get()
        command = ["scrcpy"]
        

        if resolution:
            try:
                resolution = int(resolution)
                if resolution <= 0:
                    raise ValueError
                command.append(f"-m{resolution}")
            except ValueError:
                command_label.config(text="Lỗi: độ phân giải không hợp lệ")
                return

        if bitrate:
            try:
                bitrate = int(bitrate)
                if bitrate <= 0:
                    raise ValueError
                command.append(f"-b{bitrate}")
            except ValueError:
                command_label.config(text="Lỗi: bitrate không hợp lệ")
                return

        if max_fps:
            try:
                max_fps = int(max_fps)
                if max_fps <= 0:
                    raise ValueError
                command.append(f"--max-fps={max_fps}")
            except ValueError:
                command_label.config(text="Lỗi: fps không hợp lệ")
                return

        if buffer:
            try:
                buffer = int(buffer)
                if buffer < 0:
                    raise ValueError
                command.append(f"--display-buffer={buffer}")
                command.append(f"--audio-buffer={buffer}")
            except ValueError:
                command_label.config(text="Lỗi: buffer không hợp lệ")
                return

        if k:
            command.append("-K")
        if m:
            command.append("-M")
            command.append("--mouse-bind=++++")
        if disable_audio:
            command.append("--no-audio") 

        final_command = " ".join(command)
        command_label.config(text=f"Command: \n{final_command}")

    custom_win = tk.Toplevel(root)
    tk.Label(custom_win, text="Độ phân giải (chỉ nhập chiều ngang):").grid(row=0, column=0)
    res_entry = tk.Entry(custom_win)
    res_entry.grid(row=0, column=1)
    res_entry.bind("<KeyRelease>", update_command)
    tk.Label(custom_win, text="Bitrate:").grid(row=1, column=0)
    bit_entry = tk.Entry(custom_win)
    bit_entry.grid(row=1, column=1)
    bit_entry.bind("<KeyRelease>", update_command)
    tk.Label(custom_win, text="Max FPS:").grid(row=2, column=0)
    fps_entry = tk.Entry(custom_win)
    fps_entry.grid(row=2, column=1)
    fps_entry.bind("<KeyRelease>", update_command)

    tk.Label(custom_win, text="Buffer (ms):").grid(row=3, column=0)
    buffer_entry = tk.Entry(custom_win)
    buffer_entry.grid(row=3, column=1)
    buffer_entry.bind("<KeyRelease>", update_command)

    k_var = tk.BooleanVar()
    m_var = tk.BooleanVar()
    audio_var = tk.BooleanVar()

    k_checkbox = tk.Checkbutton(custom_win, text="Bàn Phím", variable=k_var, command=update_command)
    k_checkbox.grid(row=4, column=0)
    m_checkbox = tk.Checkbutton(custom_win, text="Chuột", variable=m_var, command=update_command)
    m_checkbox.grid(row=5, column=0)
    audio_checkbox = tk.Checkbutton(custom_win, text="Tắt âm thanh", variable=audio_var, command=update_command)
    audio_checkbox.grid(row=6, column=0)

    tk.Button(custom_win, text="Kết nối", command=connect_custom).grid(row=7, column=0, columnspan=3)

    command_label = tk.Label(custom_win, text="Command: scrcpy")
    command_label.grid(row=8, column=0, columnspan=3)

def open_scrcpy_modes():
    def mode_command(mode):
        hide_tooltip(mode)
        scrcpy_win.destroy()
        scrcpy_mode(mode)

    scrcpy_win = tk.Toplevel(root)

    button_data = [
        ("View Only Mode", "Chế độ chỉ xem màn hình thiết bị."),
        ("Control Mode", "Chế độ điều khiển thiết bị."),
        ("Otg Mode", "Chế độ điều khiển giống OTG cho thiết bị."),
        ("Dex Mode", "Chế độ Desktop màn hình rời, 1 số máy sẽ không hỗ trợ!"),
        ("Full Size","Chế độ chiếu toàn màn hình 16:9 (Lưu ý: tắt app trước khi rút dây khi dùng chế độ này)"),
        ("Livestream Mode", "Chế độ chuyên dành cho chiếu màn hình Livestream."),
        ("Livestream Mode+", "Chế độ chuyên dành cho chiếu màn hình Livestream, yêu cầu kết nối ổn định, (1080p60 10k)"),
        ("Camera", "Chiếu Camera lên PC"),
        ("Camera NoMic", "Chiếu Camera lên PC (chỉ hình ảnh)"),
        ("Camera NoDelay", "Chiếu Camera lên PC (không delay)"),
        ("Audio","Chế độ tối ưu cho truyền âm thanh (delay 500ms, ko thích hợp cho chơi game)"),
        ("Tuỳ chỉnh lệnh", "Cấu hình tuỳ chỉnh.")
    ]

    for text, tooltip_text in button_data:
        btn = tk.Button(scrcpy_win, text=text, command=lambda t=text: mode_command(t), width=30)
        btn.pack(fill=tk.BOTH)
        btn.bind("<Enter>", lambda e, tt=tooltip_text: show_tooltip(e, tt))
        btn.bind("<Motion>", move_tooltip)
        btn.bind("<Leave>", hide_tooltip)

def connectiontest():
    devices_output = run_command(["adb", "devices"])
    if devices_output:
        devices = [line.split()[0] for line in devices_output.splitlines() if "\tdevice" in line]
        if len(devices) == 1:
            return 1
        elif len(devices) >= 2:
            print (devices)
            return len(devices), devices
    return 0

def connect_wifi():
    connection_status = connectiontest()
    if connection_status == 1:
        devices_output = run_command(["adb", "devices"])
        if devices_output:
            device_id = [line.split()[0] for line in devices_output.splitlines() if "\tdevice" in line][0]
            ip = get_device_ip(device_id)
            if ip:
                run_command(["adb", "-s", device_id, "tcpip", "5555"])
                connect_result = run_command(["adb", "connect", f"{ip}:5555"])
                if connect_result and "connected" in connect_result:
                    messagebox.showinfo("Info", f"Đã kết nối thiết bị {device_id} qua Wifi ({ip})")
                else:
                    messagebox.showerror("Lỗi", "Kết nối qua Wifi không thành công.")
            else:
                messagebox.showerror("Lỗi", "Không thể kết nối qua Wifi, vui lòng kiểm tra lại.")
        else:
            messagebox.showerror("Lỗi", "Không tìm thấy thiết bị.")
    elif connection_status == 2:
        messagebox.showerror("Lỗi", "Có nhiều hơn 1 thiết bị đang kết nối, vui lòng ngắt kết nối.\nNếu bạn đã kết nối qua Wifi trước đó, vui lòng tháo dây USB\nra khỏi thiết bị hoặc khởi động lại ADB Server.")
    else:
        messagebox.showerror("Lỗi", "Chưa kết nối thiết bị.")

def restart_adb_server():
    run_command(["adb", "kill-server"])
    run_command(["adb", "start-server"])
    messagebox.showinfo("Thông báo", "Đã khởi động lại ADB Server")

def get_device_ip(device_id):
    result = run_command(['adb', '-s', device_id, 'shell', 'ip', '-f', 'inet', 'addr', 'show', 'wlan0'])
    if result:
        for line in result.splitlines():
            if 'inet ' in line:
                return line.split()[1].split('/')[0]
    messagebox.showerror("Lỗi", "Không thể lấy địa chỉ IP của thiết bị.")
    return None

def show_devices():
    devices = run_command(["adb", "devices"])
    if devices:
        messagebox.showinfo("Thiết bị đã kết nối", devices)

def activeshizuku():
    connection_status = connectiontest()
    if isinstance(connection_status, tuple) and len(connection_status) == 2:
        device_count, devices = connection_status
        for device_id in devices:
            result = run_command(["adb", "-s", device_id, "shell", "sh", "/storage/emulated/0/Android/data/moe.shizuku.privileged.api/start.sh"])
            if result:
                messagebox.showinfo("Thành công", f"Shizuku đã được kích hoạt thành công trên thiết bị {device_id}.")
            else:
                messagebox.showerror("Lỗi", f"Không thể kích hoạt Shizuku trên thiết bị {device_id}. Vui lòng kiểm tra lại.")
    elif connection_status == 1:
        result = run_command(["adb", "shell", "sh", "/storage/emulated/0/Android/data/moe.shizuku.privileged.api/start.sh"])
        if result:
            messagebox.showinfo("Thành công", "Shizuku đã được kích hoạt thành công.")
        else:
            messagebox.showerror("Lỗi", "Không thể kích hoạt Shizuku. Vui lòng kiểm tra lại.")
    else:
        messagebox.showerror("Lỗi", "Chưa kết nối thiết bị.")


def disconnect():
    run_command(["adb", "disconnect"])
    messagebox.showinfo("Thành công","Đã ngắt kết nối thiết bị WiFi")

def checkupdate():
    try:
        response = requests.get("https://raw.githubusercontent.com/daongochuy2516/ScrcpyHelper/refs/heads/main/lastestver")
        response.raise_for_status()
        content = response.text.strip()
        if content.isdigit():
            lasver = int(content)
            if lasver == rawver:
                messagebox.showinfo("Thông báo", "Bạn đang sử dụng phiên bản mới nhất!")
            elif lasver > rawver:
                if messagebox.askokcancel(
                    "Cập nhật", 
                    "Phiên bản hiện tại đã cũ, hãy cập nhật để có trải nghiệm tốt hơn! Nhấn OK để cập nhật."
                ):
                    webbrowser.open(f"https://github.com/daongochuy2516/ScrcpyHelper/releases/tag/scrcpyhelper{lasver}") 
            if lasver < rawver:
                messagebox.showinfo("Thông báo", "Bạn đang sử dụng phiên bản Beta.")
        else:
            raise ValueError("Err")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể kiểm tra cập nhật. Vui lòng kiểm tra lại kết nối mạng!")
        return None
    
def opengitpage():
    webbrowser.open("https://github.com/daongochuy2516/ScrcpyHelper")

root = tk.Tk()
root.title("Scrcpy Helper")
root.geometry("270x280")
tk.Button(root, text="Danh sách thiết bị", command=show_devices, width=30).pack(fill=tk.BOTH)
tk.Button(root, text="Kết nối qua WiFi", command=connect_wifi, width=30).pack(fill=tk.BOTH)
tk.Button(root, text="Ngắt kết nối WiFi", command=disconnect, width=30).pack(fill=tk.BOTH)
tk.Button(root, text="Chạy Scrcpy", command=open_scrcpy_modes, width=30).pack(fill=tk.BOTH)
tk.Button(root, text="Active Shizuku", command=activeshizuku, width=30).pack(fill=tk.BOTH)
tk.Button(root, text="Khởi động lại ADB Server", command=restart_adb_server, width=30).pack(fill=tk.BOTH)
tk.Button(root, text="Check Update", command=checkupdate, width=30).pack(fill=tk.BOTH)
tk.Button(root, text="GitHub", command=opengitpage, width=30).pack(fill=tk.BOTH)
tk.Button(root, text="Thoát", command=root.quit, width=30).pack(fill=tk.BOTH)
version_label = tk.Label(root, text="Phiên bản Scrcpy: Đang kiểm tra...")
version_label.pack()
version_app = tk.Label(root, text= f"Phiên bản app: {APPVERSION}")
version_app.pack()

update_version_label()
root.mainloop()
