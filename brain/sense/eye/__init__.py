import importlib.util
if importlib.util.find_spec("picamera"):
    from .picamera_eye import open_eye
elif importlib.util.find_spec("cv2"):
    from .camera_eye import open_eye
else:
    from .fake_eye import open_eye
