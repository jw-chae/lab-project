import cv2
import threading

class CameraCapture(threading.Thread):
    def __init__(self, device_id):
        super().__init__()
        self.device_id = device_id
        self.cap = cv2.VideoCapture(self.device_id)

        if not self.cap.isOpened():
            raise ValueError("Unable to open device", self.device_id)

    def run(self):
        while True:
            ret, frame = self.cap.read()

            if not ret:
                break

            cv2.imshow('Camera {}'.format(self.device_id), frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

cap1 = CameraCapture(0+cv2.CAP_DSHOW)
cap2 = CameraCapture(1+cv2.CAP_DSHOW)

cap1.start()
cap2.start()

cap1.join()
cap2.join()
