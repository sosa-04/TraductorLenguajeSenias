import cv2
import mediapipe as mp

mp_hands= mp.solutions.hands
mp_drawing= mp.solutions.drawing_utils

cap= cv2.VideoCapture(0)

def gen_frame():
    with mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
        while True:
            ret, frame= cap.read()

            if not ret:
                break
            else:
                suc, encode= cv2.imencode('.jpg', frame)
                frame= encode.tobytes()
                
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')