import emilib
import time
from io import BytesIO

from PIL import Image

def open_eye(res=(640, 480)):

    img = Image.new(mode='RGB', size=res)
    bio = BytesIO()
    img.save(bio, format='jpeg')

    while True:
        time.sleep(1)

        msg = emilib.emi_msg(
            msgnum=1,
            data=bio.getvalue(),
        )

        ret = emilib.emi_msg_send(msg)
        if ret < 0:
            print("fail to send msg")
            time.sleep(1)
            continue

