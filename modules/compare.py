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


    if bl_len and wc_len is not 0:
        if (wc_len - bl_len) is 1:

            #
            # For all files that that existed beforehand
            for index in range(bl_len):
                print(bl_paths[index].strip() + "\n" + wc_paths[index].strip() + "\n")

            #
            # For defunct_class_insertion comparision
            empty_file = open(os.path.join(TMP_ASSET_FOLDER, ".ignore"), 'r')
            dci_file = open(wc_paths[-1].strip(), "r")

            compare = difflib.HtmlDiff(wrapcolumn=120)
            html = compare.make_file(empty_file , dci_file)

            hf = os.path.join(TMP_ASSET_FOLDER, "defunct_class_insertion.html")
            with open(hf, 'w') as fh:
                fh.write(html)

            empty_file.close()
            dci_file.close()