import cv2


def show_img(file_name, wait_time):
    img = cv2.imread(file_name)
    cv2.imshow(file_name, img)
    cv2.waitKey(wait_time)


def show_video(file_name=0):
    cap = cv2.VideoCapture(file_name, cv2.CAP_DSHOW)  # ?cv2.CAP_DSHOW slows down system?

    while True:
        success, img = cap.read()
        if not success:
            print("Error!")
            break
        cv2.imshow("Video", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # show_img('Resources/lena.bmp', 1000)
    show_video()
    cv2.destroyAllWindows()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
