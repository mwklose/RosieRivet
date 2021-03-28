import flask
from flask import request
from flask import make_response
from flask import jsonify
from datetime import timedelta
from cache import LRUCache
import os
import zipfile
from flask import send_file
import csv,json
import pprint
from flask_cors import CORS




app = flask.Flask(__name__)
app.config["DEBUG"] = True
import sys
# Determine current path of file
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

CORS(app)

# Allow for import of RosieRivet
sys.path.append(os.path.abspath(os.path.join('..','..')))

#Initialize session cache
sess_cache = LRUCache.LRUCache(10)

SECRET_KEY = "ses1221"

from Rivet import RosieRivet
# Get analysis
@app.route('/v1/analyze', methods=['POST'])
def analyze():
	#If request is made without session key return invalid request
	if("sess_key" not in request.form):
		return make_response({},400)
	# reference file object
	file = request.files['file']
	# save file (this ports better with our current design as we have no current implementation of parsing json)
	file.save(os.path.join(ROOT_PATH,file.filename))

	#Initialize a RosieRivet
	rr = RosieRivet.RosieRivet(file.filename)

	#retrieve Rosie analysis, return error if error is raised anywhere in RosieRivet
	try:
		analysis = rr.RivetFileAnalyzer()
	except:
		return make_response({},400)



	#Convert Tuple to string (JSON cannot serialize tuples)
	for riveter,anl in analysis.items():
		# SORT KEY VALUES HERE
		analysis[riveter]["detected"] = dict((':'.join(str(keys) for keys in k), v) for k,v in analysis[riveter]["detected"].items())

	#store RosieRivet object and file under session key
	cookie_key = request.form['sess_key'] + SECRET_KEY
	sess_cache.put(cookie_key, rr, file)



	# #Removed requested file
	# os.remove((os.path.join(ROOT_PATH,file.filename)))

	#Return successful analysis
	return make_response(jsonify(analysis),200)

@app.route('/v1/process', methods=['POST'])
def process():
	#If request is made without session key return invalid request
	if("sess_key" not in request.form):
		return make_response({},400)
	
	#retrieve session key
	cookie_key = request.form["sess_key"] + SECRET_KEY

	#if session key was not created prior to process or session key is deleted, return invalid request
	if(sess_cache.get(cookie_key) == -1):
		return make_response({},400)

	#retrieve RosieRivet object and file associated with session key
	rr,file = sess_cache.get(cookie_key)

	# #save file
	# file.save(os.path.join(ROOT_PATH,file.filename))

	#retrieve analysis(options) back from frontend which should be edited by the user to their preference
	options = json.loads(request.form["analysis"])
	for riveter,anl in options.items():
		options[riveter]["detected"] = dict(((int(k.split(":")[0]), int(k.split(":")[1]), k.split(":")[2]), v) for k,v in options[riveter]["detected"].items())
	
	print(options)
	#Process file
	rivetCSV, rivetTXT = rr.RivetProcessor(options)

	#Write modified file
	with open("out.csv", "w") as cf:
	    cw = csv.writer(cf)
	    cw.writerows(rivetCSV)

	with open("out.txt", "w") as tf:
		pprint.PrettyPrinter(indent=4, stream=tf).pprint(rivetTXT)


	zipf = zipfile.ZipFile('modified.zip','w', zipfile.ZIP_DEFLATED)
	zipf.write("out.csv")
	zipf.write("out.txt")
	zipf.close()

	#remove files created
	os.remove((os.path.join(ROOT_PATH,file.filename)))

	return send_file('modified.zip',mimetype = 'zip',attachment_filename= 'modified.zip',as_attachment = True)


 
app.run(host='127.0.0.1', port=5000)