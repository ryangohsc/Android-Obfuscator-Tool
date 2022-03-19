import os
import random
import string
import re


class DefunctClassInsertion:
    def get_smali_folders(self, working_copy_dir):
        """
        Gets all main smali folders
        :param working_copy_dir:
        :return smali_folder_list:
        """
        smali_folder_list = []
        extracted_apk_folder = working_copy_dir
        for root, subdirs, files in os.walk(extracted_apk_folder):
            for folders in subdirs:
                if "smali" in folders:
                    x = os.path.join(root, folders)
                    smali_folder_list.append(x)
        return smali_folder_list

    def get_end_path(self, working_copy_dir):
        """
        Gets all final subdirectories where the smali files reside
        :param working_copy_dir:
        :return final_list:
        """
        final_subdir_list = []
        folder_list = self.get_smali_folders(working_copy_dir)
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
        :return ''.join(random.SystemRandom().choice(string.ascii_letters) for _ in range(16)):
        """
        return ''.join(random.SystemRandom().choice(string.ascii_letters) for _ in range(16))

    def open_file(self):
        """
        Opens a file and reads it
        :return f.read():
        """
        directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "modules", "resources",
                                 "defunct_class.txt")
        with open(directory, "r") as f:
            return f.read()

    def append_to_text(self, file_path, random_name):
        """
        Appends generated files to smali.txt
        :param random_name:
        :param file_path:
        :return None:
        """
        p = os.path.join("static", "tmp", "smali.txt")
        with open(p, 'a') as f:
            f.write(file_path + "\n")

        n = os.path.join("static", "tmp", "newfiles.txt")
        with open(n, 'a') as o:
            o.write(random_name + ".smali" + "\n")

    def run(self, working_copy_dir):
        """
        Runs the defunct class insertion module
        :param working_copy_dir:
        :return None:
        """
        all_paths = self.get_end_path(working_copy_dir)
        for path in all_paths:
            class_name = re.sub(r'^.*?smali.', '', path)
            class_name = re.sub(r'^.*?classes[0-9].', '', class_name)
            class_name = class_name.replace("\\", "/")
            defunct_class = self.open_file()
            random_name = self.random_string()
            # replace placeholders in the smali code
            defunct_class = defunct_class.replace("*ClassName*", class_name + "/" + random_name)
            defunct_class = defunct_class.replace("*String1*", self.random_string())
            defunct_class = defunct_class.replace("*String2*", self.random_string())
            defunct_class = defunct_class.replace("*MethodName*", self.random_string())
            defunct_class = defunct_class.replace("*SourceName*", self.random_string())
            write_name = os.path.join(path, random_name + ".smali")
            # create the smali file
            smali_path = re.sub("^(.*)(?=dumpster)", "", write_name)
            with open(write_name, "w") as f:
                f.write(defunct_class)
                self.append_to_text(smali_path, random_name)
