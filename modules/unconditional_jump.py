import re
from .utils import *

# Global variables
LOCALS_PATTERN = re.compile(r"\s+\.locals\s(?P<local_count>\d+)")


class UnconditionalJump:
    def check_non_abstract(self, arg_line):
        """
        Checks for non-abstract methods
        :param arg_line:
        :return True:
        :return False:
        """
        if arg_line.startswith(".method ") and " abstract " not in arg_line and " native " not in arg_line:
            return True
        return False

    def run(self, arg_filename):
        """
        Runs the unconditional jump module
        :param arg_filename:
        :return None:
        """
        edit_method = False
        with inplace_edit_file(arg_filename) as (input_file, output_file):
            for line in input_file:
                # check for non-abstract or native methods
                if self.check_non_abstract(line) and not edit_method:
                    # in method
                    output_file.write(line)
                    edit_method = True
                elif line.startswith(".end method") and edit_method:
                    # at end of method
                    output_file.write("\n\t:zPJwAPOogfLGQLoD\n\n")
                    output_file.write("\tgoto/32 :GpQrBfyCJxjiSUAj\n\n")
                    output_file.write(line)
                    edit_method = False
                elif edit_method and LOCALS_PATTERN.match(line):
                    # detect .locals in a method
                    output_file.write("\n\tgoto/32 :zPJwAPOogfLGQLoD\n\n")
                    output_file.write("\t:GpQrBfyCJxjiSUAj\n")
                    output_file.write(line)
                else:
                    output_file.write(line)
