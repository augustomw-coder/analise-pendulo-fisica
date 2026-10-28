# APS de Física - Oscilador Harmónico Amortecido (OHA)

Trabalho prático de rastreamento de movimento por visão computacional e análise do modelo teórico de um pêndulo simples amortecido.

## 📌 Parâmetros do Experimento
- **Massa (m):** 0,215 kg (215 g)
- **Comprimento (l):** 0,60 m (60 cm)
- **Frequência Teórica (w):** 4,044 rad/s

## 📊 Resultados Obtidos
- **Frequência Angular Experimental (w):** 3,855 rad/s (Erro de 4,66%)
- **Constante de Amortecimento (b):** 0,00141 kg/s
- **Fator de Qualidade (Q):** 588,2

## 🚀 Ficheiros do Repositório
- `1_rastreamento.py`: Script OpenCV para extração de posições (t, x, y)
- `2_analise_oha.py`: Script para ajuste de curva teórico e gráfico do OHA
- `dados_pendulo.csv`: Dados brutos obtidos no rastreamento
- `grafico_oha.png`: Gráfico final do movimento ajustado
