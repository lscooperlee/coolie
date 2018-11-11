import base64
import json
import struct
from functools import partial

from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import emilib

img = None

emilib.emi_init()

def func(msg):
    global img
    img = msg.data
    return 0

emilib.emi_msg_register(1, func)

msgdict = {
        'w': emilib.emi_msg(msgnum = ord('m'), cmd = ord('w'),
            data=struct.pack('=ff', 1, 0)), #forward, default speed 1
        's': emilib.emi_msg(msgnum = ord('m'), cmd = ord('s'),
            data=struct.pack('=ff', 1, 0)), #backward default speed 1
        'a': emilib.emi_msg(msgnum = ord('m'), cmd = ord('a'),
            data=struct.pack('=ff', 5, 0)), #left turn, default speed 5
        'd': emilib.emi_msg(msgnum = ord('m'), cmd = ord('d'),
            data=struct.pack('=ff', 5, 0)), #right turn, default speed 5
        'n': emilib.emi_msg(msgnum = ord('m'), cmd = ord('n')),
        'c': emilib.emi_msg(msgnum = ord('m'), cmd = ord('c')),
        'u': emilib.emi_msg(msgnum = ord('u')),
        }

def index(request):
    return render(request, "index.html")

def get_image(request):
    encoded_string = base64.b64encode(img).decode() if img else ""
    return JsonResponse({'base64img':encoded_string})

@csrf_exempt
def key_handler(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode())
        if data['key'] in msgdict:
            emilib.emi_msg_send(msgdict[data['key']])
        elif data['key'] in '12345':
            msgdata = struct.pack('=ff', float(data['key']), 0)
            msg = emilib.emi_msg(msgnum=ord('m'), cmd=ord('u'), data=msgdata)
            emilib.emi_msg_send(msg)

    return HttpResponse()
