import string
import random
from .utils import *
import re
from typing import List


class Reorder:
    def __init__(self):
        # for inversion
        self.control_flow_map = {
            "if-eq": "if-ne",
            "if-ne": "if-eq",
            "if-lt": "if-ge",
            "if-ge": "if-lt",
            "if-gt": "if-le",
            "if-le": "if-gt",
            "if-eqz": "if-nez",
            "if-nez": "if-eqz",
            "if-ltz": "if-gez",
            "if-gez": "if-ltz",
            "if-gtz": "if-lez",
            "if-lez": "if-gtz"
        }

    def random_string(self):
        """
        Returns a cryptographically secure random string
        :return:
        """
        return ''.join(random.SystemRandom().choice(string.ascii_letters) for _ in range(16))

    def open_file(self):
        """
        Opens a file and reads it
        :return: lines
        """
        directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "modules", "resources",
                                 "op_codes.txt")
        with open(directory, "r") as f:
            lines = f.read().splitlines()
            return lines

    def run(self, arg_filename):
        """
        Runs the Reordering module
        :param arg_filename:
        :return: None.
        """
        op_codes = self.open_file()
        try:
            op_code_pattern = re.compile(r"\s+(?P<op_code>\S+)")
            if_pattern = re.compile(
                r"\s+(?P<if_op_code>\S+)"
                r"\s(?P<register>[vp0-9,\s]+?),\s:(?P<goto_label>\S+)"
            )
            with inplace_edit_file(arg_filename) as (input_file, output_file):
                edit_method = False
                inside_try_catch = False
                jump_count = 0
                for line in input_file:
                    if line.startswith(
                            ".method ") and " abstract " not in line and " native " not in line and not edit_method:
                        # in method
                        output_file.write(line)
                        edit_method = True
                        inside_try_catch = False
                        jump_count = 0
                    elif line.startswith(".end method") and edit_method:
                        # end of method
                        output_file.write(line)
                        edit_method = False
                        inside_try_catch = False
                    elif edit_method:
                        match = op_code_pattern.match(line)
                        if match:
                            op_code = match.group("op_code")
                            if op_code.startswith(":try_start_"):
                                output_file.write(line)
                                inside_try_catch = True
                            elif op_code.startswith(":try_end_"):
                                output_file.write(line)
                                inside_try_catch = False
                            elif op_code in op_codes and not inside_try_catch:
                                # define a block of code
                                jump_name = self.random_string()
                                output_file.write("\tgoto/32 :l_%s_%s\n\n" % (jump_name, jump_count))
                                output_file.write("\tnop\n\n")
                                output_file.write("#!block!#\n")
                                output_file.write("\t:l_%s_%s\n" % (jump_name, jump_count))
                                jump_count += 1
                                new_if = self.control_flow_map.get(op_code, None)
                                if new_if:
                                    if_match = if_pattern.match(line)
                                    random_label_name = self.random_string()
                                    output_file.write("\t%s %s, :gl_%s\n\n" % (new_if, if_match.group("register"),
                                                                               random_label_name))
                                    output_file.write("\tgoto/32 :%s\n\n" % if_match.group("goto_label"))
                                    output_file.write("\t:gl_%s" % random_label_name)
                                else:
                                    output_file.write(line)
                            else:
                                output_file.write(line)
                        else:
                            output_file.write(line)
                    else:
                        output_file.write(line)

            # Determines and group blocks of code together
            with inplace_edit_file(arg_filename) as (input_file, output_file):
                edit_method = False
                block_count = 0
                code_blocks: List[CodeBlock] = []
                current_code_block = None
                for line in input_file:
                    if line.startswith(
                            ".method ") and " abstract " not in line and " native " not in line and not edit_method:
                        # in method
                        output_file.write(line)
                        edit_method = True
                        block_count = 0
                        code_blocks = []
                        current_code_block = None
                    elif line.startswith(".end method") and edit_method:
                        # end of method
                        edit_method = False
                        random.shuffle(code_blocks)
                        for code_block in code_blocks:
                            output_file.write(code_block.smali_code)
                        output_file.write(line)
                    elif edit_method:
                        if line.startswith("#!block!#"):
                            block_count += 1
                            current_code_block = CodeBlock(block_count, "")
                            code_blocks.append(current_code_block)
                        else:
                            if block_count > 0 and current_code_block:
                                current_code_block.add_smali_code_to_block(line)
                            else:
                                output_file.write(line)
                    else:
                        output_file.write(line)
        except Exception as e:
            print(e)


class CodeBlock:
    def __init__(self, jump_id=0, smali_code=""):
        self.jump_id = jump_id
        self.smali_code = smali_code

    def add_smali_code_to_block(self, smali_code):
        self.smali_code += smali_code

