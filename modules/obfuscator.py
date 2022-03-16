import os
from .unconditional_jump import UnconditionalJump
from .reordering import Reorder
from .defunct_method_insertion import DefunctMethodInsertion
from .defunct_class_insertion import DefunctClassInsertion
from .arithmetic_branching import ArithmeticBranching
from .nop import Nop
from .method_rename import MethodRename
from .variable_rename import VariableRename


def run(TMP_ASSET_FOLDER, WORKING_FOLDER, APK_NAME, OBFUSCATION_METHODS):
    """
    Trigger point for obfuscation functions
    :return: NIL
    """
    WORKING_SMALI_LOC_FILE = "smali.txt"
    WORKING_COPY_DIR = os.path.join(WORKING_FOLDER, APK_NAME.replace('.apk', ''))

    #
    # Does not require smali file, but should run first so other modules can obfuscate it
    # Function will always run regardless of user choice
    dci = DefunctClassInsertion()
    dci.run(WORKING_COPY_DIR)
    OBFUSCATION_METHODS.pop("dci")

    #
    # Load locations of all smali files
    p = os.path.join(TMP_ASSET_FOLDER, WORKING_SMALI_LOC_FILE)
    f = open(p, "r")
    smali_locations = f.readlines()
    f.close()

    #
    # Do something here for the different modules
    dmi = DefunctMethodInsertion()
    uj = UnconditionalJump()
    ab = ArithmeticBranching()
    # nop = Nop()
    method_rename = MethodRename()
    variable_rename = VariableRename()
    ro = Reorder()

    for index, line in enumerate(smali_locations):
        file = line.strip()
        if OBFUSCATION_METHODS["dmi"]: dmi.run(file)  # should run second so other modules can obfuscate it
        if OBFUSCATION_METHODS["uj"]: uj.run(file)
        if OBFUSCATION_METHODS["ab"]: ab.run(file)
        # if OBFUSCATION_METHODS["nop"]: nop.run(file)
        if OBFUSCATION_METHODS["method_rename"]: method_rename.run(file)
        if OBFUSCATION_METHODS["variable_rename"]: variable_rename.run(file)
        if OBFUSCATION_METHODS["ro"]: ro.run(file)  # should run last
