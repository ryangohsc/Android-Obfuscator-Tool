from flask import Flask, render_template, request, Response, jsonify, session
from werkzeug.utils import secure_filename
import secrets, shutil, os, glob, subprocess

from modules import apk, smali, obfuscator, compare

IP = "127.0.0.1"
PORT = "8080"
DEBUG = True

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)

WORKING_FOLDER = "dumpster"
TMP_ASSET_FOLDER = os.path.join("static", "tmp")
APKTOOL_LOCATION = os.path.join("jars", "apktool_2.6.1.jar")
TOOLS_FOLDER = "tools"

BASE_SMALI_LOC_FILE = "BASE_smali.txt"  # Path to all untouched SMALI files
WORKING_SMALI_LOC_FILE = "smali.txt"  # Path to all modified/new SMALI files
NEW_SMALI_LOC_FILE = "newfiles.txt" # Path to all new SMALI files (UI use)

OBFUSCATION_METHODS = {
    "dci": True,
    "dmi": True,
    "uj": True,
    "ab": True,
    "nop": True,
    "method_rename": True,
    "variable_rename": True,
    "ro": True
}

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
        # Store APK
        file = request.files["file"]
        session["FILENAME"] = secure_filename(file.filename)
        p = os.path.join(WORKING_FOLDER, session["FILENAME"])
        file.save(p)
        # Store choice of obfuscation methods
        session["OBFUSCATION_METHODS"] = OBFUSCATION_METHODS
        for index, (key, value) in enumerate((request.form).items()):
            if (value == "false"):
                session["OBFUSCATION_METHODS"][key] = False;

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
                         TMP_ASSET_FOLDER,
                         session["FILENAME"],
                         BASE_SMALI_LOC_FILE,
                         WORKING_SMALI_LOC_FILE,
                         NEW_SMALI_LOC_FILE)

    return count


@app.route("/obfuscate", methods=['GET', 'POST'])
def obfuscate():
    obfuscator.run(TMP_ASSET_FOLDER,
                   WORKING_FOLDER,
                   session["FILENAME"],
                   session["OBFUSCATION_METHODS"])

    return jsonify({'Status': 'Obfuscation OK!'}), 200


@app.route("/comparefile", methods=['GET', 'POST'])
def compareFile():
    count = compare.generate(TMP_ASSET_FOLDER,
                             BASE_SMALI_LOC_FILE,
                             WORKING_SMALI_LOC_FILE)
    session["COUNT"] = count

    selectListData = compare.loadHTMLSelect(TMP_ASSET_FOLDER,
                                            WORKING_FOLDER,
                                            WORKING_SMALI_LOC_FILE,
                                            session["FILENAME"])
    return jsonify(selectListData)


@app.route("/recompileapk", methods=['GET', 'POST'])
def recompile_apk():
    result = apk.recompile(APKTOOL_LOCATION,
                         WORKING_FOLDER,
                         session["FILENAME"], TOOLS_FOLDER)

    return result


if __name__ == "__main__":
    app.run(host=IP, port=PORT, debug=DEBUG)
