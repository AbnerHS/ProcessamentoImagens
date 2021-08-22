import numpy as np
from PIL import Image
from numpy import asarray
import matplotlib.pyplot as plt

def filtroMediana(img,m,n):
    for x in range(1, m - 2):
        for y in range(1, n - 2):
            w = img[x - 1:x + 2, y - 1:y + 2]
            img[x, y] = np.median(w).astype(int)
    return img

def instantiate_histogram():
    hist_array = []
    for i in range(0, 256):
        hist_array.append(str(i))
        hist_array.append(0)
    hist_dct = {hist_array[i]: hist_array[i + 1] for i in range(0, len(hist_array), 2)}
    return hist_dct

def count_intensity_values(hist, img):
    for row in img:
        for column in row:
            hist[str(int(column))] = hist[str(int(column))] + 1
    return hist

def plot_hist(hist, hist2=''):
    if hist2 != '':
        figure, axarr = plt.subplots(1,2, figsize=(20, 10))
        axarr[0].bar(hist.keys(), hist.values())
        axarr[1].bar(hist2.keys(), hist2.values())
    else:
        plt.bar(hist.keys(), hist.values())
        plt.xlabel("Níveis intensidade")
        ax = plt.gca()
        ax.axes.xaxis.set_ticks([])
        plt.grid(True)
        plt.show()

def get_hist_proba(hist, n_pixels):
    hist_proba = {}
    for i in range(0, 256):
        hist_proba[str(i)] = hist[str(i)] / n_pixels
    return hist_proba

def get_accumulated_proba(hist_proba):
    acc_proba = {}
    sum_proba = 0
    for i in range(0, 256):
        if i == 0:
            pass
        else:
            sum_proba += hist_proba[str(i - 1)]
        acc_proba[str(i)] = hist_proba[str(i)] + sum_proba
    return acc_proba

def get_new_gray_value(acc_proba):
    new_gray_value = {}
    for i in range(0, 256):
        new_gray_value[str(i)] = np.ceil(acc_proba[str(i)] * 255)
    return new_gray_value

def equalize_hist(img, new_gray_value):
    for row in range(img.shape[0]):
        for column in range(img.shape[1]):
            img[row][column] = new_gray_value[str(int(img[row][column]))]
    return img

def main():
    image = Image.open('enhance-me.gif')
    npImage = np.array(image)
    m = npImage.shape[0]  # qtd lines
    n = npImage.shape[1]  # qtd cols
    #criar histograma da imagem
    histogram = instantiate_histogram()
    #contar qtd de vezes cada pixel (intensidade) aparece na imagem
    histogram = count_intensity_values(histogram, npImage)
    n_pixels = m * n    #qtd pixels
    #calcular probabilidade de pixel aparecer (qtd de vezes que aparece / total de pixeis)
    hist_proba = get_hist_proba(histogram, n_pixels)
    #calcular  a probabilidade acumulada (soma cada valor do hist a cada probabilidade)
    accumulated_proba = get_accumulated_proba(hist_proba)
    #calcular novos valores de cinza da imagem
    new_gray_value = get_new_gray_value(accumulated_proba)
    #aplicar os novos valores na imagem original
    eq_img = equalize_hist(npImage.copy(), new_gray_value)

    #criar histograma da imagem equalizada
    histogram1 = instantiate_histogram()
    histogram1 = count_intensity_values(histogram1, eq_img)
    #plotar histogramas
    plot_hist(histogram,histogram1)
    #aplicar filtro mediana
    imgFinal = filtroMediana(eq_img.copy(), m, n)
    #plotar imagem original, equalizada, equalizada+filtrada
    figure, axarr = plt.subplots(1, 3, figsize=(20, 10))
    axarr[0].imshow(npImage, cmap='gray')
    axarr[1].imshow(eq_img, cmap='gray')
    axarr[2].imshow(imgFinal, cmap='gray')
    plt.show()
    imgFinal = Image.fromarray(imgFinal)
    imgFinal.save("enhanced.gif")

if __name__ == "__main__":
    main()