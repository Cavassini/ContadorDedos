import cv2
import mediapipe as mp
import random
import keyboard

video = cv2.VideoCapture(0)

hands = mp.solutions.hands
Hands = hands.Hands(max_num_hands=1)
mpDraw = mp.solutions.drawing_utils

def gerar_numero_aleatorio():
    return random.randint(0, 1)

numero_aleatorio = gerar_numero_aleatorio()

# Estado anterior da contagem de dedos
estado_anterior = None

while True:
    success, img = video.read()
    frameRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = Hands.process(frameRGB)
    handPoints = results.multi_hand_landmarks
    h, w, _ = img.shape
    pontos = []

    if handPoints:
        for points in handPoints:
            mpDraw.draw_landmarks(img, points, hands.HAND_CONNECTIONS)

            for id, cord in enumerate(points.landmark):
                cx, cy = int(cord.x * w), int(cord.y * h)
                pontos.append((cx, cy))

            dedos = [8, 12, 16, 20]
            contador = 0

            if pontos:
                if pontos[4][0] < pontos[3][0]:
                    contador += 1
                for x in dedos:
                    if pontos[x][1] < pontos[x - 2][1]:
                        contador += 1

            cv2.rectangle(img, (500, 10), (580, 110), (255, 0, 0), -1)
            cv2.putText(img, str(contador), (500, 100), cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 255, 255), 5)

            # Lógica para pressionar teclas apenas quando a contagem muda
            if contador != estado_anterior:
                if contador == 0:
                    keyboard.press('down')
                elif contador == 5:
                    keyboard.press_and_release('up')
                else:
                    keyboard.release('up')
                    keyboard.release('down')

                # Atualiza o estado anterior
                estado_anterior = contador

    cv2.imshow('Imagem', img)
    cv2.waitKey(1)
