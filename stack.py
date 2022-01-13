import cv2
import numpy as np


def stack_images(img_array, scale=1.0, labels=None, size=None):
    if size is None:
        # TODO: correct for img_array being 1-D lists
        size = (img_array[0][0].shape[1], img_array[0][0].shape[0])  # (width, height)

    rows = len(img_array)
    cols = 1
    for row in img_array:
        cols = max(cols, len(row))
    rows_available = isinstance(img_array[0], list)
    width = size[0]
    height = size[1]
    if rows_available:
        for x in range(0, rows):
            for y in range(0, cols):
                if y >= len(img_array[x]):
                    image_blank = np.zeros((height, width, 3), np.uint8)
                    img_array[x].append(image_blank)
                    continue
                img_array[x][y] = cv2.resize(img_array[x][y], size, None, scale, scale)
                if len(img_array[x][y].shape) == 2:
                    img_array[x][y] = cv2.cvtColor(img_array[x][y], cv2.COLOR_GRAY2BGR)
        blank_col = np.zeros((height, width * cols, 3), np.uint8)
        hor = [blank_col] * rows
        for x in range(0, rows):
            hor[x] = np.hstack(img_array[x])
        image_grid = np.vstack(hor)
    else:
        for x in range(0, rows):
            img_array[x] = cv2.resize(img_array[x], size, None, scale, scale)
            if len(img_array[x].shape) == 2:
                img_array[x] = cv2.cvtColor(img_array[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(img_array)
        image_grid = hor
    if labels is not None and len(labels) != 0:
        each_img_width = int(image_grid.shape[1] / cols)
        each_img_height = int(image_grid.shape[0] / rows)
        for d in range(0, rows):
            for c in range(0, cols):
                cv2.rectangle(image_grid, (c * each_img_width, each_img_height * d),
                              (c * each_img_width + len(labels[d][c]) * 13 + 27, 30 + each_img_height * d),
                              (255, 255, 255),
                              cv2.FILLED)
                cv2.putText(image_grid, labels[d][c], (each_img_width * c + 10, each_img_height * d + 20),
                            cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 0, 255), 2)
    return image_grid


if __name__ == "__main__":
    frameWidth = 200
    frameHeight = 200
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    while True:
        success, img = cap.read()
        kernel = np.ones((5, 5), np.uint8)
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 0)
        imgCanny = cv2.Canny(imgBlur, 100, 200)
        imgDilation = cv2.dilate(imgCanny, kernel, iterations=2)
        imgEroded = cv2.erode(imgDilation, kernel, iterations=2)

        StackedImages = stack_images(([img, imgGray, imgBlur],
                                      [imgCanny, imgDilation, imgEroded]),
                                     0.1, size=(frameWidth, frameHeight))
        cv2.imshow("Staked Images", StackedImages)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
