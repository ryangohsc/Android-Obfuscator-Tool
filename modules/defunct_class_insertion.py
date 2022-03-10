import os
import random
import string
import re


class DefunctClassInsertion:
    def __init__(self):
        pass

    def get_smali_folders(self):
        test_list = []
        test = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dumpster")
        for root, subdirs, files in os.walk(test):
            for folders in subdirs:
                if "smali" in folders:
                    x = os.path.join(root, folders)
                    test_list.append(x)
        return test_list

    def get_end_path(self):
        final_list = []
        folder_list = self.get_smali_folders()
        for i in folder_list:
            for root, subdirs, files in os.walk(i):
                for file in files:
                    if file.endswith(".smali"):
                        x = os.path.join(root, file)
                        x = os.path.dirname(x)
                        final_list.append(x)
        final_list = list(set(final_list))
        print(final_list)
        return final_list

    def random_string(self):
        """
        Returns a cryptographically secure random string
        :return:
        """
        return ''.join(random.SystemRandom().choice(string.ascii_letters) for _ in range(16))

    def open_file(self):
        with open("defunct_class.txt", "r") as f:
            return f.read()

    def run(self):
        all_paths = self.get_end_path()
        for path in all_paths:
            class_name = re.sub(r'^.*?smali.', '', path)
            class_name = re.sub(r'^.*?classes[0-9].', '', class_name)
            class_name = class_name.replace("\\", "/")
            print(class_name)
            defunct_class = self.open_file()
            random_name = self.random_string()
            defunct_class = defunct_class.replace("*ClassName*", class_name + "/" + random_name)
            defunct_class = defunct_class.replace("*String1*", self.random_string())
            defunct_class = defunct_class.replace("*String2*", self.random_string())
            defunct_class = defunct_class.replace("*MethodName*", self.random_string())
            defunct_class = defunct_class.replace("*SourceName*", self.random_string())
            print(defunct_class)
            write_name = os.path.join(path, random_name + ".smali")
            print(write_name)
            with open(write_name, "w") as f:
                f.write(defunct_class)


if __name__ == "__main__":
    test = DefunctClassInsertion()
    test.run()
