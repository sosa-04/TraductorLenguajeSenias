import cv2
import mediapipe as mp
import numpy as np
from tensorflow.keras.models import load_model

modelo= load_model('modeloLenguajeSenias.h5')
mp_hands= mp.solutions.hands
mp_drawing= mp.solutions.drawing_utils

gestos= ['Hola', 'Adios', 'Bien', 'Gracias', 'Mal']

cap= cv2.VideoCapture(0)

def gen_frame():
    with mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
        while True:
            ret, frame= cap.read()

            if not ret:
                break
            else:

                frame_rgb= cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                resultado= hands.process(frame_rgb)

                coordenadas_manos= []
                if resultado.multi_hand_landmarks:
                    for mano in resultado.multi_hand_landmarks:
                        coordenadas_mano= []
                        for punto in mano.landmark:
                            coordenadas_mano.extend([punto.x, punto.y, punto.z])
                        coordenadas_manos.append(coordenadas_mano)


                    if  len(coordenadas_mano) == 2:
                        entrada= np.concatenate(coordenadas_manos).reshape(1, -1)
                    elif len(coordenadas_manos) == 1:
                        entrada= np.concatenate([coordenadas_manos[0], [0] * len(coordenadas_manos[0])]).reshape(1, -1)
                    else:
                        entrada= None


                    if entrada is not None:
                        prediccion= modelo.predict(entrada)
                        gesto_predicho= gestos[np.argmax(prediccion)]
                        probabilidad= np.max(prediccion)
                        cv2.putText(frame, gesto_predicho, (10,70),
                                    cv2.FONT_HERSHEY_DUPLEX, 3, (255, 0, 0), 3, cv2.LINE_AA)

                suc, encode= cv2.imencode('.jpg', frame)
                frame= encode.tobytes()
                
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')