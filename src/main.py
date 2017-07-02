# This Python file uses the following encoding: utf-8

from func_correcao import *
import cv2
from matplotlib import pyplot as plt
import numpy as np
from question_recognition import *


if __name__ == '__main__':
    img_prova = cv2.imread('../img/scan/SoMarcacoes2.png', cv2.IMREAD_GRAYSCALE)
    img_prova = cv2.threshold(img_prova, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    cv2.imshow('questao', img_prova)
    cv2.waitKey(0)
    qimgs = split_questions(img_prova)
    questions = [QuestionImg(q) for q in qimgs]
    answers = [q.evaluate() for q in questions]
    print(answers)