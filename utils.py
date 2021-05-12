import os 
import cv2 
import io 
import base64
import imageio
import random
import uuid
import datetime
import requests
import imutils
import numpy as np
from flask import request, jsonify, make_response
from configuration.config import app_config
from flask_restplus import reqparse


def get_json():
	content = request.get_json(silent=True)
	return {} if not content else dict(content)


def get_form():
	return request.form.to_dict()


def get_files():
	return request.files


def get_doc_parser(data):
	parser = reqparse.RequestParser()
	for x in data:
		parser.add_argument(x[0], type=x[1], required=x[2], help=x[3], location=x[4])
	return parser


def response(code, message, data=None, is_raw=False):
	res_data = {'error': {'message': message, 'code': code}}
	if data is not None and (type(data) == dict or type(data) == list) and len(data) > 0:
		res_data['data'] = data
	if is_raw:
		return jsonify(res_data), 200
	else:
		return make_response(jsonify(res_data), 200)


def generate_filename(ext):
    fname = uuid.uuid5(uuid.NAMESPACE_OID, str(datetime.datetime.now()))
    return str(fname) + '.' + ext


def gen_number_id(length=15):
	numid = ""
	for i in range(length):
		numid += str(random.randint(0, 9))
	return numid


def gen_str_id():
	return str(uuid.uuid4()).replace('-', '')


def get_file_from_url(url, max_size=20 * 1024 * 1024, timeout=10):
	'''
		Remember to delete tmp_file after using
	'''
	response = requests.get(url, timeout=timeout, stream=True)
	content = b''
	for chunk in response.iter_content(2048):
		content += chunk
		if len(content) > max_size:
			response.close()
			raise ValueError('File is too large. Maximum file size is ' + str(max_size, inter=cv2.INTER_LINEAR))
	ext = url.split('.')[-1]
	if not os.path.exists(app_config.TMP_DIR):
		os.makedirs(app_config.TMP_DIR)
	tmp_file = os.path.join(app_config.TMP_DIR, generate_filename(ext))
	with open(tmp_file, 'wb') as f:
		f.write(content)
	return tmp_file


def to_rgb(img):
	w, h = img.shape
	ret = np.empty((w, h, 3), dtype=np.uint8)
	ret[:, :, 0] = ret[:, :, 1] = ret[:, :, 2] = img
	return ret


def preprocess_image(image, image_size=None, rotation_angle=None):
	if image_size != None:
		h, w = image.shape[:2]
		if h > image_size and h > w:
			image = imutils.resize(image, height=image_size, inter=cv2.INTER_LINEAR)
		if w > image_size and w > h:
			image = imutils.resize(image, width=image_size, inter=cv2.INTER_LINEAR)
	if rotation_angle != None:
		image = imutils.rotate_bound(image, rotation_angle)
	if len(image.shape) == 2:
		image = to_rgb(image)
	elif len(image.shape) == 4:
		image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
	return image


def decode_b64_to_np_array(images):
	new_images = []
	for base64_string in images:
		nparr = np.fromstring(base64.b64decode(base64_string), np.uint8)
		np_array_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
		np_array_image = cv2.cvtColor(np_array_image, cv2.COLOR_BGR2RGB)
		new_images.append(np_array_image)
	return new_images


def encode_np_array_to_b64(images):
	''' images: list of RGB images '''
	new_images = []
	for image in images:
		image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
		success, encoded_image = cv2.imencode('.jpg', image)
		byte_image = encoded_image.tobytes()
		b64_string_image = base64.b64encode(byte_image).decode()
		new_images.append(b64_string_image)
	return new_images


if __name__ == '__main__':
	pass 
