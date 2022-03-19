import re
import secrets
from .utils import * 

# Global variables 
op_code_pattern = re.compile(r"\s+(?P<op_code>\S+)")


class Nop:
	def retrieve_valid_nop_op_codes(self):
		"""
		Retrieves a lst of valid no op codes from a .txt file in the /resources folder.
		:param:
		:return valid_op_codes_list: 
		"""
		cwd = os.getcwd()
		op_code_file_path = os.path.join(cwd, "modules", "resources", "op_codes.txt")
		op_code_file = open(op_code_file_path, "r") 
		valid_op_codes_list = []
		for line in op_code_file:
			valid_op_codes_list.append(line.strip("\n"))
		op_code_file.close()
		return valid_op_codes_list

	def secure_random_number(self):
		"""
		Generates a random secure number. 
		:param:
		:return secure_rng.randrange(3, 9): 
		"""
		secure_rng = secrets.SystemRandom()
		return secure_rng.randrange(3, 9)

	def insert_nop(self, valid_op_codes_list, smali_file):
		"""
		Insert "NOPs" to make the code less readable. 
		:param valid_op_codes_list:
		:param smali_file:
		:return: 
		"""
		# Open the smali file as two file objects, in_file and out_file. 
		with inplace_edit_file(smali_file) as (in_file, out_file):
			for line in in_file:
				out_file.write(line)
				match = op_code_pattern.match(line)

				# If match a valid  op code, add NOPs to it. 
				if match:
					op_code = match.group("op_code")
					if op_code in valid_op_codes_list:
						nop_count = self.secure_random_number()
						out_file.write("\tnop\n" * nop_count)
			
	def run(self, arg_filename):
		"""
		Runs the insert nop function. 
		:param:
		:return True: 
		:return False: 
		"""
		# Retrieve valid op codes 
		valid_op_codes_list = self.retrieve_valid_nop_op_codes()

		# Operate on each smali file 
		self.insert_nop(valid_op_codes_list, arg_filename)
			