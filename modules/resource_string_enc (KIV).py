import logging
import os
import re
import xml.etree.cElementTree as Xml
from binascii import hexlify
from utils import * 

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad



def encrypt_string(string_to_encrypt):
	string_to_encrypt = string_to_encrypt.encode(errors="replace").decode("unicode_escape")

	key = PBKDF2(
		password=encryption_secret,
		salt=encryption_secret.encode(),
		dkLen=32,
		count=128,
	)

	encrypted_string = hexlify(
		AES.new(key=key, mode=AES.MODE_ECB).encrypt(
			pad(string_to_encrypt.encode(errors="replace"), AES.block_size)
		)
	).decode()
	return encrypted_string


def encrypt_string_resources(string_resources_xml_file, string_names_to_encrypt):
	xml_parser = Xml.XMLParser(encoding="utf-8")
	xml_tree = Xml.parse(string_resources_xml_file, parser=xml_parser)

	for xml_string in xml_tree.iter("string"):
		string_name = xml_string.get("name", None)
		string_value = xml_string.text
		if string_name and string_value and string_name in string_names_to_encrypt:
			encrypted_string_value = self.encrypt_string(string_value)
			xml_string.text = encrypted_string_value

	xml_tree.write(string_resources_xml_file, encoding="utf-8")


def encrypt_string_array_resources(string_array_resources_xml_file, string_array_names_to_encrypt):
	xml_parser = Xml.XMLParser(encoding="utf-8")
	xml_tree = Xml.parse(string_array_resources_xml_file, parser=xml_parser)

	for xml_string_array in xml_tree.iter("string-array"):
		string_array_name = xml_string_array.get("name", None)
		if string_array_name and string_array_name in string_array_names_to_encrypt:
			for item in xml_string_array.iter("item"):
				if item.text:
					encrypted_string_value = self.encrypt_string(item.text)
					item.text = encrypted_string_value

	xml_tree.write(string_array_resources_xml_file, encoding="utf-8")



encryption_secret = "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"

string_res_field_pattern = re.compile(
	r"\.field\spublic\sstatic\sfinal\s(?P<string_name>\S+?):I\s=\s"
	r"(?P<string_id>[0-9a-fA-FxX]+)",
	re.UNICODE,
)

string_id_pattern = re.compile(
	r"\s+const\s(?P<register>[vp0-9]+),\s(?P<id>\S+)"
)

string_array_id_pattern = re.compile(
	r"\s+const/high16\s(?P<register>[vp0-9]+),\s(?P<id>\S+)"
)

load_string_res_pattern = re.compile(
	r"\s+invoke-virtual\s"
	r"{[vp0-9]+,\s(?P<param_register>[vp0-9]+)},\s"
	r"(Landroid/content/res/Resources;->getString\(I\)Ljava/lang/String;"
	r"|Landroid/content/Context;->getString\(I\)Ljava/lang/String;)"
)

load_string_array_res_pattern = re.compile(
	r"\s+invoke-virtual\s"
	r"{[vp0-9]+,\s(?P<param_register>[vp0-9]+)},\s"
	r"Landroid/content/res/Resources;->"
	r"getStringArray\(I\)\[Ljava/lang/String;"
)

move_result_obj_pattern = re.compile(
	r"\s+move-result-object\s(?P<register>[vp0-9]+)"
)


locals_pattern = re.compile(r"\s+\.locals\s(?P<local_count>\d+)")

encrypted_res_strings = set()
encrypted_res_string_arrays = set()



string_id_to_string_name = {}
string_array_id_to_string_name = {}
smali_files_list = get_smali_files_list("A2_SAMPLE_ALT")


def test():
	for smali_file in smali_files_list:
		if smali_file.endswith("R$string.smali"):
			with open(smali_file, "r", encoding="utf-8") as current_file:
				for line in current_file:
					if line.startswith(".method "):
						# Method declaration reached, no more field declarations
						# from now on.
						break
					field_match = string_res_field_pattern.match(line)
					if field_match:
						# String name and id declaration.
						string_id_to_string_name[
							field_match.group("string_id")
						] = field_match.group("string_name")

		elif smali_file.endswith("R$array.smali"):
			with open(smali_file, "r", encoding="utf-8") as current_file:
				for line in current_file:
					if line.startswith(".method "):
						# Method declaration reached, no more field declarations
						# from now on.
						break
					field_match = string_res_field_pattern.match(line)
					if field_match:
						# String array name and id declaration.
						string_array_id_to_string_name[
							field_match.group("string_id")
						] = field_match.group("string_name")
	return string_id_to_string_name, string_array_id_to_string_name


