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
URL = 'https://github.com/fnphat/dict-operations'


def json_str_2_data_dict(json_str):
    # This should be a JSON dictionary, removing the comment lines
    return _json.loads('\n'.join([x for x in json_str.splitlines() if not x.startswith('#')]))

def data_dict_2_json(data_dict):
    return _json.dumps( _collections.OrderedDict(sorted(data_dict.items(), key=lambda t: t[0].lower())), indent=4 )

def get_dicts(in_file):
    dict_a = json_str_2_data_dict(_sys.stdin.read())
    with open(in_file) as f:
        dict_b = json_str_2_data_dict(f.read())
    return (dict_a, dict_b)


def union(dict_a, dict_b):
    return dict(dict_b, **dict_a)

def intersection(dict_a, dict_b):
    return {k:v for k,v in dict_a.items() if k in dict_b.keys()}

def difference(dict_a, dict_b):
    return {k:v for k,v in dict_a.items() if k not in dict_b.keys()}

def symmetric_difference(dict_a, dict_b):
    return union(difference(dict_a, dict_b), difference(dict_b, dict_a))


def union_cmd(args):
    dict_a, dict_b = get_dicts(args.in_file)
    print data_dict_2_json(union(dict_a, dict_b))

def inter_cmd(args):
    dict_a, dict_b = get_dicts(args.in_file)
    print data_dict_2_json(intersection(dict_a, dict_b))

def diff_cmd(args):
    dict_a, dict_b = get_dicts(args.in_file)
    print data_dict_2_json(difference(dict_a, dict_b))
    
def symdiff_cmd(args):
    dict_a, dict_b = get_dicts(args.in_file)
    print data_dict_2_json(symmetric_difference(dict_a, dict_b))
 
def update_cmd(args):
    dict_a, dict_b = get_dicts(args.in_file)
    print data_dict_2_json(union(intersection(dict_b, dict_a), dict_a))

   
def main(arguments=None):
    parser = _argparse.ArgumentParser()
    parser.add_argument('--version', action='version', version="Version " +VERSION+ " - " +URL)
    subparsers = parser.add_subparsers(help='.')

    parser_union = subparsers.add_parser('union', help='Union: stdin | in_file = stdout.')
    parser_union.add_argument('in_file', help=".")
    parser_union.set_defaults(func=union_cmd)

    parser_inter = subparsers.add_parser('inter', help='Intersection: stdin & in_file = stdout.')
    parser_inter.add_argument('in_file', help=".")
    parser_inter.set_defaults(func=inter_cmd)

    parser_diff = subparsers.add_parser('diff', help='Difference: stdin - in_file = stdout.')
    parser_diff.add_argument('in_file', help=".")
    parser_diff.set_defaults(func=diff_cmd)

    parser_symdiff = subparsers.add_parser('symdiff', help='Symmetric difference:stdin ^ in_file = stdout.')
    parser_symdiff.add_argument('in_file', help=".")
    parser_symdiff.set_defaults(func=symdiff_cmd)

    parser_update = subparsers.add_parser('update', help='Update: (in_file & stdin) | (stdin) = stdout.')
    parser_update.add_argument('in_file', help=".")
    parser_update.set_defaults(func=update_cmd)
    
    args = parser.parse_args(arguments)
    args.func(args)

        
if __name__ == "__main__":
    main()