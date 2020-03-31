import json
import requests
import re

base_url = 'https://canvas.instructure.com/'
postman_domain = '{{domain}}'

print('Getting base doc')
top_level_docs = requests.get('{}/doc/api/api-docs.json'.format(base_url))

docs = top_level_docs.json()['apis']

postman_collection = {
	'info': {
		'name': 'Canvas API',
		'schema': 'https://schema.getpostman.com/json/collection/v2.1.0/collection.json'
	},
	'item': [],
	'auth': {
		'type': 'bearer',
		'bearer': [
			{
				'key': 'token',
				'value': '{{user_token}}',
				'type': 'string'
			}
		]
	}
}

for doc in docs:
	folder = {
		'name': doc['description'],
		'item': []
	}
	print('Getting {} doc'.format(folder['name']))
	raw_doc_request = requests.get('{}/doc/api{}'.format(base_url,doc['path']))
	doc_detail = raw_doc_request.json()
	for item in doc_detail['apis']:
		path_array = [
			'api'
			]
		path_array_items = []
		path_elements = re.findall('(\/[^/]*)', item['path'])
		for el in path_elements:
			el = el[1:]
			if '{' in el:
				path_array_items = re.sub('{',':',re.sub('}','',el))
				path_array.append(path_array_items)
			else:
				path_array.append(el)
		revised_path = '/'.join(path_array)

		form_parameters = []
		variable_array = []
		if 'parameters' in list(item['operations'][0]):
			for param in item['operations'][0]['parameters']:
				if param['paramType'] == 'form':
					param_type = 'text'
					if param['type'] == 'file':
						param_type = 'file'

					temp_param = {
						'key': param['name'],
						'value': '',
						'type': param_type,
						'description': param['description']
					}
					form_parameters.append(temp_param)
				elif param['paramType'] == 'path':
					temp_var = {
						'key': param['name'],
						'description': param['description']
					}
					variable_array.append(temp_var)

		# put it all together
		api_call = {
			'name': item['operations'][0]['summary'],
			'request': {
				'method': item['operations'][0]['method'],
				'header': [],
				'url': {
					'raw': 'https://{}/api/{}'.format(postman_domain, revised_path),
					'protocol': 'https',
					'host': [ postman_domain ],
					'path': path_array,
					'variable': variable_array
				},
				'description': item['description']
			},
			'response': []
		}	

		if len(form_parameters) > 0:
			api_call['request']['body'] = {
				'mode': 'formdata',
				'formdata': form_parameters
			}
		folder['item'].append(api_call)
	postman_collection['item'].append(folder)

with open('output.json', 'w') as f:
	json.dump(postman_collection, f, indent=3, separators=(',', ': '))
