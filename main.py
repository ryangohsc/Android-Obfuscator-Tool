from flask import Flask, render_template, request, Response, jsonify, session
from werkzeug.utils import secure_filename
import secrets, difflib, shutil, os, glob

IP = "127.0.0.1"
PORT = "80"
DEBUG = True
SECRET = secrets.token_urlsafe(16)

app = Flask(__name__)
app.secret_key = SECRET

app.config["UPLOAD_FOLDER"] = "dumpster/"

@app.route("/")
def start():
	return render_template("index.html")

@app.route("/cleanup", methods=['GET', 'POST'])
def cleanup():
	dumpsterFiles = glob.glob("dumpster/*")
	for f in dumpsterFiles:
		try:
			os.remove(f)
		except OSError as e:
			print(e)

	tmpHTMLFiles = glob.glob("static/tmp/*")
	for f in tmpHTMLFiles:
		try:
			os.remove(f)
		except OSError as e:
			print(e)

	return jsonify({'Status': 'Cleanup OK!'}), 200

@app.route("/upload", methods=['GET', 'POST'])
def uploadFile():
	if request.method == "POST":
		orig_file = request.files["file"]
		orig_fileName = secure_filename(orig_file.filename)
		session["filename"] = orig_fileName
		orig_file.save(app.config["UPLOAD_FOLDER"] + orig_fileName)

		mod_fileName = "modded_" + orig_fileName
		session["mod_filename"] = mod_fileName

		shutil.copy(app.config["UPLOAD_FOLDER"] + orig_fileName, app.config["UPLOAD_FOLDER"] + mod_fileName)
	
	return jsonify({'Status': 'File upload OK!'}), 200

@app.route("/readfile", methods=['GET', 'POST'])
def readFile():
	filename = session["filename"]
	file = open(app.config["UPLOAD_FOLDER"] + filename, "r")

	if filename.lower().endswith('.smali'):
		return file.read()
	else:
		return filename

@app.route("/modifysmali", methods=['GET', 'POST'])
def modifySmali():
	mod_fileName = session["mod_filename"]
	with open(app.config["UPLOAD_FOLDER"] + mod_fileName, "r+") as f:
		content = f.read()
		f.seek(0, 0)
		f.write("TEST INSERT\n")

	return jsonify({'Status': 'SMALI Modification OK!'}), 200

@app.route("/comparefile", methods=['GET', 'POST'])
def compareFile():
	orig_filename = session["filename"]
	mod_filename = "modded_" + orig_filename

	orig_file = open(app.config["UPLOAD_FOLDER"] + orig_filename, "r")
	mod_file = open(app.config["UPLOAD_FOLDER"] + mod_filename, "r")

	compare = difflib.HtmlDiff(wrapcolumn=60)

	html = compare.make_file(orig_file, mod_file)

	with open('static/tmp/output.html', 'w') as fh:
		fh.write(html)

	return jsonify({'Status': 'File compare OK!'}), 200

if __name__ == "__main__":
	app.run(host=IP, port=PORT, debug=DEBUG)