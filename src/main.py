# This Python file uses the following encoding: utf-8

from func_correcao import *
import cv2
from matplotlib import pyplot as plt
import numpy as np
from question_recognition import *


if __name__ == '__main__':
    # img_prova = cv2.imread('../img/scan/SoMarcacoes2.png', cv2.IMREAD_GRAYSCALE)
    img_prova = cv2.imread('../img/scan/Folhas gabarito-2.png', cv2.IMREAD_GRAYSCALE)
    # img_prova = cv2.imread('../img/scan/foto1.png', cv2.IMREAD_GRAYSCALE)
    img_prova_bin = cv2.threshold(img_prova, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    questions = split_questions(img_prova_bin, img_prova, line_width=0.95)
    # for i, q in enumerate(questions):
    #     img = q.marked_image()
    #     cv2.imwrite('../res/analog_questao%d.png' % (i+1), img)
    #####################
    # for i, q in enumerate(questions):
    #     print('Questao %d' % (i+1))
    #     q.show()
    for q in questions:
        q.show()
    answers = [q.evaluate() for q in questions]
    print(answers)
