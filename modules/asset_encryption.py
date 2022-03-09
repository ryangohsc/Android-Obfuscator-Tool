import random
import string
import os 
import fnmatch


# def get_lines(file_name):
#     try:
#         with open(file_name, "r", encoding="utf-8") as file:
#             # Return a list with the non blank lines contained in the file.
#             return list(filter(None, (line.rstrip() for line in file)))
#     except Exception as e:
#         pass 


# def get_class_names():
#     return get_lines(
#         os.path.join(
#             os.path.dirname(__file__), "resources", "android_class_names_api_27.txt"
#         )
#     )


# Get the Smali files 
# Parse them for the methods 
# Rename the methods 


def get_smali_files():
smali_files = [os.path.join(root, file_name)
                for root, dir_names, file_names in os.walk(self._decoded_apk_path)
                for file_name in file_names
                if file_name.endswith(".smali")] 

print(smali_files)








# class_names = set(get_class_names())
