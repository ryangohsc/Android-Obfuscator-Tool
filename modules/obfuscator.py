import os
from .unconditional_jump import UnconditionalJump
from .reordering import Reorder
from .defunct_method_insertion import DefunctMethodInsertion
from .defunct_class_insertion import DefunctClassInsertion
from .arithmetic_branching import ArithmeticBranching


def run():
    #
    # Does not require smali file, but should run first so other modules can obfuscate it
    dci = DefunctClassInsertion()
    dci.run()
    #
    # Load locations of all smali files
    p = os.path.join("static", "tmp", "smali.txt")
    f = open(p, "r")
    smali_locations = f.readlines()
    f.close()

    #
    # Do something here for the different modules
    uj = UnconditionalJump()
    ro = Reorder()
    dmi = DefunctMethodInsertion()
    ab = ArithmeticBranching()

    for index, line in enumerate(smali_locations):
        file = line.strip()
        print(file)
        dmi.run(file)  # should run second so other modules can obfuscate it
        uj.run(file)
        ab.run(file)
        ro.run(file)  # should run last
