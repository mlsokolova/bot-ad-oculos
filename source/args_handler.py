# -*- coding: utf-8 -*-
import re

def parameters_handler(args_string, valid_args_list):
    
    valid_args_count = len(valid_args_list)
    re_pattern = "|".join(valid_args_list)
    args_list = re.findall(re_pattern, args_string)
    args_list_count = len(args_list)
    if (args_list_count != valid_args_count):
        return 1, "Args is not valid. Please run {c} with the following arguments: " + " and ".join(valid_args_list) + "."
    else:
        args_values = re.split(re_pattern, args_string)
        args_values = map(lambda x: x.strip().strip('"').strip("'").strip(), args_values)
        return 0, dict(zip(args_list,args_values[1:]))
