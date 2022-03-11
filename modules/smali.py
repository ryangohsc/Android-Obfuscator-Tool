import os

def locate(APK_LOCATION, APK_NAME):
    APK_FOLDER = os.path.join(APK_LOCATION, APK_NAME.replace('.apk', ''))
    EXT = ".smali"

    p = os.path.join("static", "tmp", "smali.txt")
    tmpFile = open(p, 'w')

    count = 0

    for root, dirs, files in os.walk(APK_FOLDER):
        for file in files:
            if file.endswith(EXT):
                count += 1;
                tmpFile.write(os.path.join(root, file) + "\n")

    tmpFile.close()
    return str(count)