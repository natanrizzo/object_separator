# Orientações sobre o trabalho

Para a coleta de pontos para o KMeans deve enviar dois arrays
- Um com as cores dos pixels. Array de Array
- Outro com a classe (fundo ou objeto). Array
---
Durante o processamento da imagem, envia o valor da cor do pixel, predict com o KMeans.
Se fundo:
- Dois arquivos, no do objeto, pinta de preto, no do fundo deixa a cor do pixel.

Se objeto:
- Dois arquivos, no do objecto, pinta a cor do pixel, no do fundo pinta de preto.