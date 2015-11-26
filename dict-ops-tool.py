#!/usr/bin/env python
"""
The MIT License (MIT)

Copyright (c) 2015 Frederic N. Therrien

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import json as _json
import sys as _sys
import collections as _collections
import argparse as _argparse


VERSION = '0.1'
URL = 'https://github.com/fnphat/dict-ops-tool'


def json_str_2_data_dict(json_str):
    """
    Convert a JSON string to a dictionary.
    """
    # This should be a JSON dictionary, removing the comment lines
    return _json.loads('\n'.join([x for x in json_str.splitlines() if not x.startswith('#')]))

def data_dict_2_json(data_dict):
    """
    Convert a dictionary to a JSON string.
    """
    return _json.dumps( _collections.OrderedDict(sorted(data_dict.items(), key=lambda t: t[0].lower())), indent=4 )

"""
Basic set operations for dictionaries
"""
def union(dict_a, dict_b):
    return dict(dict_b, **dict_a)

def intersection(dict_a, dict_b):
    return {k:v for k,v in dict_a.items() if k in dict_b.keys()}

def difference(dict_a, dict_b):
    return {k:v for k,v in dict_a.items() if k not in dict_b.keys()}

def symmetric_difference(dict_a, dict_b):
    return union(difference(dict_a, dict_b), difference(dict_b, dict_a))

"""
Command line commands
"""
def count_cmd(args):
    return len(args.dict)

def equal_cmd(args):
    return args.dict_a == args.dict_b
    
def kequal_cmd(args):
    return args.dict_a.keys() == args.dict_b.keys()

def union_cmd(args):
    return data_dict_2_json(union(args.dict_a, args.dict_b))

def inter_cmd(args):
    return data_dict_2_json(intersection(args.dict_a, args.dict_b))

def diff_cmd(args):
    return data_dict_2_json(difference(args.dict_a, args.dict_b))
    
def symdiff_cmd(args):
    return data_dict_2_json(symmetric_difference(args.dict_a, args.dict_b))
 
def update_cmd(args):
    return data_dict_2_json(union(intersection(args.dict_b, args.dict_a), args.dict_a))

   
def main(arguments=None):
    parser = _argparse.ArgumentParser()
    
    # Basic arguments
    parser.add_argument('--version', action='version', version="Version " +VERSION+ " - " +URL)
    
    # Common arguments
    parent_parser = _argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument('in_file', help="Input file containing the JSON dictionary B.")
    parent_parser.add_argument('-r', '--reverse-order', action='store_true', dest='reverse', help="Reverse the order of the operands: dict A is in_file and dict B is stdin.")

    # Commands
    subparsers = parser.add_subparsers(help="Data dictionary operations tool. Dict A is stdin and dict B is in_file. Dict A's values have priority over dict B's values.")

    parser_count = subparsers.add_parser('count', help="Count the number of key-value pairs: len(A) = len(stdin) = <positive integer>.")
    parser_count.set_defaults(func=count_cmd)

    parser_equal = subparsers.add_parser('==', parents=[parent_parser], help="Equality: [A == B] = [stdin == in_file] = True|False.")
    parser_equal.set_defaults(func=equal_cmd)

    parser_kequal = subparsers.add_parser('k==', parents=[parent_parser], help="Equality of keys: [keys(A) == keys(B)] = [keys(stdin) == keys(in_file)] = True|False.")
    parser_kequal.set_defaults(func=kequal_cmd)
    
    parser_union = subparsers.add_parser('union', parents=[parent_parser], help="Union: A | B = stdin | in_file = stdout.")
    parser_union.set_defaults(func=union_cmd)

    parser_inter = subparsers.add_parser('inter', parents=[parent_parser], help="Intersection: A & B = stdin & in_file = stdout.")
    parser_inter.set_defaults(func=inter_cmd)

    parser_diff = subparsers.add_parser('diff', parents=[parent_parser], help="Difference: A - B = stdin - in_file = stdout.")
    parser_diff.set_defaults(func=diff_cmd)

    parser_symdiff = subparsers.add_parser('symdiff', parents=[parent_parser], help="Symmetric difference: A ^ B = stdin ^ in_file = stdout.")
    parser_symdiff.set_defaults(func=symdiff_cmd)

    parser_update = subparsers.add_parser('update', parents=[parent_parser], help="Update: (B & A) | A = (in_file & stdin) | stdin = stdout.")
    parser_update.set_defaults(func=update_cmd)
    
    args = parser.parse_args(arguments)

    # Get dict A and B
    if _sys.stdin.isatty():
        print "You need to provide a JSON dictionary on STDIN."
        exit(1)
    else:
        stdin_dict = json_str_2_data_dict(_sys.stdin.read())
        if 'in_file' in args:
            with open(args.in_file) as f:
                in_file_dict = json_str_2_data_dict(f.read())
            if args.reverse:
                args.dict_a, args.dict_b = (in_file_dict, stdin_dict)
            else:
                args.dict_a, args.dict_b = (stdin_dict, in_file_dict)
        else:
            args.dict = stdin_dict
        return args.func(args)

       
if __name__ == "__main__":
    print main()