def test2(string_id_to_string_name, string_array_id_to_string_name):
	for smali_file in smali_files_list:
		with open(smali_file, "r", encoding="utf-8") as current_file:
			lines = current_file.readlines()
			
		# Line numbers where a string is loaded from resources.
		string_index = []

		# Registers containing the strings loaded from resources.
		string_register = []

		# The number of local registers in the method where a string resource
		# is loaded.
		string_local_count = []

		# Line numbers where a string array is loaded from resources.
		string_array_index = []

		# Registers containing the string arrays loaded from resources.
		string_array_register = []

		# The number of local registers in the method where a string array
		# resource is loaded.
		string_array_local_count = []

		# Look for resource strings that can be encrypted.
		current_local_count = 0
		for line_number, line in enumerate(lines):
			match = locals_pattern.match(line)
			if match:
				current_local_count = int(match.group("local_count"))
				continue

			string_res_match = load_string_res_pattern.match(line)
			if string_res_match:
				string_index.append(line_number)
				string_register.append(string_res_match.group("param_register"))
				string_local_count.append(current_local_count)
				continue

			string_array_res_match = load_string_array_res_pattern.match(line)
			if string_array_res_match:
				string_array_index.append(line_number)
				string_array_register.append(
					string_array_res_match.group("param_register")
				)
				string_array_local_count.append(current_local_count)
	


		# Iterate the lines backwards (until the method declaration is reached)
		# and find the id of each string resource.
		for string_number, index in enumerate(string_index):
			for line_number in range(index - 1, 0, -1):
				if lines[line_number].startswith(".method "):
					string_index[string_number] = -1
					break

				id_match = string_id_pattern.match(lines[line_number])
				if (id_match and id_match.group("register") == string_register[string_number]):
					if id_match.group("id") in string_id_to_string_name:
						encrypted_res_strings.add(string_id_to_string_name[id_match.group("id")])
					break

		# Iterate the lines backwards (until the method declaration is reached)
		# and find the id of each string array resource.
		for string_array_number, index in enumerate(string_array_index):
			for line_number in range(index - 1, 0, -1):
				if lines[line_number].startswith(".method "):
					string_array_index[string_array_number] = -1
					break

				id_match = string_array_id_pattern.match(lines[line_number])
				if (id_match and id_match.group("register") == string_array_register[string_array_number]):
					if id_match.group("id") in string_array_id_to_string_name:
						encrypted_res_string_arrays.add(string_array_id_to_string_name[id_match.group("id")])
					break

		# After each string resource is loaded, decrypt it (the string resource
		# will be encrypted directly in the xml file).
		for string_number, index in enumerate(i for i in string_index if i != -1):
			for line_number in range(index + 1, len(lines)):
				if lines[line_number].startswith(".end method"):
					break

				move_result_match = move_result_obj_pattern.match(lines[line_number])
				if move_result_match:
					reg_type = move_result_match.group("register")[:1]
					reg_number = int(move_result_match.group("register")[1:])
					if (reg_type == "v" and reg_number <= 15) or (
						reg_type == "p"
						and reg_number + string_local_count[string_number] <= 15
					):
						# Add string decrypt instruction.
						lines[line_number] += (
							"\n\tinvoke-static {{{register}}}, "
							"Lcom/decryptstringmanager/DecryptString;->"
							"decryptString(Ljava/lang/String;)"
							"Ljava/lang/String;\n\n".format(
								register=move_result_match.group("register")
							)
							+ lines[line_number]
						)

					# Proceed with the next string resource (if any).
					break

		# After each string array resource is loaded, decrypt it (the string
		# array resource will be encrypted directly in the xml file).
		for string_array_number, index in enumerate(i for i in string_array_index if i != -1):
			for line_number in range(index + 1, len(lines)):
				if lines[line_number].startswith(".end method"):
					break

				move_result_match = move_result_obj_pattern.match(lines[line_number])
				if move_result_match:
					reg_type = move_result_match.group("register")[:1]
					reg_number = int(move_result_match.group("register")[1:])
					if (reg_type == "v" and reg_number <= 15) or (
						reg_type == "p"
						and reg_number
						+ string_array_local_count[string_array_number]
						<= 15
					):
						# Add string array decrypt instruction.
						lines[line_number] += (
							"\n\tinvoke-static {{{register}}}, "
							"Lcom/decryptstringmanager/DecryptString;->"
							"decryptStringArray([Ljava/lang/String;)"
							"[Ljava/lang/String;\n\n".format(
								register=move_result_match.group("register")
							)
							+ lines[line_number]
						)

					# Proceed with the next string array resource (if any).
					break

		with open(smali_file, "w", encoding="utf-8") as current_file:
			current_file.writelines(lines)


	# Encrypt the strings and the string arrays in the resource files.
	resource_directory = r"C:\Users\tux\Documents\GitHub\ICT-2207-A2\dumpster\A2_SAMPLE_ALT\res"

	strings_xml_path = os.path.join(resource_directory, "values", "strings.xml")
	string_arrays_xml_path = os.path.join(resource_directory, "values", "arrays.xml")

	if os.path.isfile(strings_xml_path):
		encrypt_string_resources(strings_xml_path, encrypted_res_strings)

	if os.path.isfile(string_arrays_xml_path):
		encrypt_string_array_resources(
			string_arrays_xml_path, encrypted_res_string_arrays
		)



	if encrypted_res_strings or encrypted_res_string_arrays:
		# Add to the app the code for decrypting the encrypted strings. The code
		# for decrypting can be put in any smali directory, since it will be
		# moved to the correct directory when rebuilding the application.
		destination_dir = r"C:\Users\tux\Documents\GitHub\ICT-2207-A2\dumpster\agent\smali"
		destination_file = os.path.join(destination_dir, "DecryptString.smali")
		with open(destination_file, "w", encoding="utf-8") as decrypt_string_smali:
			decrypt_string_smali.write(encryption_secret)


string_id_to_string_name, string_array_id_to_string_name = test()
test2(string_id_to_string_name, string_array_id_to_string_name)






