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
Basic operations for dictionaries
"""
def count(dict_a):
    return len(dict_a)

def same_keys(dict_a, dict_b):
    return set(dict_a.keys()) == set(dict_b.keys())

def same(dict_a, dict_b):
    return dict_a == dict_b

def intersection(dict_a, dict_b):
    return dict(set(dict_a.items()) & set(dict_b.items()))

def difference(dict_a, dict_b):
    return dict(set(dict_a.items()) - set(dict_b.items()))

def merge(dict_a, dict_b):
    return dict(dict_b, **dict_a)

def extract(dict_a, dict_b):
    return {k:v for k,v in dict_a.items() if k in dict_b.keys()}

def erase(dict_a, dict_b):
    return {k:v for k,v in dict_a.items() if k not in dict_b.keys()}

"""
Command line commands
"""
def count_cmd(args):
    return count(args.dict)

def samekeys_cmd(args):
    return same_keys(args.dict_a, args.dict_b)

def same_cmd(args):
    return same(args.dict_a, args.dict_b)

def inter_cmd(args):
    return data_dict_2_json(intersection(args.dict_a, args.dict_b))

def diff_cmd(args):
    return data_dict_2_json(difference(args.dict_a, args.dict_b))

def merge_cmd(args):
    return data_dict_2_json(merge(args.dict_a, args.dict_b))

def extract_cmd(args):
    return data_dict_2_json(extract(args.dict_a, args.dict_b))

def erase_cmd(args):
    return data_dict_2_json(erase(args.dict_a, args.dict_b))



def main(arguments=None):
    parser = _argparse.ArgumentParser()
    
    # Basic arguments
    parser.add_argument('--version', action='version', version="Version " +VERSION+ " - " +URL)
    
    # Common arguments
    parent_parser = _argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument('in_file', help="Input file containing the JSON dictionary B.")
    parent_parser.add_argument('-r', '--reverse-order', action='store_true', dest='reverse', help="Reverse the order of the operands: dict A is in_file and dict B is stdin.")
    
    # Commands
    subparsers = parser.add_subparsers(help="Data dictionary operations tool. Dict A is stdin and dict B is in_file, result is on stdout.")
    
    parser_count = subparsers.add_parser('count', help="Count the number of key-value pairs: the result will be a non-negative integer.")
    parser_count.set_defaults(func=count_cmd)
    
    parser_samekeys = subparsers.add_parser('samekeys', parents=[parent_parser], help="Keys equality: 'True' when all keys from A are in B and vice-versa, 'False' otherwise.")
    parser_samekeys.set_defaults(func=samekeys_cmd)
    
    parser_same = subparsers.add_parser('same', parents=[parent_parser], help="key-value pairs equality: 'True' when all key-value pairs from A are in B and vice-versa, 'False' otherwise.")
    parser_same.set_defaults(func=same_cmd)
    
    parser_inter = subparsers.add_parser('inter', parents=[parent_parser], help="Intersection of dictionaries: get the key-value pairs that are common to A and B.")
    parser_inter.set_defaults(func=inter_cmd)
    
    parser_diff = subparsers.add_parser('diff', parents=[parent_parser], help="Difference of dictionaries: remove key-value pairs from A that are in B.")
    parser_diff.set_defaults(func=diff_cmd)
    
    parser_merge = subparsers.add_parser('merge', parents=[parent_parser], help="Merge dictionaries: value in A have priority over value in B with the same key.")
    parser_merge.set_defaults(func=merge_cmd)
    
    parser_extract = subparsers.add_parser('extract', parents=[parent_parser], help="Extract key-value pairs from A for all keys that are in B.")
    parser_extract.set_defaults(func=extract_cmd)
    
    parser_erase = subparsers.add_parser('erase', parents=[parent_parser], help="Erase key-value pairs from A for all keys that are in B.")
    parser_erase.set_defaults(func=erase_cmd)
    
    
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