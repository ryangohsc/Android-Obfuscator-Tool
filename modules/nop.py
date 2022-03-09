import re
import random 




def get_nop_valid_op_codes():
	f = open(r"C:\Users\tux\Documents\GitHub\ICT-2207-A2\modules\op_codes.txt", "r") 
	valid_op_codes = []
	for line in f:
		valid_op_codes.append(line.strip("\n"))
	return valid_op_codes



f = open(r"C:\Users\tux\Documents\GitHub\ICT-2207-A2\modules\MainActivity.smali", "r")
f1 = open(r"C:\Users\tux\Documents\GitHub\ICT-2207-A2\modules\uwu.smali", "w")
op_codes = get_nop_valid_op_codes()
pattern = re.compile(r"\s+(?P<op_code>\S+)")


for line in f:
	f1.write(line)
	match = pattern.match(line)
	if match:
		op_code = match.group("op_code")
		if op_code in op_codes:
			nop_count = random.randint(3, 9)
			f1.write("\tnop\n" * nop_count)

