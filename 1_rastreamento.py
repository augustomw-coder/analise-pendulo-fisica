import cv2
import numpy as np
import pandas as pd

# Nome do ficheiro de vídeo (ajuste a extensão se for .mov ou .mp4)
video_path = "pendulo.mp4" 
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print(f"Erro ao abrir o vídeo: {video_path}. Verifique o nome/extensão na pasta!")
    exit()

fps = cap.get(cv2.CAP_PROP_FPS)
dt = 1.0 / fps if (fps and fps > 0) else 1.0 / 30.0

dados = []
frame_idx = 0

print("A processar o vídeo... Pressione 'q' para interromper.")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    height, width = frame.shape[:2]

    # 1. Cortar o chão: analisa apenas até 70% da altura da imagem (ignora o piso)
    roi = frame[0:int(height * 0.70), :]

    # 2. Converter para escala de cinzento
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    # 3. Limiar de brilho para isolar a esfera branca
    _, mask = cv2.threshold(gray, 170, 255, cv2.THRESH_BINARY)

    # 4. Limpeza de ruído
    mask = cv2.GaussianBlur(mask, (5, 5), 0)
    mask = cv2.erode(mask, None, iterations=1)
    mask = cv2.dilate(mask, None, iterations=2)

    # 5. Detetar contornos dentro da ROI
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Seleciona o maior objeto claro na região do pêndulo
        c = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)

        if radius > 6:
            t = frame_idx * dt
            dados.append([t, x, y])

            # Desenha a marcação verde no vídeo
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 0), 2)

    # Mostrar janelas de visualização
    cv2.imshow("Rastreamento - Pendulo", frame)
    cv2.imshow("Mascara de Detecao (Sem Chao)", mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    frame_idx += 1

cap.release()
cv2.destroyAllWindows()

# Guardar posições obtidas
df = pd.DataFrame(dados, columns=["t", "x", "y"])
df.to_csv("dados_pendulo.csv", index=False)

print(f"\nProcessamento concluído! Foram capturados {len(dados)} pontos.")
if len(dados) > 0:
    print(f"Variação da posição X obtida: min = {df['x'].min():.1f} px | max = {df['x'].max():.1f} px")