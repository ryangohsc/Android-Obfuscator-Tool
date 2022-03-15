import os
from .unconditional_jump import UnconditionalJump
from .reordering import Reorder
from .defunct_method_insertion import DefunctMethodInsertion
from .defunct_class_insertion import DefunctClassInsertion
from .arithmetic_branching import ArithmeticBranching
from .nop import Nop
from .method_rename import MethodRename
from .variable_rename import VariableRename


def run(TMP_ASSET_FOLDER, WORKING_FOLDER, APK_NAME):
    WORKING_SMALI_LOC_FILE = "smali.txt"
    WORKING_COPY_DIR = os.path.join(WORKING_FOLDER, APK_NAME.replace('.apk', ''))

    #
    # Does not require smali file, but should run first so other modules can obfuscate it
    dci = DefunctClassInsertion()
    dci.run(WORKING_COPY_DIR)
    #
    # Load locations of all smali files
    p = os.path.join(TMP_ASSET_FOLDER, WORKING_SMALI_LOC_FILE)
    f = open(p, "r")
    smali_locations = f.readlines()
    f.close()

    #
    # Do something here for the different modules
    uj = UnconditionalJump()
    ro = Reorder()
    dmi = DefunctMethodInsertion()
    ab = ArithmeticBranching()
    nop = Nop()
    method_rename = MethodRename()
    variable_rename = VariableRename()

    for index, line in enumerate(smali_locations):
        file = line.strip()
        print(file)
        dmi.run(file)  # should run second so other modules can obfuscate it
        uj.run(file)
        ab.run(file)
        nop.run(file)
        method_rename.run(file)
        variable_rename.run(file)
        ro.run(file)  # should run last
