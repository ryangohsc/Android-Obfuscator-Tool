import re
from hashlib import md5
from .utils import * 

# Global variables 
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
	def get_android_classes(self):
		"""
		Get the list of Android classes from the /resources folder. 
		:param:
		:return android_classes: 
		"""
		cwd = os.getcwd()
		android_classes_path = os.path.join(cwd, "modules", "resources", "android_classes.txt")
		f = open(android_classes_path, "r")  
		android_classes = []
		for line in f:
			android_classes.append(line.strip("\n"))
		return android_classes   

	def rename_method(self, method_name):
		"""
		Renames the method to a randomly generated MD5 name. 
		:param:
		:return "m{0}".format(md5_string.lower()[:8]): 
		"""		
		md5_string = md5(method_name.encode()).hexdigest()
		return "m%s" % md5_string.lower()[:8]

	def rename_method_declarations(self, class_names_to_ignore, smali_file):
		"""
		:param class_names_to_ignore:
		:param smali_file:
		:return renamed_methods: 
		"""
		# Create a set of the methods to be renamed. 
		renamed_methods = set()

		# Open the smali file as two file objects, in_file and out_file. 
		with inplace_edit_file(smali_file) as (in_file, out_file):
			skip_remaining_lines = False
			class_name = None

			# Parse each line in the smali in_file object. 
			for line in in_file:
				# Skip the file if it fails any of the checks as stated below. 
				if skip_remaining_lines:
					out_file.write(line)
					continue

				# Skip the file if it contains an "emum" class.
				if not class_name:
					class_match = class_pattern.match(line)

					# If this is an enum class, don't rename anything.
					if " enum " in line:
						skip_remaining_lines = True
						out_file.write(line)
						continue

					# If the file does not contain an "enum" class.
					elif class_match:
						class_name = class_match.group("class_name")

						# Check that the name of the class is not in the list of classes to ignore. 
						if class_name in class_names_to_ignore:
							skip_remaining_lines = True
						out_file.write(line)
						continue

				# Skip the smali file if it is a virtual method. 
				if line.startswith("# virtual methods"):
					skip_remaining_lines = True
					out_file.write(line)
					continue
			
				# Check that the method is not a constructor, native or abstract method.
				method_match = method_pattern.match(line)

				# Avoid constructors, native and abstract methods.
				not_init = "<init>" not in line
				not_clinit = "<clinit>" not in line
				not_native = " native " not in line
				not_abstract = " abstract " not in line
				if method_match and not_init and not_clinit and not_native and not_abstract:
					method_name = method_match.group("method_name")
					method_param = method_match.group("method_param")
					method_return = method_match.group("method_return")
					method = "%s(%s)%s" % (method_name, method_param, method_return)
					
					# Rename the method declaration.
					method_name = method_match.group("method_name")
					out_file.write(line.replace("%s(" % method_name, "%s(" % self.rename_method(method_name)))
					
					# Direct methods cannot be overridden, so they can be called only by the same class that declares them.
					renamed_methods.add("%s->%s" % (class_name, method))

				# Skip renaming the method if the method is a constructor, native or abstract method.
				else:
					out_file.write(line)

		return renamed_methods

	def rename_method_invocations(self, methods_to_rename, smali_file):
		"""
		:param methods_to_rename:
		:param smali_file:
		:return: None.
		"""
		with inplace_edit_file(smali_file) as (in_file, out_file):
			for line in in_file:
				# Find the method invocation to rename in the smali file.
				invoke_match = invoke_pattern.match(line)
				if invoke_match:
					class_name = invoke_match.group("invoke_object")
					method_name = invoke_match.group("invoke_method")
					method_param = invoke_match.group("invoke_param")
					method_return = invoke_match.group("invoke_return")
					method = "%s->%s(%s)%s" % (class_name, method_name, method_param, method_return)
					invoke_type = invoke_match.group("invoke_type")
					
					# Rename the method invocation only if is direct or static.
					is_direct = "direct" in invoke_type
					is_static = "static" in invoke_type

					if (is_direct or is_static) and method in methods_to_rename:
						method_name = invoke_match.group("invoke_method")
						out_file.write(line.replace("->%s(" % method_name, "->%s(" % self.rename_method(method_name)))
					else:
						out_file.write(line)
				else:
					out_file.write(line)		

	def run(self, arg_filename):
		"""
		Runs the MethodRename functions. 
		:param:
		:return True: 
		:return False: 
		"""		
		# Get the list of all the valid android classes. 
		android_classes = self.get_android_classes()

		# Operate on each smali file. 
		renamed_methods = self.rename_method_declarations(android_classes, arg_filename) 
		self.rename_method_invocations(renamed_methods, arg_filename)
