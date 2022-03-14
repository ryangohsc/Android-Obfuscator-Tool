import re
from hashlib import md5
from utils import * 


ignore_package_names = []

class_pattern = re.compile(r"\.class.+?(?P<class_name>\S+?;)", re.UNICODE)

method_pattern = re.compile(
	r"\.method.+?(?P<method_name>\S+?)"
	r"\((?P<method_param>\S*?)\)"
	r"(?P<method_return>\S+)",
	re.UNICODE,
)


invoke_pattern = re.compile(
    r"\s+(?P<invoke_type>invoke-\S+)\s"
    r"{(?P<invoke_pass>[vp0-9,.\s]*)},\s"
    r"(?P<invoke_object>\S+?)"
    r"->(?P<invoke_method>\S+?)"
    r"\((?P<invoke_param>\S*?)\)"
    r"(?P<invoke_return>\S+)",
    re.UNICODE,
)




class MethodRename:
	def __init__(self, smali_file_list):
		self.smali_file_list = smali_file_list 
	
	
	def get_android_classes(self):
		f = open(r"C:\Users\tux\Documents\GitHub\ICT-2207-A2\modules\android_classes.txt", "r")  
		android_classes = []
		for line in f:
			android_classes.append(line.strip("\n"))
		return android_classes   


	def rename_method(self, method_name):
		md5_string = md5(method_name.encode()).hexdigest()
		return "m{0}".format(md5_string.lower()[:8])


	def rename_method_declarations(self, class_names_to_ignore, smali_file):
		renamed_methods = set()

		with inplace_edit_file(smali_file) as (in_file, out_file):
			skip_remaining_lines = False
			class_name = None
			for line in in_file:

				if skip_remaining_lines:
					out_file.write(line)
					continue

				if not class_name:
					class_match = class_pattern.match(line)
					# If this is an enum class, don't rename anything.
					if " enum " in line:
						skip_remaining_lines = True
						out_file.write(line)
						continue
					elif class_match:
						class_name = class_match.group("class_name")
						if (class_name in class_names_to_ignore):
							# The methods of this class should be ignored when
							# renaming, so proceed with the next class.
							skip_remaining_lines = True
						out_file.write(line)
						continue

				# Skip virtual methods, consider only the direct methods defined
				# earlier in the file.
				if line.startswith("# virtual methods"):
					skip_remaining_lines = True
					out_file.write(line)
					continue
			

				# Method declared in class.
				method_match = method_pattern.match(line)

				# Avoid constructors, native and abstract methods.
				if (
					method_match
					and "<init>" not in line
					and "<clinit>" not in line
					and " native " not in line
					and " abstract " not in line
				):
					method = "{method_name}({method_param}){method_return}".format(
						method_name=method_match.group("method_name"),
						method_param=method_match.group("method_param"),
						method_return=method_match.group("method_return"),
					)
					# Rename method declaration (invocations of this method will be
					# renamed later).
					method_name = method_match.group("method_name")
					out_file.write(
						line.replace(
							"{0}(".format(method_name),
							"{0}(".format(self.rename_method(method_name)),
						)
					)
					# Direct methods cannot be overridden, so they can be called
					# only by the same class that declares them.
					renamed_methods.add(
						"{class_name}->{method}".format(
							class_name=class_name, method=method
						)
					)
				else:
					out_file.write(line)

		return renamed_methods



	def rename_method_invocations(self, methods_to_rename, smali_file):


		with inplace_edit_file(smali_file) as (in_file, out_file):
			for line in in_file:
				# Method invocation.
				invoke_match = invoke_pattern.match(line)
				if invoke_match:
					method = (
						"{class_name}->"
						"{method_name}({method_param}){method_return}".format(
							class_name=invoke_match.group("invoke_object"),
							method_name=invoke_match.group("invoke_method"),
							method_param=invoke_match.group("invoke_param"),
							method_return=invoke_match.group("invoke_return"),
						)
					)
					invoke_type = invoke_match.group("invoke_type")
					# Rename the method invocation only if is direct or static (we
					# are renaming only direct methods). The list of methods to
					# rename already contains the class name of each method, since
					# here we have a list of methods whose declarations were already
					# renamed.
					if (
						"direct" in invoke_type or "static" in invoke_type
					) and method in methods_to_rename:
						method_name = invoke_match.group("invoke_method")
						out_file.write(
							line.replace(
								"->{0}(".format(method_name),
								"->{0}(".format(self.rename_method(method_name)),
							)
						)
					else:
						out_file.write(line)
				else:
					out_file.write(line)		
	

	def run(self):
		if self.smali_file_list is None:
			return False 
		
		else:
			android_classes = self.get_android_classes()

			# Make a copy of all the smali_files
			# create_backup_smali_files(self.smali_file_path, self.smali_file_list)

			# Operate on each smali file 
			for smali_file in self.smali_file_list:
				renamed_methods = self.rename_method_declarations(android_classes, smali_file) 
				self.rename_method_invocations(renamed_methods, smali_file)

			# Remove backup files 
			# remove_backup_smali_files(self.smali_file_path, self.smali_file_list)

			return True





if __name__ == "__main__":
	smali_files_list = get_smali_files_list("A2_SAMPLE_ALT")
	method_rename = MethodRename(smali_files_list)
	method_rename.run()
	