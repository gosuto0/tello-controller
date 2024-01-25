import threading
import queue
import cv2

class ThreadingVideoCapture:
    def __init__(self, src, max_queue_size=256):
        self.video = cv2.VideoCapture(src)
        self.q = queue.Queue(maxsize=max_queue_size)
        self.stopped = False

    def start(self):
        thread = threading.Thread(target=self.update, daemon=True)
        thread.start()
        return self

    def update(self):
        while True:
            if self.stopped:
                return
            if not self.q.full():
                print(self.q.qsize())
                ok, frame = self.video.read()
                self.q.put((ok, frame))

                if not ok:
                    self.stop()
                    return

    def read(self):
        return self.q.get()

    def stop(self):
        self.stopped = True

    def release(self):
        self.stopped = True
        self.video.release()

    def isOpened(self):
        return self.video.isOpened()

    def get(self, i):
        return self.video.get(i)