from flask import Flask, render_template, request, Response, jsonify, session, send_file
from werkzeug.utils import secure_filename
import secrets, shutil, os, glob, subprocess

from modules import apk, smali, obfuscator, compare

IP = "127.0.0.1"
PORT = "8080"
DEBUG = True

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)

WORKING_FOLDER = "dumpster"
TOOLS_FOLDER = "tools"
DOWNLOAD_FOLDER = os.path.join(WORKING_FOLDER, "dist")
TMP_ASSET_FOLDER = os.path.join("static", "tmp")
APKTOOL_LOCATION = os.path.join(TOOLS_FOLDER, "apktool_2.6.1.jar")

BASE_SMALI_LOC_FILE = "BASE_smali.txt"  # Path to all untouched SMALI files
WORKING_SMALI_LOC_FILE = "smali.txt"  # Path to all modified/new SMALI files
NEW_SMALI_LOC_FILE = "newfiles.txt"  # Path to all new SMALI files (UI use)

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
    """
    Serves landing page
    :return: index.html
    """
    return render_template("index.html")


@app.route("/cleanup", methods=['GET', 'POST'])
def cleanup():
    """
    Cleans up working directories
    :return: Status 200
    """
    if not os.path.exists(WORKING_FOLDER):
        os.makedirs(WORKING_FOLDER)
    # Cleanup and recreate dumpster/work folder
    shutil.rmtree(WORKING_FOLDER)
    os.makedirs(WORKING_FOLDER)
    wf = os.path.join(WORKING_FOLDER, ".ignore")
    open(wf, 'a').close()

    if not os.path.exists(TMP_ASSET_FOLDER):
        os.makedirs(TMP_ASSET_FOLDER)
    # Cleanup and recreate difflib HTML folder
    shutil.rmtree(TMP_ASSET_FOLDER)
    os.makedirs(TMP_ASSET_FOLDER)
    tf = os.path.join(TMP_ASSET_FOLDER, ".ignore")
    open(tf, 'a').close()

    return jsonify({'Status': 'Cleanup OK!'}), 200


@app.route("/upload", methods=['GET', 'POST'])
def uploadFile():
    """
    Endpoint for APK Upload
    :return: Status 200
    """
    if request.method == "POST":
        # Store APK
        file = request.files["file"]
        session["FILENAME"] = secure_filename(file.filename)
        p = os.path.join(WORKING_FOLDER, session["FILENAME"])
        file.save(p)
        # Store choice of obfuscation methods
        session["OBFUSCATION_METHODS"] = OBFUSCATION_METHODS
        for index, (key, value) in enumerate(request.form.items()):
            if value == "false":
                session["OBFUSCATION_METHODS"][key] = False;

    return jsonify({'Status': 'File upload OK!'}), 200


@app.route("/extractapk", methods=['GET', 'POST'])
def extractapk():
    """
    Trigger for APK extraction
    :return: Status 200
    """
    result = apk.extract(APKTOOL_LOCATION,
                         WORKING_FOLDER,
                         session["FILENAME"])

    return jsonify({'Status': 'APK Extraction OK!'}), 200


@app.route("/locatesmali", methods=['GET', 'POST'])
def locatesmali():
    """
    Trigger for SMALI locating via traversal
    :return: count - Number of SMALI files found from extracted APK
    """
    count = smali.locate(WORKING_FOLDER,
                         TMP_ASSET_FOLDER,
                         session["FILENAME"],
                         BASE_SMALI_LOC_FILE,
                         WORKING_SMALI_LOC_FILE,
                         NEW_SMALI_LOC_FILE)

    return count


@app.route("/obfuscate", methods=['GET', 'POST'])
def obfuscate():
    """
    Trigger for obfuscation functions
    :return: Status 200
    """
    obfuscator.run(TMP_ASSET_FOLDER,
                   WORKING_FOLDER,
                   session["FILENAME"],
                   session["OBFUSCATION_METHODS"])

    return jsonify({'Status': 'Obfuscation OK!'}), 200


@app.route("/comparefile", methods=['GET', 'POST'])
def compareFile():
    """
    Trigger for SMALI file comparison between original(BASE) and modified(WORKING)
    :return: selectListData - List of modified files for user selection in HTML
    """
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
    """
    Trigger for APK re-compilation
    :return: Status 200
    """
    apk.recompile(APKTOOL_LOCATION,
                         WORKING_FOLDER,
                         session["FILENAME"], TOOLS_FOLDER)
    return jsonify({'Status': 'APK Recompile OK!'}), 200


@app.route("/download", methods=['GET', 'POST'])
def download_file():
    """
    Endpoint for APK Download
    :return: APK file
    """
    FILE = os.path.join(DOWNLOAD_FOLDER, "final_" + session["FILENAME"])
    return send_file(FILE, as_attachment=True)


if __name__ == "__main__":
    app.run(host=IP, port=PORT, debug=DEBUG)
