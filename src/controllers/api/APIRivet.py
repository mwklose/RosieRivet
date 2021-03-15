import flask
from flask import request
from flask import jsonify
from flask import make_response
import os
app = flask.Flask(__name__)
app.config["DEBUG"] = True
import sys
# Determine current path of file
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

# Allow for import of RosieRivet
sys.path.append(os.path.abspath(os.path.join('..','..')))

from Rivet import RosieRivet
# Get analysis
@app.route('/v1/analyze', methods=['POST'])
def analyze():
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


	#Removed requested file
	os.remove((os.path.join(ROOT_PATH,file.filename)))

	#Convert Tuple to string (JSON cannot serialize tuples)
	for riveter,anl in analysis.items():
		analysis[riveter]["detected"] = dict((':'.join(str(keys) for keys in k), v) for k,v in analysis[riveter]["detected"].items())
	#Return successful analysis
	return make_response(jsonify(analysis),200)

app.run()