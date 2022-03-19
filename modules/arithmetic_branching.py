import random
import re
import secrets
import string
from .utils import *


class ArithmeticBranching:
    def __init__(self):
        self.locals_pattern = re.compile(r"\s+\.locals\s(?P<local_count>\d+)")

    def random_number(self):
        """
        Returns a cryptographically secure random number between 1 and 16
        :return:
        """
        secure_rng = secrets.SystemRandom()
        return secure_rng.randrange(1, 16)

    def random_string(self):
        """
        Returns a cryptographically secure random string
        :return:
        """
        return ''.join(random.SystemRandom().choice(string.ascii_letters) for _ in range(16))

    def run(self, arg_filename):
        """
        Run the arithmetic branching module
        :param arg_filename:
        :return: None.
        """
        edit_method = False
        start_label = None
        end_label = None
        try:
            with inplace_edit_file(arg_filename) as (input_file, output_file):
                for line in input_file:
                    # check for non-abstract or native methods
                    if line.startswith(
                            ".method ") and " abstract " not in line and " native " not in line and not edit_method:
                        # in a method, can edit
                        output_file.write(line)
                        edit_method = True
                    elif line.startswith(".end method") and edit_method:
                        # end of method and disable edit
                        if start_label and end_label:
                            output_file.write("\t:%s\n" % end_label)
                            output_file.write("\tgoto/32 :%s\n" % start_label)
                            start_label = None
                            end_label = None
                        output_file.write(line)
                        edit_method = False
                    elif edit_method:
                        output_file.write(line)
                        match = self.locals_pattern.match(line)
                        # check if local count is 2, means 2 registers is available, then can do arithmetic branching
                        if match and int(match.group("local_count")) >= 2:
                            # generate random number and strings
                            first_num = self.random_number()
                            second_num = self.random_number()
                            start_label = self.random_string()
                            end_label = self.random_string()
                            tmp_label = self.random_string()
                            output_file.write("\n\tconst v0, %s\n" % first_num)
                            output_file.write("\tconst v1, %s\n" % second_num)
                            output_file.write("\tadd-int v0, v0, v1\n")
                            output_file.write("\trem-int v0, v0, v1\n")
                            output_file.write("\tif-gtz v0, :%s\n" % tmp_label)
                            output_file.write("\tgoto/32 :%s\n" % end_label)
                            output_file.write("\t:%s\n" % tmp_label)
                            output_file.write("\t:%s\n" % start_label)
                    else:
                        output_file.write(line)
        except Exception as e:
            print(e)
