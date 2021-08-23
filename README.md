![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![OpenCV](https://img.shields.io/badge/opencv-%23white.svg?style=for-the-badge&logo=opencv&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)


# Projeto-Sinais-e-Sistemas

Detecção de imagens borradas usando FFT e filtro passa-alta.

## Objetivo

O objetivo desse projeto é a identificação de imagens borradas.

## Metodologia

Para tal, nós aplicamos um filtro passa-alta para a identificação dos contornos e bordas da imagem. Determinamos se a imagem está borrada baseado na quantidade e intensidade de pixels ativados na imagem resultante. Se a imagem resultante está muito apagada, a imagem original deve estar borrada.

O filtro passa-alta depende de uma frequência de corte omega_c, e a imagem resultante é considerada muito apagada se a média da intensidade de seus pixels for abaixo de um valor de corte B_c.

Para determinar essas constantes, nós testamos com o banco de imagens disponibilizado, buscando encontrar um omega_c e B_c que permita a maior separação dos casos disponíveis. Esse teste pode ser feito usando essa ferramenta caso deseje-se encontrar diferentes valores dos que sugerimos.

## Uso

Para testar se uma única imagem pode ser consideda borrada, o programa pode ser rodado como exemplificado a seguir:

```
python main.py single -i <caminho para a imagem> -t <omega_c> [-m rectangular|circular] [-v] [-s]
```

onde

1. `-m`/`--mask-generator` indica o tipo de máscara que deve ser usada para o filtro passa alta.
2. `v`/`--visualize` se for desejado que uma imagem intermediária seja gerada mostrando o processo até a geração da imagem reconstruída pela ifft
3. `s`/`--save-reconstructed` para salvar a imagem reconstruída (a depender do valor de omega, o resultado pode ser uma imagem com mais contraste e mais legível)

Nesse uso, o programa resulta num booleano que informa se a imagem foi considerada como borrada ou não.

Para rodar a sequência de testes com várias imagens e para diferentes valores de omega, o programa pode ser rodado como a seguir:

```
python main.py batch -f <caminho para a pasta contendo imagens> -t <lista de omega_c separados por linha> [-m rectangular|circular] [-v] [-s]
```

As imagens devem seguir o padrão de nomeação tal que se a imagem for nítida pode ter um nome qualquer que não possua hífen (-). Se a imagem for borrada, pode ter seu nome qualquer e deve acabar com "-blur".

O resultado desse programa será um arquivo `.csv` com o seguinte cabeçalho:

|  | name | is_image_blur | wc=<omega_c1> | wc=<omega_c2> | ... | wc=<omega_cN> |
|:--- | ---|---|---|---|---|---|

Onde

1. **name** é o nome do arquivo de cada imagem
2. **is_image_blur** é se a imagem está etiquetada como borrada ou não
3. **wc=<omega_ci>** é a média das intensidades dos pixels da imagem quando é usado o valor i dos omega_cs passados para o programa


Esse projeto será melhor apreciado com essa música: [![YouTube Music](https://img.shields.io/badge/YouTube_Music-FF0000?style=for-the-badge&logo=youtube-music&logoColor=white)](https://www.youtube.com/watch?v=68ugkg9RePc&ab_channel=BlissCorporation)

