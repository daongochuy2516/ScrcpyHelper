import tkinter as tk
from tkinter import messagebox
import subprocess

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
        
        if version.startswith("2.6.") and len(version) > 5 and int(version[4:6]) < 6:
            messagebox.showerror("Lỗi", "Phiên bản scrcpy quá cũ. Vui lòng cập nhật lên ít nhất phiên bản 2.6.0.")
    else:
        version_label.config(text="Phiên bản Scrcpy: Không thể xác định")

def scrcpy_mode(mode):
    connection_status = connectiontest()
    if connection_status == 1:
        commands = {
            "View Only Mode": ["scrcpy", "-m1366", "-b6m", "--max-fps=60", "-n"],
            "Control Mode": ["scrcpy", "-m1366", "-b5m", "--max-fps=60", "--mouse-bind=++++"],
            "Otg Mode": ["scrcpy", "-m1366", "-b5m", "--max-fps=60", "-K", "-M", "--mouse-bind=++++"],
            "Livestream Mode": ["scrcpy", "-m1600", "-b6m", "--max-fps=60", "--audio-dup"],
            "Dex Mode": ["scrcpy", "--new-display=1920x1080/256", "--max-fps=60", "-K", "-m1366", "-b8m", 
                         "--no-mouse-hover", "--stay-awake", "--mouse-bind=++++"]
        }
        root.destroy()
        run_command(commands[mode])
    elif connection_status == 2:
        messagebox.showerror("Lỗi", "Có nhiều hơn 1 thiết bị đang kết nối, vui lòng ngắt kết nối.")
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
        scrcpy_win.destroy()
        scrcpy_mode(mode)

    scrcpy_win = tk.Toplevel(root)
    tk.Button(scrcpy_win, text="View Only Mode", command=lambda: mode_command("View Only Mode"), width=30).pack(fill=tk.BOTH)
    tk.Button(scrcpy_win, text="Control Mode", command=lambda: mode_command("Control Mode"), width=30).pack(fill=tk.BOTH)
    tk.Button(scrcpy_win, text="Otg Mode", command=lambda: mode_command("Otg Mode"), width=30).pack(fill=tk.BOTH)
    tk.Button(scrcpy_win, text="Livestream Mode", command=lambda: mode_command("Livestream Mode"), width=30).pack(fill=tk.BOTH)
    tk.Button(scrcpy_win, text="Dex Mode", command=lambda: mode_command("Dex Mode"), width=30).pack(fill=tk.BOTH)
    tk.Button(scrcpy_win, text="Tuỳ chỉnh lệnh", command=lambda: [scrcpy_win.destroy(), custom_scrcpy()], width=30).pack(fill=tk.BOTH)

def connectiontest():
    devices_output = run_command(["adb", "devices"])
    if devices_output:
        devices = [line.split()[0] for line in devices_output.splitlines() if "\tdevice" in line]
        if len(devices) == 1:
            return 1
        elif len(devices) == 0:
            return 0
        elif len(devices) > 1:
            return 2
    return False

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

root = tk.Tk()
root.title("Scrcpy Helper")
root.geometry("270x175")

tk.Button(root, text="Danh sách thiết bị", command=show_devices, width=30).pack(fill=tk.BOTH)
tk.Button(root, text="Kết nối qua Wifi", command=connect_wifi, width=30).pack(fill=tk.BOTH)
tk.Button(root, text="Chạy Scrcpy", command=open_scrcpy_modes, width=30).pack(fill=tk.BOTH)
tk.Button(root, text="Khởi động lại ADB Server", command=restart_adb_server, width=30).pack(fill=tk.BOTH)
tk.Button(root, text="Thoát", command=root.quit, width=30).pack(fill=tk.BOTH)
version_label = tk.Label(root, text="Phiên bản Scrcpy: Đang kiểm tra...")
version_label.pack()
version_app = tk.Label(root, text= "Phiên bản app: 1.0.0")
version_app.pack()

update_version_label()
root.mainloop()
