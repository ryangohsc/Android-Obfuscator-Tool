from flask import Flask, render_template, request, Response, jsonify, session
from werkzeug.utils import secure_filename
import secrets, difflib, shutil, os, glob, subprocess

from modules import apk, smali

IP = "127.0.0.1"
PORT = "8080"
DEBUG = True
SECRET = secrets.token_urlsafe(16)

app = Flask(__name__)
app.secret_key = SECRET

app.config["WORKING_FOLDER"] = "dumpster/"
app.config["APKTOOL_LOCATION"] = "jars/apktool_2.6.1.jar"

@app.route("/")
def start():
	return render_template("index.html")

@app.route("/cleanup", methods=['GET', 'POST'])
def cleanup():
	# Cleanup and recreate dumpster/work folder
	shutil.rmtree("dumpster/")
	os.makedirs("dumpster/")
	open("dumpster/.ignore", 'a').close()

	# Cleanup and recreate difflib HTML folder
	shutil.rmtree("static/tmp/")
	os.makedirs("static/tmp/")
	open("static/tmp/.ignore", 'a').close()

	return jsonify({'Status': 'Cleanup OK!'}), 200

@app.route("/upload", methods=['GET', 'POST'])
def uploadFile():
	if request.method == "POST":
		orig_file = request.files["file"]
		orig_fileName = secure_filename(orig_file.filename)
		session["filename"] = orig_fileName
		orig_file.save(app.config["WORKING_FOLDER"] + orig_fileName)

		# mod_fileName = "modded_" + orig_fileName
		# session["mod_filename"] = mod_fileName
		# shutil.copy(app.config["WORKING_FOLDER"] + orig_fileName, app.config["WORKING_FOLDER"] + mod_fileName)
	
	return jsonify({'Status': 'File upload OK!'}), 200

@app.route("/extractapk", methods=['GET', 'POST'])
def extractapk():
	result = apk.extract(app.config["APKTOOL_LOCATION"],
						app.config["WORKING_FOLDER"],
						session["filename"])

	# return jsonify({'Status': 'APK Extraction OK!'}), 200
	return result

@app.route("/locatesmali", methods=['GET', 'POST'])
def locatesmali():
	count = smali.locate(app.config["WORKING_FOLDER"],
						session["filename"])
	return count

# @app.route("/readfile", methods=['GET', 'POST'])
# def readFile():
# 	filename = session["filename"]
# 	file = open(app.config["WORKING_FOLDER"] + filename, "r")

# 	if filename.lower().endswith('.smali'):
# 		return file.read()
# 	else:
# 		return filename

# @app.route("/modifysmali", methods=['GET', 'POST'])
# def modifySmali():
# 	mod_fileName = session["mod_filename"]
# 	with open(app.config["WORKING_FOLDER"] + mod_fileName, "r+") as f:
# 		content = f.read()
# 		f.seek(0, 0)
# 		f.write("TEST INSERT\n")

# 	return jsonify({'Status': 'SMALI Modification OK!'}), 200

# @app.route("/comparefile", methods=['GET', 'POST'])
# def compareFile():
# 	orig_filename = session["filename"]
# 	mod_filename = "modded_" + orig_filename

# 	orig_file = open(app.config["WORKING_FOLDER"] + orig_filename, "r")
# 	mod_file = open(app.config["WORKING_FOLDER"] + mod_filename, "r")

# 	compare = difflib.HtmlDiff(wrapcolumn=60)

# 	html = compare.make_file(orig_file, mod_file)

# 	with open('static/tmp/output.html', 'w') as fh:
# 		fh.write(html)

# 	return jsonify({'Status': 'File compare OK!'}), 200

if __name__ == "__main__":
	app.run(host=IP, port=PORT, debug=DEBUG)