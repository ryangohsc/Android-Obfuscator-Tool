import re
from .utils import *


class UnconditionalJump:
    def __init__(self):
        self.locals_pattern = re.compile(r"\s+\.locals\s(?P<local_count>\d+)")

    def run(self, arg_filename):
        """
        Runs the unconditional jump module
        :param arg_filename:
        :return: None.
        """
        try:
            with inplace_edit_file(arg_filename) as (input_file, output_file):
                edit_method = False
                for line in input_file:
                    if line.startswith(
                            ".method ") and " abstract " not in line and " native " not in line and not edit_method:
                        # in method
                        output_file.write(line)
                        edit_method = True
                    elif line.startswith(".end method") and edit_method:
                        # at end of method
                        output_file.write("\n\t:zPJwAPOogfLGQLoD\n\n")
                        output_file.write("\tgoto/32 :GpQrBfyCJxjiSUAj\n\n")
                        output_file.write(line)
                        edit_method = False
                    elif edit_method and self.locals_pattern.match(line):
                        # detect .locals in a method
                        output_file.write("\n\tgoto/32 :zPJwAPOogfLGQLoD\n\n")
                        output_file.write("\t:GpQrBfyCJxjiSUAj\n")
                        output_file.write(line)
                    else:
                        output_file.write(line)
        except Exception as e:
            print(e)
