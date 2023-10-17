import cv2
import time

# Camera 700
cap1 = cv2.VideoCapture(700 + cv2.CAP_DSHOW)
if not cap1.isOpened():
    print("Unable to open camera 700")
else:
    while True:
        ret1, frame1 = cap1.read()
        if not ret1:
            break
        cv2.imshow('Camera 700', frame1)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap1.release()
    cv2.destroyAllWindows()

time.sleep(1)  # Optional: Wait for a second before starting the next camera

# Camera 701
cap2 = cv2.VideoCapture(701 + cv2.CAP_DSHOW)
if not cap2.isOpened():
    print("Unable to open camera 701")
else:
    while True:
        ret2, frame2 = cap2.read()
        if not ret2:
            break
        cv2.imshow('Camera 701', frame2)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap2.release()
    cv2.destroyAllWindows()
