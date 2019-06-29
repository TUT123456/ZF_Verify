# -*- coding: UTF-8 -*-
"""
构建flask接口服务
接收 files={'image_file': ('captcha.jpg', BytesIO(bytes), 'application')} 参数识别验证码
需要配置参数：
    image_height = 40
    image_width = 80
    max_captcha = 4
"""
import json
import os
import random
import string
import time
from flask import Flask, request, jsonify, Response
from recognizer import recognizer

# 默认使用CPU
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "-1i"

# 使用后缀
image_suffix = '.png'
api_image_dir = './img/'

# Flask对象
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))


def response_headers(content):
    resp = Response(content)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/b', methods=['POST'])
def up_image():
    if request.method == 'POST' and request.files.get('image_file'):
        timec = str(time.time()).replace(".", "")
        img = request.files.get('image_file')
        # 生成随机字符串，防止图片名字重复
        ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 16))
        # 定义一个图片存放的位置 存放在api_img_dir下面
        path = api_image_dir
        # 图片名称 给图片重命名 为了图片名称的唯一性
        imgName = ran_str + img.filename
        # 图片path和名称组成图片的保存路径
        file_path = path + imgName
        # 保存图片
        img.save(file_path)
        # username = request.form.get("name")
        s = time.time()
        value = recognizer.recognize_checkcode(file_path)
        e = time.time()
        print("识别结果: {}".format(value))
        # 重命名图片
        print("保存图片： {}{}_{}.{}".format(api_image_dir, value, timec, image_suffix))
        file_name = "{}_{}.{}".format(value, timec, image_suffix)
        rename_file_path = os.path.join(api_image_dir + file_name)
        os.rename(file_path, rename_file_path)
        result = {
            'time': timec,   # 时间戳
            'value': value,  # 预测的结果
            'speed_time(ms)': int((e - s) * 1000)  # 识别耗费的时间
        }
        img.close()
        return jsonify(result)
    else:
        content = json.dumps({"error_code": "1001"})
        resp = response_headers(content)
        return resp


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=6000,
        debug=True
    )
