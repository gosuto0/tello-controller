import tkinter as tk
from tkinter import *
import threading
import TELLO.main as tello
import CNN.face as face
from PIL import Image, ImageTk, ImageOps
import cv2
import keyboard
import CNN.yolov5 as yolo
import time
import socket


tello_ip = "192.168.10.1"
tello_port = 8889
video_ip = "udp://@0.0.0.0:11111?overrun_nonfatal=1&fifo_size=50000000"
value = None


class UI(tk.Frame):
    def __init__(self, tk, tello, tello_ip, tello_port, video_ip):
        # tk config
        self.theme = "#0D1117"
        self.frame_theme = "#0D1117"
        self.linetheme = "#222e3f"
        self.button_theme = "White"
        self.font = "robot"
        self.title = "Tello Controller"
        self.size = "1280x720"

        # tk setup
        self.tk = tk
        self.tk.configure(bg=self.theme)
        self.tk.title(self.title)
        self.tk.geometry(self.size)

        # tello config
        self.tello_class = tello
        self.tello_ip = tello_ip
        self.tello_port = tello_port
        self.video_ip = video_ip
        self.videomode = 0
        self.video = True
        self.a = 0
        self.b = 0
        self.c = 0
        self.d = 0

        # function
        self.setup()

    def setup(self):
        self.setup_frame()
        self.setup_control()

        threading.Thread(target=lambda: self.tello_class.setup(self), args=()).start()
        threading.Thread(target=lambda: self.rc_input(), args=()).start()

    def setup_frame(self):
        # video frame
        self.video_frame = Frame(self.tk, width=1080, height=720)
        self.video_frame.place(x=0, y=0)
        self.video_frame.configure(bg=self.frame_theme)

        # controller frame
        self.controller_frame = Frame(self.tk, width=200, height=720)
        self.controller_frame.place(x=1082, y=0)
        self.controller_frame.configure(bg=self.frame_theme)

    def setup_control(self):
        # config
        self.key_input = tk.BooleanVar(value=True)
        self.rc_control = tk.BooleanVar(value=True)
        self.rc_bind()

        # label
        self.bat = tk.StringVar()
        self.time = tk.StringVar()
        self.temp = tk.StringVar()
        self.tof = tk.StringVar()

        self.bat.set("Battery: 0%")
        self.time.set("Time: 00:00")
        self.temp.set("temp: 0C")
        self.tof.set("Tof: 0cm")

        Label(
            self.controller_frame, textvariable=self.bat, bg=self.theme, fg="white"
        ).place(x=10, y=290)
        Label(
            self.controller_frame, textvariable=self.time, bg=self.theme, fg="white"
        ).place(x=10, y=320)
        Label(
            self.controller_frame, textvariable=self.temp, bg=self.theme, fg="white"
        ).place(x=10, y=350)
        Label(
            self.controller_frame, textvariable=self.tof, bg=self.theme, fg="white"
        ).place(x=10, y=380)
        # BTNfunc

        Button(
            self.controller_frame,
            text="速度変更",
            bg=self.button_theme,
            relief="raised",
            width=5,
            height=2,
            justify=CENTER,
            command=lambda: self.tello_class.send_data("switch_speed"),
        ).place(x=10, y=30)
        Button(
            self.controller_frame,
            text="Emr",
            bg=self.button_theme,
            relief="raised",
            width=5,
            height=2,
            justify=CENTER,
            command=lambda: self.tello_class.send_data("emergency"),
        ).place(x=10, y=80)
        Button(
            self.controller_frame,
            text="VideoOn",
            bg=self.button_theme,
            relief="raised",
            width=5,
            height=2,
            justify=CENTER,
            command=lambda: self.tello_class.send_data("streamon"),
        ).place(x=10, y=130)
        Button(
            self.controller_frame,
            text="Off",
            bg=self.button_theme,
            relief="raised",
            width=5,
            height=2,
            justify=CENTER,
            command=lambda: self.tello_class.send_data("streamoff"),
        ).place(x=10, y=180)
        Button(
            self.controller_frame,
            text="Tgl",
            bg=self.button_theme,
            relief="raised",
            width=5,
            height=2,
            justify=CENTER,
            command=lambda: self.toggle_videomode(),
        ).place(x=10, y=230)

        # CBfunc
        tk.Checkbutton(
            self.controller_frame,
            text="キーボード入力",
            bg=self.theme,
            fg="white",
            selectcolor=self.theme,
            command=lambda: self.switch_bind(),
            variable=self.key_input,
        ).place(x=5, y=3)

        # scalebar
        self.drone_v = tk.Scale(
            self.controller_frame,
            from_=100,
            to=0,
            label="移動量",
            bg=self.button_theme,
            length=230,
        )
        self.drone_v.place(x=80, y=30)
        self.drone_v.set(50)

    # keyboard
    def switch_bind(self):
        self.clear_bind()
        if self.key_input.get():
            if self.rc_input.get():
                self.setup_rc()
            else:
                self.setup_bind()

    def key_bind(self):
        keyboard.on_press_key("w", lambda _: self.tello_class.send_data("forward 20"))
        keyboard.on_press_key("s", lambda _: self.tello_class.send_data("back 20"))
        keyboard.on_press_key("d", lambda _: self.tello_class.send_data("right 50"))
        keyboard.on_press_key("a", lambda _: self.tello_class.send_data("left 50"))
        keyboard.on_press_key("e", lambda _: self.tello_class.send_data("cw 15"))
        keyboard.on_press_key("q", lambda _: self.tello_class.send_data("ccw 15"))
        keyboard.on_press_key("z", lambda _: self.tello_class.send_data("takeoff"))
        keyboard.on_press_key("x", lambda _: self.tello_class.send_data("land"))
        keyboard.on_press_key("c", lambda _: self.tello_class.send_data("switch_speed"))
        keyboard.on_press_key("r", lambda _: self.tello_class.send_data("up 40"))
        keyboard.on_press_key("f", lambda _: self.tello_class.send_data("down 40"))

    def clear_bind(self):
        keyboard.unhook_all()

    def rc_bind(self):
        keyboard.on_press_key("z", lambda _: self.tello_class.send_data("takeoff"))
        keyboard.on_press_key("x", lambda _: self.tello_class.send_data("land"))
        keyboard.on_press_key("c", lambda _: self.tello_class.send_data("switch_speed"))

    def rc_input(self):
        while True:
            time.sleep(0.05)
            if self.rc_control == False:
                continue
            if keyboard.is_pressed("d"):
                self.a = self.drone_v.get()
            else:
                if self.a >= 0:
                    self.a = 0
            if keyboard.is_pressed("a"):
                self.a = -self.drone_v.get()
            else:
                if self.a <= 0:
                    self.a = 0
            if keyboard.is_pressed("w"):
                self.b = self.drone_v.get()
            else:
                if self.b >= 0:
                    self.b = 0
            if keyboard.is_pressed("s"):
                self.b = -self.drone_v.get()
            else:
                if self.b <= 0:
                    self.b = 0
            if keyboard.is_pressed("r"):
                self.c = self.drone_v.get()
            else:
                if self.c >= 0:
                    self.c = 0
            if keyboard.is_pressed("f"):
                self.c = -self.drone_v.get()
            else:
                if self.c <= 0:
                    self.c = 0
            if keyboard.is_pressed("e"):
                self.d = self.drone_v.get()
            else:
                if self.d >= 0:
                    self.d = 0
            if keyboard.is_pressed("q"):
                self.d = -self.drone_v.get()
            else:
                if self.d <= 0:
                    self.d = 0
            self.tello_class.send_data(f"rc {self.a} {self.b} {self.c} {self.d}")

    # video stream

    def setup_video(self):
        threading.Thread(target=lambda: self.stream_ready(), args=()).start()

    def stream_ready(self):
        self.canvas = tk.Canvas(self.video_frame, width=1080, height=720)
        self.canvas.pack()

        # self.capture = vw.ThreadingVideoCapture(self.video_ip)
        self.capture = cv2.VideoCapture(self.video_ip)
        # self.capture.start()
        self.disp_image()

    def disp_image(self):
        try:
            for i in range(2):
                self.capture.read()
            _, frame = self.capture.read()
            pil_image = Image.fromarray(self.overray_image(frame))
            self.photo_image = ImageTk.PhotoImage(image=pil_image)
            t = time.perf_counter()
            self.canvas.create_image(1080 / 2, 720 / 2, image=self.photo_image)
            self.after(3, self.disp_image)
        except:
            pass

    def overray_image(self, frame):
        cv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        if self.videomode == 0:
            cv2.putText(
                cv_image,
                "VideoMode: None",
                (3, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                1,
            )
        if self.videomode == 1:
            cv_image = face.face_detect(cv_image)
            cv2.putText(
                cv_image,
                "VideoMode: CascadeFace",
                (3, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                1,
            )
        if self.videomode == 2:
            cv_image = yolo.main_n(frame, cv_image)
            cv2.putText(
                cv_image,
                "VideoMode: Yolov5",
                (3, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                1,
            )
        if self.videomode == 3:
            cv_image = yolo.main_p(frame, cv_image)
            cv2.putText(
                cv_image,
                "VideoMode: Yolov5Pandas[Person]",
                (3, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                1,
            )
        if self.videomode == 4:
            cv_image = yolo.main_m(frame, cv_image)
            cv2.putText(
                cv_image,
                "VideoMode: Yolov5Pandas[All]",
                (3, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                1,
            )

        return cv_image

    def toggle_videomode(self):
        if self.videomode <= 3:
            self.videomode = self.videomode + 1
        else:
            self.videomode = 0
        print("toggle video mode: " + str(self.videomode))

    def update_drone_state(self):
        state_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        state_sock.bind(("", 8890))
        while True:
            data, _ = state_sock.recvfrom(1024)
            data = self.get_drone_state(data)
            self.bat.set("Battery: " + str(data["bat"]) + "%")
            self.temp.set("Temp: " + str((data["temph"] - 32) / 1.8) + "C")
            self.time.set("Time: " + str(data["time"]))
            self.tof.set("Tof: " + str(data["tof"]) + "cm")
            self.controller_frame.update()
            time.sleep(5)

    def get_drone_state(self, data):
        s = data.decode(errors="replace")
        values = s.split(";")
        state = {}
        for v in values:
            kv = v.split(":")
            if len(kv) > 1:
                state[kv[0]] = float(kv[1])
        return state


# main function
def ThreadWithReturnValue(data):
    global value
    value = data


def main():
    global value
    root = tk.Tk()
    threading.Thread(
        target=lambda: tello.main(tello_ip, tello_port, video_ip), args=()
    ).start()
    while value == None:
        pass
    UI(root, value, tello_ip, tello_port, video_ip)
    root.mainloop()
