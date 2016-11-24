import emilib
import time
import io
import picamera

def open_eye(res=(640, 480)):

    camera = picamera.PiCamera()
    camera.resolution = res
    camera.vflip = True
    camera.hflip = True

    camera.start_preview()
    time.sleep(2)

    stream = io.BytesIO()
    for foo in camera.capture_continuous(stream, 'jpeg'):

        stream.seek(0)

        msg = emilib.emi_msg(
            msgnum=1,
            data=stream.read(),
        )

        stream.seek(0)
        stream.truncate()

        ret = emilib.emi_msg_send(msg)
        if ret < 0:
            print("fail to send msg")
            time.sleep(1)
            continue
