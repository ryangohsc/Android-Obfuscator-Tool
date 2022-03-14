import re
import secrets
from utils import * 


class Nop:
	def __init__(self, smali_file_list):
		self.smali_file_list = smali_file_list
		self.__valid_nop_op_codes_dir = r"C:\Users\tux\Documents\GitHub\ICT-2207-A2\modules\resources\op_codes.txt"
		self.__op_code_pattern = re.compile(r"\s+(?P<op_code>\S+)")

	def retrieve_valid_nop_op_codes(self):
		op_code_file = open(self.__valid_nop_op_codes_dir, "r") 
		valid_op_codes_list = []
		for line in op_code_file:
			valid_op_codes_list.append(line.strip("\n"))
		return valid_op_codes_list

	def secure_random_number(self):
		secure_rng = secrets.SystemRandom()
		return secure_rng.randrange(3, 9)

	def insert_nop(self, valid_op_codes_list, smali_file):
		with inplace_edit_file(smali_file) as (in_file, out_file):
			for line in in_file:
				out_file.write(line)
				match = self.__op_code_pattern.match(line)
				if match:
					op_code = match.group("op_code")
					if op_code in valid_op_codes_list:
						nop_count = self.secure_random_number()
						out_file.write("\tnop\n" * nop_count)		
		in_file.close()
		out_file.close()
			
	def run(self):
		if self.smali_file_list is None:
			return False 

		else:
			# Retrieve valid op codes 
			valid_op_codes_list = self.retrieve_valid_nop_op_codes()

			# Operate on each smali file 
			for smali_file in self.smali_file_list:
				self.insert_nop(valid_op_codes_list, smali_file)
				
			return True


if __name__ == "__main__":
	smali_files_list = get_smali_files_list("A2_SAMPLE_ALT")
	nop = Nop(smali_files_list) 
	nop.run()
