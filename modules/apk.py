import os, subprocess

def extract(APKTOOL_LOCATION, APK_LOCATION, APK_NAME):
    EXTRACT_LOCATION = APK_LOCATION + APK_NAME.replace('.apk', '')
    COMMAND = "java -jar " + APKTOOL_LOCATION + " d " + APK_LOCATION + APK_NAME + " -o " + EXTRACT_LOCATION
    result = subprocess.check_output(COMMAND, shell=True)
    return result