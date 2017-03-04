import json, logging, random
from flask import Flask, request, make_response
from functools import wraps, update_wrapper
from datetime import datetime

def nocache(view):
	@wraps(view)
	def no_cache(*args, **kwargs):
		response = make_response(view(*args, **kwargs))
		response.headers['Last-Modified'] = datetime.now()
		response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
		response.headers['Pragma'] = 'no-cache'
		response.headers['Expires'] = '-1'
		return response
	return update_wrapper(no_cache, view)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__, static_url_path='')
app.debug = True

@app.route('/')
@nocache
def root():
	return file('index.html').read()

@app.route('/main.js')
@nocache
def main():
	fake = str(random.randrange(1100000, 1600000))
	rnd = ''
	for i in xrange(random.randrange(100)):
		rnd += 'for(var x = 0; x < %i; ++x) {\n' % random.randrange(10, 1000)
		for j in xrange(random.randrange(10)):
			if random.randrange(2) == 0:
				rnd += '\tvar _%s = %i %s %i;\n' % (''.join(random.choice('abcdefghijklmnopqrstuvwxyz0123456789') for i in xrange(random.randrange(3, 12))), random.randrange(-100000, 10000000), random.choice('+-/*'), random.randrange(-100000, 10000000))
			else:
				rnd += '\tvar _%s = new Uint32Array(%i);' % (''.join(random.choice('abcdefghijklmnopqrstuvwxyz0123456789') for i in xrange(random.randrange(3, 12))), random.randrange(0, 1000))
		rnd += '}\n'
	return file('main.js').read().replace('FAKE', fake).replace('RND', rnd)

@app.route('/log', methods=['POST'])
@nocache
def log():
	if request.form['data'] == 'undefined':
		message = '??undefined??'
	else:
		message = json.loads(request.form['data'])
	if message == 'Loaded':
		print
		print
	print 'Log: ', message
	return ''

@app.route('/error', methods=['POST'])
@nocache
def error():
	line, message = json.loads(request.form['data'])

	print 'ERR [%i]: ' % line, message
	return ''

app.run(host='0.0.0.0', port=80, threaded=True)
