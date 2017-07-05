import cv2
import numpy as np
from random import randrange as rr
import operator


def split_questions(img_bin, img_gray, lines=None, line_width=0.95):
    rows, cols = img_bin.shape
    if lines is None:
        # Engrossar linhas do separador de questao para tolerancia a rotacoes leves
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 5))
        lines = cv2.morphologyEx(img_bin, cv2.MORPH_DILATE, kernel)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (int(line_width * cols), 1))  # * 255
        lines = cv2.morphologyEx(lines, cv2.MORPH_OPEN, kernel)
    questions = []
    mid = cols // 2
    state = 0
    midcol = lines[:, mid]
    i = 0
    while i < rows:
        if state == 0:  # espaco entre questoes
            if midcol[i] > 0:
                state = 1
        elif state == 1:  # linha de inicio da questao
            if midcol[i] == 0:
                i += 10
                qstart = i
                state = 2
        elif state == 2:  # conteudo da questao
            if midcol[i] > 0:
                questions.append(QuestionImg(img_bin[qstart:i - 10, :], img_gray[qstart:i - 10, :]))
                # cv2.imshow('questao', img_bin[qstart:i - 10, :])
                # cv2.waitKey(0)
                state = 3
        elif state == 3:  # linha de final de questao
            if midcol[i] == 0:
                state = 0
        i += 1

    return questions


class Marker:
    def __init__(self, centroid, stats):
        self.centroid = centroid
        self.stats = stats

    def draw(self, image, color):
        int_centroid = int(self.centroid[0]), int(self.centroid[1])
        cv2.circle(image, int_centroid, int(self.stats[cv2.CC_STAT_AREA]/(2*np.pi)), color, thickness=3)


class AnswerArea:
    checked_threshold = 0.11
    margin_h = 6
    margin_v = 3
    color_unchecked = (139, 227, 24)  # verde
    color_checked = (66, 106, 255)  # coral

    def __init__(self, xstart, xend, ystart, yend, image):
        self.xstart = xstart + self.margin_h
        self.xend = xend - self.margin_h
        self.ystart = ystart + self.margin_v
        self.yend = yend - self.margin_v
        self.img_flat = image[self.ystart:self.yend, self.xstart:self.xend].flatten()
        self.checked = self.measure() >= self.checked_threshold

    def measure(self):
        return 1.0 - (np.sum(self.img_flat) / (len(self.img_flat) * 255.0))

    def draw(self, image):
        c = self.color_checked if self.checked else self.color_unchecked
        cv2.rectangle(image, (self.xstart, self.ystart), (self.xend, self.yend), c, thickness=2)
        # print("BoxValue: %f" % self.measure())


class QuestionImg:
    def __init__(self, img_bin, img_gray):
        self.img_bin = img_bin
        self.img_gray = img_gray
        self.markers = []
        self.find_markers()
        self.answer_blocks = []
        self.find_answer_blocks()

    def find_markers(self):
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        eroded = cv2.dilate(self.img_bin, kernel)  # fecha possiveis buracos nos marcadores
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10))
        eroded = cv2.morphologyEx(eroded, cv2.MORPH_ERODE, kernel)
        n_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(eroded, connectivity=8)
        all_markers = [Marker(c, stats[i]) for i, c in enumerate(centroids)]
        # remove marcador do plano de fundo
        max_area, inx = -1, -1
        for i, m in enumerate(all_markers):
            current_area = m.stats[cv2.CC_STAT_AREA]
            if current_area > max_area:
                max_area = current_area
                inx = i
        all_markers.pop(inx)

        m_xmin = min(all_markers, key=lambda m: m.centroid[0])
        m_xmax = max(all_markers, key=lambda m: m.centroid[0])
        ymin = m_xmin.centroid[1] + 13
        self.markers.append(m_xmin)
        for m in all_markers:
            if m.centroid[1] >= ymin:
                self.markers.append(m)
        self.markers.append(m_xmax)

    def find_answer_blocks(self):
        self.markers.sort(key=lambda m: m.centroid[0])
        half_height = (self.markers[1].centroid[1] - self.markers[0].centroid[1]) / 2.0
        y_center = (self.markers[0].centroid[1] + self.markers[-1].centroid[1]) / 2.0
        ybegin = int(y_center - half_height)
        yend = int(y_center + half_height)
        # interpolacao linear para tolerancia a pequenas rotacoes
        xbase, ybase = self.markers[0].centroid
        m = (self.markers[-1].centroid[1] - ybase) / (self.markers[-1].centroid[0] - xbase)
        for i in range(1, len(self.markers) - 1):
            xcenter = self.markers[i].centroid[0]
            xbegin = int((self.markers[i-1].centroid[0] + xcenter) // 2)
            xend = int((self.markers[i+1].centroid[0] + xcenter) // 2)
            # interpolacao linear
            deltax = xcenter - xbase
            deltay = int(np.round(m * deltax))
            self.answer_blocks.append(AnswerArea(xbegin, xend, ybegin + deltay, yend + deltay, self.img_gray))

    def show(self):
        cv2.imshow('areas', self.marked_image())
        cv2.waitKey(0)

    def marked_image(self):
        img_bgr = cv2.cvtColor(self.img_gray, cv2.COLOR_GRAY2BGR)
        for ab in self.answer_blocks:
            ab.draw(img_bgr)
        for m in self.markers:
            m.draw(img_bgr, (222, 204, 32))
        return img_bgr

    def evaluate(self):
        return [i for i, a in enumerate(self.answer_blocks) if a.checked]
