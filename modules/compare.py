import os, difflib

def generate(TMP_ASSET_FOLDER, BASE_SMALI_LOC_FILE, WORKING_SMALI_LOC_FILE):
    bl = os.path.join(TMP_ASSET_FOLDER, BASE_SMALI_LOC_FILE)
    baseline_smali_loc_file = open(bl, "r")
    bl_paths = baseline_smali_loc_file.readlines()
    bl_len = len(bl_paths)
    baseline_smali_loc_file.close()

    wc = os.path.join(TMP_ASSET_FOLDER, WORKING_SMALI_LOC_FILE)
    working_samli_loc_file = open(wc, "r")
    wc_paths = working_samli_loc_file.readlines()
    wc_len = len(wc_paths)
    working_samli_loc_file.close()

    if bl_len and wc_len != 0:
        #
        # For all files that that existed beforehand
        for index in range(bl_len):
            createHTML(TMP_ASSET_FOLDER,
                        bl_paths[index].strip(),
                        wc_paths[index].strip(),
                        index+1,
                        60)
        #
        # For defunct_class_insertion comparison
        defunct_classes = wc_len - bl_len + 1
        for index in range(1, defunct_classes):
            createHTML(TMP_ASSET_FOLDER,
                        os.path.join(TMP_ASSET_FOLDER, ".ignore"),
                        wc_paths[bl_len+index-1].strip(),
                        bl_len+index,
                        120)
    return wc_len

def createHTML(TMP_ASSET_FOLDER, BASE_FILE, MODIFIED_FILE, COUNT, WRAP):
    COUNT = str(COUNT)
    base_file = open(BASE_FILE, 'r')
    modified_file = open(MODIFIED_FILE, "r")

    compare = difflib.HtmlDiff(wrapcolumn=WRAP)
    html = compare.make_file(base_file, modified_file)

    hf = os.path.join(TMP_ASSET_FOLDER, COUNT + ".html")
    with open(hf, 'w') as fh:
        fh.write(html)

    base_file.close()
    modified_file.close()

def loadHTMLSelect(TMP_ASSET_FOLDER, WORKING_FOLDER, WORKING_SMALI_LOC_FILE, APK_NAME):
    file = os.path.join(TMP_ASSET_FOLDER, WORKING_SMALI_LOC_FILE)
    f = open(file, 'r')
    truncatePath = os.path.join(WORKING_FOLDER, APK_NAME.replace(".apk", ""))
    selectListData = {0: "NULL"}
    for index, path in enumerate(f):
        selectListData[index+1] = path.strip().replace(truncatePath, "")
    f.close()
    return selectListData