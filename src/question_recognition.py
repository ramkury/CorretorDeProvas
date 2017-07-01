import cv2
import numpy as np
import operator


pi = 3.14159


def split_questions(image, lines=None):
    rows, cols = image.shape
    if lines is None:
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (int(0.95 * cols), 1)) * 255
        lines = cv2.erode(image, kernel)
    questions = []
    mid = cols // 2
    state = 0
    for i, elem in enumerate(lines[:, mid]):
        if state == 0:  # espaco entre questoes
            if elem > 0:
                state = 1
        elif state == 1:  # linha de inicio da questao
            if elem == 0:
                qstart = i
                state = 2
        elif state == 2:  # conteudo da questao
            if elem > 0:
                questions.append(image[qstart:i - 1, :])
                state = 3
        elif state == 3:  # linha de final de questao
            if elem == 0:
                state = 0

    return questions


class Marker:
    def __init__(self, centroid, stats):
        self.centroid = centroid
        self.stats = stats

    def draw(self, image, color):
        cv2.circle(image, self.centroid, self.stats[cv2.CC_STAT_AREA/(2*pi)], color)

    def x(self):
        return self.centroid[0]

    def y(self):
        return self.centroid[1]


class AnswerArea:
    def __init__(self, img):
        self.img = img
        self.area = img.shape[0] * img.shape[1]

    def measure(self):
        return 1.0 - (float(np.count_nonzero(self.img[:, :])) / self.area)

    def evaluate(self, percentage):
        return self.measure() > percentage


class QuestionImg:
    def __init__(self, img_bin):
        self.img_bin = img_bin
        self.markers = []
        self.find_markers()
        self.answer_blocks = []

    def find_markers(self):
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10))
        eroded = cv2.erode(self.img_bin, kernel)
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
        half_height = self.markers[1].centroids[1] - self.markers[0].centroids[1]
        y_center = (self.markers[0].centroids[1] + self.markers[-1].centroids[1]) // 2
        ybegin, yend = y_center - half_height, y_center + half_height

        for i in range(1, len(self.markers) - 1):
            xcenter = self.markers[i][0]
            xbegin = self.markers[i-1].centroid[0] + xcenter // 2
            xend = self.markers[i+1].centroids[0] + xcenter // 2
            self.answer_blocks.append(AnswerArea(self.img_bin[ybegin:yend, xbegin:xend]))