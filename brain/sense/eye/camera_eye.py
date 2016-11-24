import cv2
import emilib
import time

def open_eye(res=(640, 480)):
    print('camera')

    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, res[0])
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, res[1])

    time.sleep(1)

    while True:
        time.sleep(0.1)

        ret, im = camera.read()
        if ret is None:
            print("fail to get camera")
            time.sleep(1)
            continue

        ret, jpg = cv2.imencode(".jpg", im)

        msg = emilib.emi_msg(
            msgnum=1,
            data=jpg.tobytes(),
            # flag=emilib.emi_flag.EMI_MSG_MODE_BLOCK
        )

        ret = emilib.emi_msg_send(msg)
        if ret < 0:
            print("fail to send msg")
            time.sleep(1)
            continue

    del(camera)
