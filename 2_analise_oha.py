import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# 1. Carregar dados
try:
    df = pd.read_csv("dados_pendulo.csv")
except FileNotFoundError:
    print("Erro: O ficheiro 'dados_pendulo.csv' não foi encontrado!")
    exit()

# 2. Filtrar o início do vídeo para pegar apenas a oscilação livre (a partir de t = 8.0s)
df_livre = df[df["t"] >= 8.0].copy()

# Normalizar o tempo para começar em t = 0s no instante da soltura
t = df_livre["t"].values - df_livre["t"].values[0]
x = df_livre["x"].values

# Parâmetros físicos fornecidos
m = 0.215  # kg
l = 0.60   # m
g = 9.81   # m/s^2

# 3. Modelo Teórico do Oscilador Harmónico Amortecido (OHA)
def oha_model(t, A, gamma, omega, phi, x0):
    return A * np.exp(-gamma * t) * np.cos(omega * t + phi) + x0

# Estimativas iniciais dos parâmetros
x0_est = np.mean(x)
A_est = (np.max(x) - np.min(x)) / 2.0
gamma_est = 0.005
omega_est = np.sqrt(g / l)  # approx 4.04 rad/s
phi_est = 0.0

p0 = [A_est, gamma_est, omega_est, phi_est, x0_est]

# 4. Ajuste de Curva Não-Linear
popt, _ = curve_fit(oha_model, t, x, p0=p0)
A, gamma, omega, phi, x0 = popt

# 5. Cálculos Físicos
b = 2 * m * gamma          # Coeficiente de amortecimento
Q = omega / (2 * gamma)    # Fator de Qualidade
omega_0_teorico = np.sqrt(g / l) # Frequência teórica do pêndulo simples
erro_frequencia = abs(omega - omega_0_teorico) / omega_0_teorico * 100

print("\n==================================================")
print("       RESULTADOS DA ANÁLISE FÍSICA (APS)        ")
print("==================================================")
print(f" Amplitude inicial (A):             {abs(A):.2f} px")
print(f" Posição de equilíbrio (x0):         {x0:.2f} px")
print(f" Taxa de atenuação (gamma):          {gamma:.5f} s^-1")
print(f" Constante de amortecimento (b):    {b:.6f} kg/s")
print(f" Frequência angular exp. (omega):   {omega:.3f} rad/s")
print(f" Frequência angular teórica (w0):   {omega_0_teorico:.3f} rad/s")
print(f" Erro relativo na frequência:        {erro_frequencia:.2f}%")
print(f" Fase inicial (phi):                 {phi:.3f} rad")
print(f" Fator de Qualidade (Q):             {Q:.1f}")
print("==================================================\n")

# 6. Gráfico de Comparação: Dados vs. Ajuste Teórico
plt.figure(figsize=(12, 5))
plt.scatter(t, x, color='red', s=6, alpha=0.4, label='Dados OpenCV (Extraídos do Vídeo)')
plt.plot(t, oha_model(t, *popt), color='blue', linewidth=2, label=f'Ajuste Teórico OHA (Q = {Q:.1f})')
plt.title('Oscilação Harmónica Amortecida do Pêndulo Simples', fontsize=14)
plt.xlabel('Tempo de Oscilação Livre t (s)', fontsize=12)
plt.ylabel('Posição X (pixels)', fontsize=12)
plt.legend(fontsize=11)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()