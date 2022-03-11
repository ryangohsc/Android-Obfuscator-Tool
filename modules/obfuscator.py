from .unconditional_jump import UnconditionalJump

def run():

    #
    # Load locations of all smali files
    f = open("static/tmp/smali.txt", "r")
    smaliLocations = f.readlines()
    f.close()

    #
    # Do something here for the different modules
    uj = UnconditionalJump()

    for index, line in enumerate(smaliLocations):
        file = line.strip()
        print(file)
        uj.run(file)