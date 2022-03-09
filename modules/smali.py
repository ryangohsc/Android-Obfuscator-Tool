import os

def locate(APK_LOCATION, APK_NAME):
    APK_FOLDER = APK_LOCATION + APK_NAME.replace('.apk', '')
    EXT = ".smali"

    tmpFile = open("static/tmp/smali.txt", 'w')

    count = 0

    for root, dirs, files in os.walk(APK_FOLDER):
        for file in files:
            if file.endswith(EXT):
                count += 1;
                print(os.path.join(root, file))
                tmpFile.write(os.path.join(root, file) + "\n")

    tmpFile.close()
    return str(count)