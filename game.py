import random
import cv2
import hand_detection_lib as handlib
import os

detector = handlib.handDetector()
cam = cv2.VideoCapture(0)


user_points = 0
com_points = 0
games = 0

def draw_results(frame, user_draw):
    global user_points, com_points
    # Cho máy sinh ra lựa chọn ngẫu nhiên
    com_draw = random.randint(0, 2)

    # Kiểm tra và hiển thị kết quá
    if user_draw == com_draw:
        result="DRAW!"
    elif (user_draw == 0) and (com_draw == 1):
        user_points+=1
        result="YOU WIN!"
    elif (user_draw == 1) and (com_draw == 2):
        user_points += 1
        result="YOU WIN!"
    elif (user_draw == 2) and (com_draw == 0):
        user_points+=1
        result="YOU WIN!"
    else:
        com_points+=1
        result="YOU LOSE!"

    frame = cv2.putText(frame, result, (50, 100), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 165, 255), 2, cv2.LINE_AA)

    # Vẽ hình, viết chữ theo user_draw
    frame = cv2.putText(frame, f'You: {user_points}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 255, 0), 2, cv2.LINE_AA)

    s_img = cv2.imread(os.path.join("pix", str(user_draw) + ".png"))
    x_offset = 20
    y_offset = 150
    frame[y_offset:y_offset + s_img.shape[0], x_offset:x_offset + s_img.shape[1]] = s_img


    # Vẽ hình, viết chữ theo com_draw
    frame = cv2.putText(frame, f'Computer: {com_points}', (400, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 0, 255), 2, cv2.LINE_AA)
    s_img = cv2.imread(os.path.join("pix",str(com_draw) + ".png"))
    x_offset = 320
    y_offset = 150
    frame[y_offset:y_offset + s_img.shape[0], x_offset:x_offset + s_img.shape[1]] = s_img

while True:
    ret, frame = cam.read()
    frame = cv2.flip(frame, 1)

    # Đưa hình ảnh vào detector
    frame, hand_lms = detector.findHands(frame)
    n_fingers = detector.count_finger(hand_lms)

    user_draw = 4 # 0: Lá, 1: Đấm, 2 Kéo
    print(n_fingers)
    if n_fingers == 0 or n_fingers == 1:
        user_draw = 1
    elif n_fingers == 2 or n_fingers == 3:
        user_draw = 2
    elif n_fingers == 4 or n_fingers == 5:
        user_draw = 0

    key = cv2.waitKey(1)

    cv2.imshow("game", frame)
    if key==ord("q"):
        break
    elif key == ord(" "):
        draw_results(frame, user_draw)
        cv2.imshow("game", frame)
        cv2.waitKey()
    elif key == ord("`"):
        user_points = 0
        com_points = 0


cam.release()
cv2.destroyAllWindows()