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

WORKING_FOLDER = "dumpster"
TMP_ASSET_FOLDER = os.path.join("static", "tmp")
APKTOOL_LOCATION = os.path.join("jars", "apktool_2.6.1.jar")

@app.route("/")
def start():
	return render_template("index.html")

@app.route("/cleanup", methods=['GET', 'POST'])
def cleanup():
	# Cleanup and recreate dumpster/work folder
	shutil.rmtree(WORKING_FOLDER)
	os.makedirs(WORKING_FOLDER)
	wf = os.path.join(WORKING_FOLDER, ".ignore")
	open(wf, 'a').close()


	# Cleanup and recreate difflib HTML folder
	shutil.rmtree(TMP_ASSET_FOLDER)
	os.makedirs(TMP_ASSET_FOLDER)
	tf = os.path.join(TMP_ASSET_FOLDER, ".ignore")
	open(tf, 'a').close()

	return jsonify({'Status': 'Cleanup OK!'}), 200

@app.route("/upload", methods=['GET', 'POST'])
def uploadFile():
	if request.method == "POST":
		file = request.files["file"]
		session["FILENAME"] = secure_filename(file.filename)
		p = os.path.join(WORKING_FOLDER, session["FILENAME"])
		file.save(p)

	return jsonify({'Status': 'File upload OK!'}), 200

@app.route("/extractapk", methods=['GET', 'POST'])
def extractapk():
	result = apk.extract(APKTOOL_LOCATION,
						WORKING_FOLDER,
						session["FILENAME"])

	return result

@app.route("/locatesmali", methods=['GET', 'POST'])
def locatesmali():
	count = smali.locate(WORKING_FOLDER,
						session["FILENAME"])

	return count

@app.route("/obfuscate", methods=['GET', 'POST'])
def obfuscate():
	obfuscator.run()

	return jsonify({'Status': 'Obfuscation OK!'}), 200

@app.route("/comparefile", methods=['GET', 'POST'])
def compareFile():
	workingCopyDir = os.path.join(WORKING_FOLDER, session["FILENAME"].replace('.apk', ''))
	baselineCopyDir = os.path.join(WORKING_FOLDER, "BASE_" + session["FILENAME"].replace('.apk', ''))

	#
	# SAMPLE TO TEST IF COMPARE WORKS
	#
	wp = os.path.join(workingCopyDir, "smali", "com", "securitycompass", "androidlabs", "base", "AccountsActivity.smali")
	bp = os.path.join(baselineCopyDir, "smali", "com", "securitycompass", "androidlabs", "base", "AccountsActivity.smali")
	working = open(wp, "r")
	baseline = open(bp, "r")
	compare = difflib.HtmlDiff(wrapcolumn=62)
	html = compare.make_file(baseline, working)

	hp = os.path.join(TMP_ASSET_FOLDER, "output.html")
	with open(hp, 'w') as fh:
		fh.write(html)

	return jsonify({'Status': 'File compare OK!'}), 200

if __name__ == "__main__":
	app.run(host=IP, port=PORT, debug=DEBUG)