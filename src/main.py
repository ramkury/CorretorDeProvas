# This Python file uses the following encoding: utf-8

from func_correcao import *
import cv2
from matplotlib import pyplot as plt
import numpy as np
from question_recognition import *


def main():
    marcador_questao = cv2.imread('../img/marcacao_resposta.png', cv2.IMREAD_GRAYSCALE)
    marcador_questao = cv2.threshold(marcador_questao, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    prova = []
    prova.append(cv2.imread('../img/p1_1.png', cv2.IMREAD_GRAYSCALE))
    prova.append(cv2.imread('../img/p1_2.png', cv2.IMREAD_GRAYSCALE))
    prova.append(cv2.imread('../img/p1_3.png', cv2.IMREAD_GRAYSCALE))
    prova = np.concatenate(prova)
    rows, cols = prova.shape

    # Imagem binarizada negativa
    prova_bin = cv2.threshold(prova, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    # Isola linhas
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (int(0.95 * cols), 1)) * 255
    prova_linhas = cv2.erode(prova_bin, kernel)

    questoes = split_questions(prova_bin, prova_linhas)
    for n, q in enumerate(questoes):
        cv2.imwrite(('../res/q%d.png' % (1+n)), q)

    cv2.imwrite('../img/linhas.png', prova_linhas)
    # plt.imshow(prova, cmap='gray', interpolation='bilinear')
    # plt.show()
    # cv2.waitKey(0)

if __name__ == '__main__':
    # main()
    img_prova = cv2.imread('../img/teste-circulo.png', cv2.IMREAD_GRAYSCALE)
    img_prova = cv2.threshold(img_prova, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    cv2.imshow('questao', img_prova)
    cv2.waitKey(0)
    qimgs = split_questions(img_prova)
    questions = [QuestionImg(q) for q in qimgs]
    print([m.centroid for m in questions[0].markers])