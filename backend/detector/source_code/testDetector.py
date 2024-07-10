import cv2
import numpy as np


def show(text, image):
    cv2.imshow(text, image)
    cv2.waitKey(0)


def remove_shadow(image):
    rgb_planes = cv2.split(image)

    result_planes = []
    result_norm_planes = []
    for plane in rgb_planes:
        dilate_img = cv2.dilate(plane, np.ones((7, 7), np.uint8))
        bg_img = cv2.medianBlur(dilate_img, 21)
        diff_img = 255 - cv2.absdiff(plane,
                                     bg_img)
        norm_img = cv2.normalize(diff_img, None, 0, 255,
                                 cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
        result_planes.append(diff_img)
        result_norm_planes.append(norm_img)

    result = cv2.merge(result_planes)
    result_norm = cv2.merge(result_norm_planes)
    return result, result_norm


def image_processing(image):
    img, _ = remove_shadow(image)
    blurred = cv2.GaussianBlur(img, (5, 5), 0)
    edged = cv2.Canny(blurred, 50, 190)
    _, thresh = cv2.threshold(
        edged, 50, 255, cv2.THRESH_BINARY_INV)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
    close = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel, iterations=1)
    mask = cv2.morphologyEx(close, cv2.MORPH_OPEN, kernel, iterations=1)
    show('mask', mask)
    return thresh, edged, close


def get_contour(image):
    _, _, img = image_processing(image)
    contours, hierarchy = cv2.findContours(
        img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    return contours, hierarchy, img


def draw_contour_(contours, image):
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)

        if len(approx) >= 4:
            x, y, w, hh = cv2.boundingRect(cnt)
            M = cv2.moments(cnt)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            cv2.drawContours(image, [cnt], 0, (0, 0, 255), -1)
            # cv2.putText(image, "Rectangle", (cx-50, cy),
            #           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)
    return image


def draw_contour(contours, image):
    max_area = 0
    max_box = None

    for i, cnt in enumerate(contours):
        if cv2.contourArea(cnt) <= 1000:
            continue
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)

        area = int(abs((box[2][0] - box[0][0]) * (box[2][1] - box[0][1])))
        cv2.drawContours(image, [box.astype(int)], 0, (0, 0, 255), 2)

    return image


image_ = cv2.imread('./images/13_Color.png')
image = image_.copy()


show("e", image)
contours, _, img = get_contour(image)
show('a', img)
contours = sorted(contours, key=cv2.contourArea,
                  reverse=False)[:len(contours)-1]
show('res', draw_contour_(contours, image))
