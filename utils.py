import uuid
from flask import request, jsonify, make_response

def get_json():
	content = request.get_json(silent=True)
	return {} if not content else dict(content)


def response(code, message, data=None, is_raw=False):
	res_data = {'error': {'message': message, 'code': code}}
	if data is not None and (type(data) == dict or type(data) == list) and len(data) > 0:
		res_data['data'] = data
	if is_raw:
		return jsonify(res_data), 200
	else:
		return make_response(jsonify(res_data), 200)




def gen_str_id():
	return str(uuid.uuid4()).replace('-', '')




if __name__ == '__main__':
	pass 
