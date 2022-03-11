import os
from .unconditional_jump import UnconditionalJump

def run():

    #
    # Load locations of all smali files
    p = os.path.join("static", "tmp", "smali.txt")
    f = open(p, "r")
    smaliLocations = f.readlines()
    f.close()

    #
    # Do something here for the different modules
    uj = UnconditionalJump()

    for index, line in enumerate(smaliLocations):
        file = line.strip()
        print(file)
        uj.run(file)