import re 
from .utils import * 
from hashlib import md5


class VariableRename:	
	def generate_md5_string(self, string_to_hash):
		"""
		Generates a random MD5 string. 
		:param:
		:return md5_string: 
		"""
		md5_string = md5(string_to_hash.encode()).hexdigest()[:8]
		return md5_string

	def rename_variable(self, smali_file):
		"""
		Reanmes variables in the smali file to a randomly generated MD5 string. 
		:param smali_file:
		:return: 
		"""
		with inplace_edit_file(smali_file) as (in_file, out_file):
			for line in in_file:
				matches = re.findall(r'(?:(?<=\.local|\.param))(\s\w+,)\s\"(.*?)\"', line)
				if matches != []:
					replacement_name = '"%s"' % self.generate_md5_string(matches[0][1]) 
					original_name = '"%s"' % matches[0][1]
					line = re.sub(original_name, replacement_name, line)
				out_file.write(line)

		in_file.close()
		out_file.close()			

	def run(self, arg_filename):
		"""
		Runs the variable rename function. 
		:param arg_filename:
		"""
		self.rename_variable(arg_filename) 
