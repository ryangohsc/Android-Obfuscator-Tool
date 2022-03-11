import os
import random
import string
import re


class DefunctClassInsertion:
    def get_smali_folders(self):
        """
        Gets all main smali folders
        :return: smali_folder_list
        """
        smali_folder_list = []
        extracted_apk_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dumpster")
        for root, subdirs, files in os.walk(extracted_apk_folder):
            for folders in subdirs:
                if "smali" in folders:
                    x = os.path.join(root, folders)
                    smali_folder_list.append(x)
        return smali_folder_list

    def get_end_path(self):
        """
        Gets all final subdirectories where the smali files reside
        :return: final_list
        """
        final_subdir_list = []
        folder_list = self.get_smali_folders()
        for i in folder_list:
            for root, subdirs, files in os.walk(i):
                for file in files:
                    if file.endswith(".smali"):
                        x = os.path.join(root, file)
                        x = os.path.dirname(x)
                        final_subdir_list.append(x)
        final_list = list(set(final_subdir_list))
        return final_list

    def random_string(self):
        """
        Returns a cryptographically secure random string
        :return:
        """
        return ''.join(random.SystemRandom().choice(string.ascii_letters) for _ in range(16))

    def open_file(self):
        """
        Opens a file and reads it
        :return: f.read()
        """
        directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "modules", "defunct_class.txt")
        with open(directory, "r") as f:
            return f.read()

    def run(self):
        all_paths = self.get_end_path()
        for path in all_paths:
            class_name = re.sub(r'^.*?smali.', '', path)
            class_name = re.sub(r'^.*?classes[0-9].', '', class_name)
            class_name = class_name.replace("\\", "/")
            defunct_class = self.open_file()
            random_name = self.random_string()
            defunct_class = defunct_class.replace("*ClassName*", class_name + "/" + random_name)
            defunct_class = defunct_class.replace("*String1*", self.random_string())
            defunct_class = defunct_class.replace("*String2*", self.random_string())
            defunct_class = defunct_class.replace("*MethodName*", self.random_string())
            defunct_class = defunct_class.replace("*SourceName*", self.random_string())
            write_name = os.path.join(path, random_name + ".smali")
            with open(write_name, "w") as f:
                f.write(defunct_class)

