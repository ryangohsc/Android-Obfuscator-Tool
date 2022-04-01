import re
from .utils import *


class DefunctMethodInsertion:
    def open_file(self):
        """
        Opens a file and reads it
        :return f.read():
        """
        directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "modules", "resources",
                                 "defunct_method.txt")
        with open(directory, "r") as f:
            return f.read()

    def run(self, arg_filename):
        """
        Runs the defunct method insertion module
        :param arg_filename:
        :return None.:
        """
        with inplace_edit_file(arg_filename) as (input_file, output_file):
            for line in input_file:
                # place the method above direct methods line in the smali code
                if re.search(r'^([ ]*?)# direct methods', line) is not None:
                    output_file.write(self.open_file())
                else:
                    output_file.write(line)
