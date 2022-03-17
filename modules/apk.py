import os, subprocess
import distutils
from distutils import dir_util


def extract(APKTOOL_LOCATION, WORKING_FOLDER, APK_NAME):
    """
    Extracts APK uploaded by user
    :return: java process output(console)
    """
    FILE_LOCATION = os.path.join(WORKING_FOLDER, APK_NAME)
    WORKING_COPY_DIR = os.path.join(WORKING_FOLDER, APK_NAME.replace('.apk', ''))
    BASELINE_COPY_DIR = os.path.join(WORKING_FOLDER, "BASE_" + APK_NAME.replace('.apk', ''))
    COMMAND = "java -jar " + APKTOOL_LOCATION + " d " + FILE_LOCATION + " -o " + WORKING_COPY_DIR

    # Run extract command
    result = subprocess.check_output(COMMAND, shell=True)

    # Create base line copy for comparison
    distutils.dir_util._path_created = {}
    dir_util.copy_tree(WORKING_COPY_DIR, BASELINE_COPY_DIR)

    return result


def recompile(APKTOOL_LOCATION, WORKING_FOLDER, APK_NAME, TOOLS_FOLDER):
    """
    Recompiles APK after obfuscation/modification
    :return: java process output(console)
    """
    WORKING_COPY_DIR = os.path.join(WORKING_FOLDER, APK_NAME.replace('.apk', ''))
    if os.path.exists(os.path.join(WORKING_FOLDER, "dist")):
        os.makedirs(os.path.join(WORKING_FOLDER, "dist"))
    FILE_LOCATION = os.path.join(WORKING_FOLDER, "dist", APK_NAME)
    COMMAND = "java -jar " + APKTOOL_LOCATION + " b " + WORKING_COPY_DIR + " -o " + FILE_LOCATION

    # Run extract command
    result = subprocess.check_output(COMMAND, shell=True)

    # Zipalign and re-sign new APK
    if os.path.exists(FILE_LOCATION):
        ZIPALIGN_LOCATION = os.path.join(TOOLS_FOLDER, "zipalign.exe")
        APKSIGNER_LOCATION = os.path.join(TOOLS_FOLDER, "apksigner.jar")
        KEY = os.path.join(TOOLS_FOLDER, "release.jks")
        ZIPALIGN_FILE = os.path.join(WORKING_FOLDER, "dist", "final_"+APK_NAME)
        ZIPALIGN_COMMAND = ZIPALIGN_LOCATION + " -v 4 " + FILE_LOCATION + " " +  ZIPALIGN_FILE
        zipalign_result = subprocess.check_output(ZIPALIGN_COMMAND, shell=True)
        RESIGN_COMMAND = APKSIGNER_LOCATION + " sign --ks " + KEY + " --ks-key-alias release --ks-pass pass:s7p4od2 --key-pass pass:r5o8lw3 " + ZIPALIGN_FILE
        resign_result = subprocess.check_output(RESIGN_COMMAND, shell=True)

    return result, zipalign_result, resign_result
