# This Python file uses the following encoding: utf-8

from func_correcao import *
import cv2
from matplotlib import pyplot as plt
import numpy as np
from question_recognition import *


if __name__ == '__main__':
    # img_prova = cv2.imread('../img/scan/SoMarcacoes2.png', cv2.IMREAD_GRAYSCALE)
    img_prova = cv2.imread('../img/scan/Folhas gabarito-4.png', cv2.IMREAD_GRAYSCALE)
    # img_prova = cv2.imread('../img/scan/mult5.jpg', cv2.IMREAD_GRAYSCALE)
    img_prova_bin = cv2.threshold(img_prova, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    questions = split_questions(img_prova_bin, img_prova, line_width=0.95)
    for i, q in enumerate(questions):
        cv2.imwrite('../res/res%d.png' % (i+1), q.marked_image())
        q.show()
    answers = [q.evaluate() for q in questions]
    print(answers)
