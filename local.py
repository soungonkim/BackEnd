import os
import threading
from flask import Flask, request, render_template, redirect, url_for, send_file
import numpy as np
import cv2
from werkzeug.utils import secure_filename
import style_transfer
from PIL import Image
import io
import shutil

# from flask.ext.uploads import UploadSet, configure_uploads, IMAGES

app = Flask(__name__)

style_img = None
count = 0


def MyThread1(args):
    global count
    print("#########################################")
    print(args)
    print(type(args))
    print("#########################################")
    # args = list(args)
    a, b = args.split('@')
    style_transfer.style_transfer(a, b, count)
    pass


@app.route('/')
def hello():
    return 'Hello, World!'


@app.route('/input/filter', methods=['GET'])
def get_input_filter():
    filter = request.args.get('filter')
    print(filter)
    global count
    global style_img
    # print (request)
    if filter == 'Gogh_painting':
        style_img = './input/Gogh_painting.png'
    elif filter == 'Gogh_portrait':
        style_img = './input/Gogh_portrait.jpg'
    elif filter == 'Monet_painting':
        style_img = './input/Monet_painting.jpg'
    elif filter == 'Monet_portrait':
        style_img = './input/Monet_portrait.jpg'
    elif filter == 'Chung_painting':
        style_img = './input/Chung_painting.jpg'
    elif filter == 'Lee_portrait':
        style_img = './input/Lee_portrait.jpg'
    elif filter == 'Picaso_portrait':
        style_img = './input/Picaso_portrait.jpg'
    elif filter == 'Picaso_painting':
        style_img = './input/Picaso_painting.jpg'
    elif filter == 'Mona_lisa':
        style_img = './input/Mona_lisa.jpg'
    else:
        style_img = 'None'

    if not os.path.exists('./result/' + str(count)):
        os.mkdir('./result/' + str(count))
    print(style_img)

    return "Filter Selected"


@app.route('/test', methods=['GET'])
def test():
    request.args.get('num')
    num = request.args.get('num')
    img_path = './result/' + str(count) + '/' + num + '.jpg'
    if os.path.isfile(img_path):
        return 'yes'

    else:
        return 'no'


@app.route('/done', methods=['GET'])
def done():
    global count
    state = request.args.get('done')
    if state == "True":
        if os.path.exists('./result/' + str(count)):
            shutil.rmtree('./result/'+str(count))
        return "Image Deleted"


@app.route('/input/img', methods=['GET', 'POST'])
def get_input_img():
    savepath = './input/input_img.jpg'
    image = request.files['image']
    in_memory_file = io.BytesIO()
    image.save(in_memory_file)
    data = np.fromstring(in_memory_file.getvalue(), dtype=np.uint8)
    color_image_flag = 1
    img = cv2.imdecode(data, color_image_flag)
    cv2.imwrite(savepath, img)

    t1 = threading.Thread(target=MyThread1, args={savepath + '@' + style_img: ""})
    t1.start()
    return "Image Get!"


@app.route('/output', methods=['GET', 'POST'])
def post_output_img():
    global count
    num = request.args.get('num')
    img_path = './result/' + str(count) + '/' + num + '.jpg'
    if num == 10:
        count += 1
    return send_file(img_path, mimetype='image/jpeg')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, threaded=True, debug=True)
