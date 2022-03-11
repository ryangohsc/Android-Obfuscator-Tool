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
        self.valid_block_opcodes = ["move", "move/from16", "move/16", "move-wide", "move-wide/from16", "move-wide/16",
                                    "move-object", "move-object/from16", "move-object/16", "return-void", "return",
                                    "return-wide", "return-object", "const/4", "const/16", "const", "const/high16",
                                    "const-wide/16", "const-wide/32", "const-wide", "const-wide/high16", "const-string",
                                    "const-string/jumbo", "const-class", "monitor-enter", "monitor-exit", "check-cast",
                                    "instance-of", "array-length", "new-instance", "new-array", "filled-new-array",
                                    "filled-new-array/range", "throw", "goto", "goto/16", "goto/32", "cmpl-float",
                                    "cmpg-float", "cmpl-double", "cmpg-double", "cmp-long", "if-eq", "if-ne", "if-lt",
                                    "if-ge", "if-gt", "if-le", "if-eqz", "if-nez", "if-ltz", "if-gez", "if-gtz",
                                    "if-lez", "aget", "aget-wide", "aget-object", "aget-boolean", "aget-byte",
                                    "aget-char", "aget-short", "aput", "aput-wide", "aput-object", "aput-boolean",
                                    "aput-byte", "aput-char", "aput-short", "iget", "iget-wide", "iget-object",
                                    "iget-boolean", "iget-byte", "iget-char", "iget-short", "iput", "iput-wide",
                                    "iput-object", "iput-boolean", "iput-byte", "iput-char", "iput-short", "sget",
                                    "sget-wide", "sget-object", "sget-boolean", "sget-byte", "sget-char", "sget-short",
                                    "sput", "sput-wide", "sput-object", "sput-boolean", "sput-byte", "sput-char",
                                    "sput-short", "invoke-virtual", "invoke-super", "invoke-direct", "invoke-static",
                                    "invoke-interface", "invoke-virtual/range", "invoke-super/range",
                                    "invoke-direct/range", "invoke-static/range", "invoke-interface/range", "neg-int",
                                    "not-int", "neg-long", "not-long", "neg-float", "neg-double", "int-to-long",
                                    "int-to-float", "int-to-double", "long-to-int", "long-to-float", "long-to-double",
                                    "float-to-int", "float-to-long", "float-to-double", "double-to-int",
                                    "double-to-long", "double-to-float", "int-to-byte", "int-to-char", "int-to-short",
                                    "add-int", "sub-int", "mul-int", "div-int", "rem-int", "and-int", "or-int",
                                    "xor-int", "shl-int", "shr-int", "ushr-int", "add-long", "sub-long", "mul-long",
                                    "div-long", "rem-long", "and-long", "or-long", "xor-long", "shl-long", "shr-long",
                                    "ushr-long", "add-float", "sub-float", "mul-float", "div-float", "rem-float",
                                    "add-double", "sub-double", "mul-double", "div-double", "rem-double",
                                    "add-int/2addr", "sub-int/2addr", "mul-int/2addr", "div-int/2addr", "rem-int/2addr",
                                    "and-int/2addr", "or-int/2addr", "xor-int/2addr", "shl-int/2addr", "shr-int/2addr",
                                    "ushr-int/2addr", "add-long/2addr", "sub-long/2addr", "mul-long/2addr",
                                    "div-long/2addr", "rem-long/2addr", "and-long/2addr", "or-long/2addr",
                                    "xor-long/2addr", "shl-long/2addr", "shr-long/2addr", "ushr-long/2addr",
                                    "add-float/2addr", "sub-float/2addr", "mul-float/2addr", "div-float/2addr",
                                    "rem-float/2addr", "add-double/2addr", "sub-double/2addr", "mul-double/2addr",
                                    "div-double/2addr", "rem-double/2addr", "add-int/lit16", "rsub-int",
                                    "mul-int/lit16", "div-int/lit16", "rem-int/lit16", "and-int/lit16", "or-int/lit16",
                                    "xor-int/lit16", "add-int/lit8", "rsub-int/lit8", "mul-int/lit8", "div-int/lit8",
                                    "rem-int/lit8", "and-int/lit8", "or-int/lit8", "xor-int/lit8", "shl-int/lit8",
                                    "shr-int/lit8", "ushr-int/lit8"]

    def random_string(self):
        """
        Returns a cryptographically secure random string
        :return:
        """
        return ''.join(random.SystemRandom().choice(string.ascii_letters) for _ in range(16))

    def run(self, arg_filename):
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
                    if line.startswith(".method ") and " abstract " not in line and " native " not in line and not edit_method:
                        output_file.write(line)
                        edit_method = True
                        inside_try_catch = False
                        jump_count = 0

                    elif line.startswith(".end method") and edit_method:
                        output_file.write(line)
                        edit_method = False
                        inside_try_catch = False

                    elif edit_method:
                        # Inside method. Check if this line contains an op code at
                        # the beginning of the string.
                        match = op_code_pattern.match(line)
                        if match:
                            op_code = match.group("op_code")

                            # Check if we are entering or leaving a try-catch
                            # block of code.
                            if op_code.startswith(":try_start_"):
                                output_file.write(line)
                                inside_try_catch = True
                            elif op_code.startswith(":try_end_"):
                                output_file.write(line)
                                inside_try_catch = False

                            # If this is a valid op code, and we are not inside a
                            # try-catch block, mark this section with a special
                            # label that will be used later and invert the if
                            # conditions (if any).
                            elif op_code in self.valid_block_opcodes and not inside_try_catch:
                                jump_name = self.random_string()
                                output_file.write("\tgoto/32 :l_%s_%s\n\n" % (jump_name, jump_count))
                                output_file.write("\tnop\n\n")
                                output_file.write("#!code_block!#\n")
                                output_file.write("\t:l_%s_%s\n" % (jump_name, jump_count))
                                jump_count += 1

                                new_if = self.control_flow_map.get(op_code, None)
                                if new_if:
                                    if_match = if_pattern.match(line)
                                    random_label_name = self.random_string()
                                    output_file.write("\t%s %s, :gl_%s\n\n" % (new_if, if_match.group("register"), random_label_name))
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

            with inplace_edit_file(arg_filename) as (input_file, output_file):
                edit_method = False
                block_count = 0
                code_blocks: List[CodeBlock] = []
                current_code_block = None
                for line in input_file:
                    if line.startswith(".method ") and " abstract " not in line and " native " not in line and not edit_method:
                        # If at the beginning of a non abstract/native method
                        output_file.write(line)
                        edit_method = True
                        block_count = 0
                        code_blocks = []
                        current_code_block = None

                    elif line.startswith(".end method") and edit_method:
                        edit_method = False
                        random.shuffle(code_blocks)
                        for code_block in code_blocks:
                            output_file.write(code_block.smali_code)
                        output_file.write(line)

                    elif edit_method:
                        # Inside method. Check if this line is marked with a special label.
                        if line.startswith("#!code_block!#"):
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

