import cv2
import numpy as np
from random import randrange as rr
import operator


pi = 3.14159


def split_questions(image, lines=None):
    rows, cols = image.shape
    if lines is None:
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (int(0.95 * cols), 1)) # * 255
        lines = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
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
                questions.append(image[qstart:i - 10, :])
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
        cv2.circle(image, int_centroid, int(self.stats[cv2.CC_STAT_AREA]/(2*pi)), color, thickness=3)


class AnswerArea:
    checked_threshold = 0.5

    def __init__(self, xstart, xend, ystart, yend, image):
        self.xstart = xstart
        self.xend = xend
        self.ystart = ystart
        self.yend = yend
        self.img_flat = image[ystart:yend, xstart:xend].flatten()

    def measure(self):
        return float(np.count_nonzero(self.img_flat)) / len(self.img_flat)

    def is_checked(self):
        return self.measure() >= self.checked_threshold

    def draw(self, image, color):
        c = (rr(256), rr(256), rr(256))
        cv2.rectangle(image, (self.xstart, self.ystart), (self.xend, self.yend), c, thickness=2)
        print("BoxValue: %f" % self.measure())


class QuestionImg:
    def __init__(self, img_bin):
        self.img_bin = img_bin
        self.markers = []
        self.find_markers()
        self.answer_blocks = []
        self.find_answer_blocks()

    def find_markers(self):
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10))
        eroded = cv2.morphologyEx(self.img_bin, cv2.MORPH_ERODE, kernel)
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

        for i in range(1, len(self.markers) - 1):
            xcenter = self.markers[i].centroid[0]
            xbegin = int((self.markers[i-1].centroid[0] + xcenter) // 2)
            xend = int((self.markers[i+1].centroid[0] + xcenter) // 2)
            self.answer_blocks.append(AnswerArea(xbegin, xend, ybegin, yend, self.img_bin))

    def show(self):
        img_bgr = cv2.cvtColor(self.img_bin, cv2.COLOR_GRAY2BGR)
        for ab in self.answer_blocks:
            ab.draw(img_bgr, (255, 0, 0))
        for m in self.markers:
            m.draw(img_bgr, (0, 255, 0))
        cv2.imshow('areas', img_bgr)
        cv2.waitKey(0)

    def evaluate(self):
        return [i for i, a in enumerate(self.answer_blocks) if a.is_checked()]
