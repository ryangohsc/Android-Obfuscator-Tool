import os, subprocess
import distutils
from distutils import dir_util

def extract(APKTOOL_LOCATION, WORKING_FOLDER, APK_NAME):
    FILE_LOCATION = os.path.join(WORKING_FOLDER, APK_NAME)
    EXTRACT_LOCATION = os.path.join(WORKING_FOLDER, APK_NAME.replace('.apk', ''))
    COMMAND = "java -jar " + APKTOOL_LOCATION + " d " + FILE_LOCATION + " -o " + EXTRACT_LOCATION

    # Run extract command
    result = subprocess.check_output(COMMAND, shell=True)

    # Create base line copy for comparison
    workingCopyDir = EXTRACT_LOCATION
    baselineCopyDir = os.path.join(WORKING_FOLDER, "BASE_" + APK_NAME.replace('.apk', ''))
    distutils.dir_util._path_created = {}
    dir_util.copy_tree(workingCopyDir, baselineCopyDir)

    return result