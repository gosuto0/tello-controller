import UI.main
import time
import socket
import threading

#pitch	ピッチ (角度)
#roll	ロール (角度)
#yaw	ヨー (角度)
#vgx	x速度
#vgy	y速度
#vgz	z速度
#templ	最低温度 (℃)
#temph	最高温度 (℃)
#tof	TOF距離 (cm)
#h	高さ(cm)
#bat	バッテリー残量 (%)
#baro	気圧 (cm)
#time	モーター起動時間
#agx	x加速度
#agy	y加速度
#agz	z加速度

class tello:
    def __init__(self,tello_ip,tello_port,video_port):
        self.tello_ip = tello_ip
        self.tello_port = tello_port
        self.video_port = video_port
        self.send_flag = True
        self.speed = 50
        
    def setup(self, ui_class):
        self.tello_address = (self.tello_ip, self.tello_port)
        self.sock_command = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock_command.bind(('', self.tello_port))
        self.ui_class = ui_class
        
        self.sock_command.sendto("command".encode(), self.tello_address)
        self.sock_command.sendto("streamon".encode(), self.tello_address)

        threading.Thread(target=lambda: self.ui_class.update_drone_state(), args=()).start()
        self.ui_class.setup_video()
        
    def send_data(self, data):
        threading.Thread(target=lambda: self.send_data_thread(data), args=()).start()

    def send_data_thread(self, data):
        if data == "switch_speed":
            if self.speed == 50:
                self.speed = 10
            elif self.speed == 10:
                self.speed = 30
            elif self.speed == 30:
                self.speed = 50
            print("Switch Speed: "+str(self.speed))
        self.sock_command.sendto(data.encode(), self.tello_address)
        
def main(tello_ip,tello_port,video_port):
    tello_class = tello(tello_ip,tello_port,video_port)
    UI.main.ThreadWithReturnValue(tello_class)
