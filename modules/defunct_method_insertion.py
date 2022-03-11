import re
import utils


class DefunctMethodInsertion:
    def open_file(self):
        """
        Opens a file and reads it
        :return: f.read()
        """
        with open("defunct_method.txt", "r") as f:
            return f.read()

    def run(self, arg_filename):
        try:
            with utils.inplace_edit_file(arg_filename) as (input_file, output_file):
                for line in input_file:
                    if re.search(r'^([ ]*?)# direct methods', line) is not None:
                        output_file.write(self.open_file())
                    else:
                        output_file.write(line)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    test = DefunctMethodInsertion()
    filename = "MainActivity.smali"
    test.run(filename)
