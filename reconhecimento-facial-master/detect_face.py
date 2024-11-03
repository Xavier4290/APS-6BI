import cv2
import os
import numpy as np
import shutil

# Caminho Haarcascade
cascPath = 'cascade/haarcascade_frontalface_default.xml'
cascPathOlho = 'cascade/haarcascade-eye.xml'

# Classificador baseado nos haarcascades
facePath = cv2.CascadeClassifier(cascPath)
facePathOlho = cv2.CascadeClassifier(cascPathOlho)
video_capture = cv2.VideoCapture(0)

# Caminho do arquivo que queremos mover
arquivo = 'pessoa.jpg'

# Verifica se a pasta 'fotos' já existe, se não, cria a pasta
pasta_destino = 'fotos'
if not os.path.exists(pasta_destino):
    os.mkdir(pasta_destino)

# Verifica se o arquivo existe antes de mover
if os.path.exists(arquivo):
    shutil.move(arquivo, os.path.join(pasta_destino, arquivo))
    print(f"Imagem '{arquivo}' foi movida para a pasta '{pasta_destino}'.")
else:
    print(f"Arquivo '{arquivo}' não encontrado.")

increment = 1
numMostras = 50
id = int(input("Digite o número do ID: "))
width, height = 220, 220
print('Capturando as faces...')

while True:
    conect, image = video_capture.read()
    if not conect:
        print("Erro ao capturar imagem.")
        break

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Qualidade da luz sobre a imagem capturada
    print(np.average(gray))

    # Realizando face detect
    face_detect = facePath.detectMultiScale(
        gray,
        scaleFactor=1.5,
        minSize=(35, 35),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

 
    for (x, y, w, h) in face_detect:
        # Desenhando retângulo na face detectada
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        
        # Condição: Captura a foto automaticamente quando o retângulo for desenhado
        face_off = cv2.resize(gray[y:y + h, x:x + w], (width, height))
        cv2.imwrite(f'fotos/pessoa.{id}.{increment}.jpg', face_off)
        print(f'[Foto capturada com sucesso] - ', np.average(gray))
        increment += 1

        # Realizando detecção do olho da face
        region = image[y:y + h, x:x + w]
        imageOlhoGray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
        face_detect_olho = facePathOlho.detectMultiScale(imageOlhoGray)
          
        for (ox, oy, ow, oh) in face_detect_olho:
            # Desenhando retângulo nos olhos detectados
            cv2.rectangle(region, (ox, oy), (ox + ow, oy + oh), (0, 0, 255), 2)
            face_off = cv2.resize(gray[y:y + h, x:x + w], (width, height))
            cv2.imwrite(f'fotos/pessoa.{id}.{increment}.jpg', face_off)

            print(f'[Foto capturada com sucesso] - ', np.average(gray))
            increment += 1
            # id += 1

            # Parar o loop caso tenhamos capturado o número desejado de imagens
            if increment > numMostras:
                break
        if increment > numMostras:
            break
    if increment > numMostras:
        break

    # Incrementa o ID para cada nova pessoa detectada
    #  id += 1

    cv2.imshow('Face', image)
    cv2.waitKey(1)


print('Fotos capturadas com sucesso :)')
video_capture.release()
cv2.destroyAllWindows()
