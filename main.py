import cv2
import numpy as np


def show_img(file_name, wait_time):
    img = cv2.imread(file_name)
    cv2.imshow(file_name, img)
    cv2.waitKey(wait_time)


def show_video(file_name=0):
    cap = cv2.VideoCapture(file_name, cv2.CAP_DSHOW)  # ?cv2.CAP_DSHOW slows down system?

    while True:
        success, img = cap.read()
        img = cv2.resize(img, (200, 400))  # resize (width/x, height/y)
        img = img[:200, 50:350]  # crop: [height, width]
        if not success:
            print("Error!")
            break
        cv2.imshow("Video", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()


def lines_shapes(size):
    img = np.zeros(size + (3,), np.uint8)
    # img[:] = 255, 255, 0  # Change BG colour
    cv2.imshow("Blank", img)

    # Draw a line, circle, rectangle, text
    cv2.line(img, (10, 10), (size[0] - 10, size[1] - 10), (128, 128, 128), 2)
    cv2.circle(img, (size[0] // 3, 2 * size[1] // 3), 100, (255, 0, 0), 2)
    cv2.rectangle(img, (2 * size[0] // 3, size[1] // 3), (2 * size[0] // 3 + 100, size[1] // 3 + 100), (0, 255, 0),
                  cv2.FILLED)
    cv2.putText(img, "Draw Shapes...", (75, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255))
    cv2.imshow("Line, circle, rectangle and text.", img)
    cv2.waitKey(0)


def warp_perspective(img_file, points, width, height):
    img = cv2.imread(img_file)
    ref_points = [(0, 0), (width, 0), (0, height), (width, height)]
    matrix = cv2.getPerspectiveTransform(np.float32(points), np.float32(ref_points))
    transformed_img = cv2.warpPerspective(img, matrix, (width, height))
    for point in points:
        cv2.circle(img, point, 5, (0, 0, 255), cv2.FILLED)
    cv2.imshow("Original image with markings", img)
    cv2.imshow("Transformed image", transformed_img)
    cv2.waitKey(0)


if __name__ == '__main__':
    # show_img('Resources/lena.bmp', 1000)
    # show_video()
    # cv2.destroyAllWindows()
    # lines_shapes((512, 512))
    warp_perspective("Resources/chess.jpg", [(23, 149), (187, 93), (290, 334), (474, 237)], 300, 600)
