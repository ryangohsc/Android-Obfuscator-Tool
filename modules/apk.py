import os, subprocess
import distutils
from distutils import dir_util


def extract(APKTOOL_LOCATION, WORKING_FOLDER, APK_NAME):
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


def recompile(APKTOOL_LOCATION, WORKING_FOLDER, APK_NAME):
    WORKING_COPY_DIR = os.path.join(WORKING_FOLDER, APK_NAME.replace('.apk', ''))
    if os.path.exists(os.path.join(WORKING_FOLDER, "dist")):
        os.makedirs(os.path.join(WORKING_FOLDER, "dist"))
    FILE_LOCATION = os.path.join(WORKING_FOLDER, "dist", APK_NAME)
    COMMAND = "java -jar " + APKTOOL_LOCATION + " b " + WORKING_COPY_DIR + " -o " + FILE_LOCATION

    # Run extract command
    result = subprocess.check_output(COMMAND, shell=True)

    return result
