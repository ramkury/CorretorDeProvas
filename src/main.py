import cv2
from matplotlib import pyplot as plt
import numpy as np


def split_questions(original, lines):
    rows, cols = original.shape
    questions = []
    mid = cols // 2
    state = 0
    for i in xrange(rows):
        elem = lines[i, mid]
        if state == 0:  # espaco entre questoes
            if elem > 0:
                state = 1
        elif state == 1:  # linha de inicio da questao
            if elem == 0:
                qstart = i
                state = 2
        elif state == 2:  # conteudo da questao
            if elem > 0:
                questions.append(original[qstart:i-1, :])
                state = 3
        elif state == 3:  # linha de final de questao
            if elem == 0:
                state = 0

    return questions


def main():
    prova = []
    prova.append(cv2.imread('../img/p1_1.png', cv2.IMREAD_GRAYSCALE))
    prova.append(cv2.imread('../img/p1_2.png', cv2.IMREAD_GRAYSCALE))
    prova.append(cv2.imread('../img/p1_3.png', cv2.IMREAD_GRAYSCALE))
    prova = np.concatenate(prova)

    # Imagem binarizada negativa
    prova_linhas = cv2.threshold(prova, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    rows, cols = prova.shape

    # Isola linhas
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (int(0.95 * cols), 1)) * 255
    prova_linhas = cv2.erode(prova_linhas, kernel)

    questoes = split_questions(prova, prova_linhas)
    for n, q in enumerate(questoes):
        cv2.imwrite(('../res/q%d.png' % (1+n)), q)

    cv2.imwrite('../img/linhas.png', prova_linhas)
    # plt.imshow(prova, cmap='gray', interpolation='bilinear')
    # plt.show()
    # cv2.waitKey(0)

if __name__ == '__main__':
    main()
