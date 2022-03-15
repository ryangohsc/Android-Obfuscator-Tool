import os

def locate(APK_LOCATION, TMP_ASSET_FOLDER, APK_NAME, BASE_SMALI_LOC_FILE, WORKING_SMALI_LOC_FILE):
    """
    Traverse working directory to locate smali files
    :return: number of smali files
    """
    BASE_APK_FOLDER = os.path.join(APK_LOCATION, "BASE_" + APK_NAME.replace('.apk', ''))
    EXT = ".smali"

    bc = os.path.join(TMP_ASSET_FOLDER, BASE_SMALI_LOC_FILE)
    wc = os.path.join(TMP_ASSET_FOLDER, WORKING_SMALI_LOC_FILE)

    baseline_copy = open(bc, 'w')
    working_copy = open(wc, 'w')

    count = 0

    for root, dirs, files in os.walk(BASE_APK_FOLDER):
        for file in files:
            if file.endswith(EXT):
                count += 1;
                baseline_copy.write(os.path.join(root, file) + "\n")
                working_copy.write(os.path.join(root.replace("BASE_", ""), file) + "\n")

    baseline_copy.close()
    working_copy.close()

    return str(count)