import os

def generate(TMP_ASSET_FOLDER, BASE_SMALI_LOC_FILE, WORKING_SMALI_LOC_FILE):

    bl = os.path.join(TMP_ASSET_FOLDER, BASE_SMALI_LOC_FILE)
    baseline_smali_loc_file = open(bl, "r")
    bl_paths = baseline_smali_loc_file.readlines()
    baseline_smali_loc_file.close()

    wc = os.path.join(TMP_ASSET_FOLDER, WORKING_SMALI_LOC_FILE)
    working_samli_loc_file = open(wc, "r")
    wc_paths = working_samli_loc_file.readlines()
    working_samli_loc_file.close()


    for wc_index, wc_file in enumerate(wc_paths):
        for bl_index, bl_file in enumerate(bl_paths):
            if wc_index == bl_index:
                print(str(bl_index + 1) + " " + bl_file + "  " + wc_file)