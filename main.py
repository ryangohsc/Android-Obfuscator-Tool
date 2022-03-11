from flask import Flask, render_template, request, Response, jsonify, session
from werkzeug.utils import secure_filename
import secrets, difflib, shutil, os, glob, subprocess

from modules import apk, smali, obfuscator

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
		file = request.files["file"]
		fileName = secure_filename(file.filename)
		session["filename"] = fileName
		file.save(app.config["WORKING_FOLDER"] + fileName)

	return jsonify({'Status': 'File upload OK!'}), 200

@app.route("/extractapk", methods=['GET', 'POST'])
def extractapk():
	result = apk.extract(app.config["APKTOOL_LOCATION"],
						app.config["WORKING_FOLDER"],
						session["filename"])

	return result

@app.route("/locatesmali", methods=['GET', 'POST'])
def locatesmali():
	count = smali.locate(app.config["WORKING_FOLDER"],
						session["filename"])

	return count

@app.route("/obfuscate", methods=['GET', 'POST'])
def obfuscate():
	obfuscator.run()

	return jsonify({'Status': 'Obfuscation OK!'}), 200

@app.route("/comparefile", methods=['GET', 'POST'])
def compareFile():
	workingCopyDir = app.config["WORKING_FOLDER"] + session["filename"].replace('.apk', '')
	baselineCopyDir = app.config["WORKING_FOLDER"] + "BASE_" + session["filename"].replace('.apk', '')

	#
	# SAMPLE TO TEST IF COMPARE WORKS
	#
	working = open(workingCopyDir + "/smali/com/securitycompass/androidlabs/base/AccountsActivity.smali", "r")
	baseline = open(baselineCopyDir + "/smali/com/securitycompass/androidlabs/base/AccountsActivity.smali", "r")
	compare = difflib.HtmlDiff(wrapcolumn=62)
	html = compare.make_file(baseline, working)

	with open('static/tmp/output.html', 'w') as fh:
		fh.write(html)

	return jsonify({'Status': 'File compare OK!'}), 200

if __name__ == "__main__":
	app.run(host=IP, port=PORT, debug=DEBUG)