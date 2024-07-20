import cv2
import numpy as np
import json
from math import sqrt
import os


class ImageDetector:
    def __init__(self, path, text='orig img', min_area=2000, max_area=50000):
        self.image = cv2.imread(path)
        self.min_area = min_area
        self.max_area = max_area
        self.text = text
        self.boxes = []

    def run(self):
        self.remove_shadow()
        self.image_processing()
        self.get_contour()
        self.draw_contour()
        # self.show('res')
        result = (self.create_json())
        return result

    def show(self, text=None, image=None):
        if text is None:
            text = self.text
        if image is None:
            image = self.image
        cv2.imshow(text, image)
        cv2.waitKey(0)

    def remove_shadow(self):
        rgb_planes = cv2.split(self.image)
        result_planes = []
        result_norm_planes = []
        for plane in rgb_planes:
            dilate_img = cv2.dilate(plane, np.ones((6, 6), np.uint8))
            bg_img = cv2.medianBlur(dilate_img, 21)
            diff_img = 255 - cv2.absdiff(plane,
                                         bg_img)
            norm_img = cv2.normalize(diff_img, None, 1, 255,
                                     cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
            result_planes.append(diff_img)
            result_norm_planes.append(norm_img)

        self.img_without_shadow = cv2.merge(result_planes)
        self.img_norm = cv2.merge(result_norm_planes)

    def image_processing(self):
        self.edged = cv2.Canny(self.img_without_shadow, 50, 150)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        self.img_after_morph = cv2.morphologyEx(
            self.edged, cv2.MORPH_CLOSE, kernel, iterations=1)

    def get_contour(self, img_type='morph'):
        match img_type:
            case 'morph':
                img = self.img_after_morph
            case 'norm':
                img = self.img_norm
            case 'edged':
                img = self.edged
            case _:
                img = self.img_after_morph

        self.contours, self.hierarchy = cv2.findContours(
            img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    def draw_contour(self):
        self.contours = sorted(self.contours,
                               key=cv2.contourArea, reverse=False)[:len(self.contours)-1]
        for cnt in self.contours:
            area = cv2.contourArea(cnt)
            if area < self.min_area or area > self.max_area:
                continue
            rect = cv2.minAreaRect(cnt)
            x, y, w, h = cv2.boundingRect(cnt)
            box1 = cv2.boxPoints(rect)
            p1 = (x, y+h)
            p2 = (x, y)
            p3 = (x+w, y)
            p4 = (x+w, y+h)
            c = 50
            if self.dist(p1, (box1[0])) < c and self.dist(p2, (box1[1])) < c and self.dist(p3, (box1[2])) < c and self.dist(p4, (box1[3])) < c:

                # box = cv2.rectangle(self.image, (x, y),
                #                   (x+w, y+h), (0, 255, 0), 2)
                cv2.drawContours(
                    self.image, [box1.astype(int)], 0, (0, 0, 255), 2)
                self.boxes.append(box1)

    def save_result(self, filename):
        cv2.imwrite(filename, self.image)

    def create_json(self):
        output = {}
        for id, box in enumerate(self.boxes):
            output[id] = {
                "x1": float(box[0][0]), "y1": float(box[0][1]),
                "x2": float(box[1][0]), "y2": float(box[1][1]),
                "x3": float(box[2][0]), "y3": float(box[2][1]),
                "x4": float(box[3][0]), "y4": float(box[3][1])
            }
        filename = "output/output.json"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "a+") as file:
            json.dump(output, file)
        return (output)

    def dist(self, p1, p2):
        return sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
