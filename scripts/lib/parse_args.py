#!/usr/env python
# -*- coding: utf-8 -*-
# -*- format: python -*-
# -*- author: G. Henning -*-
# -*- created: Mon Feb 19 14:32:07 CET 2018 -*-
# -*- copyright: GH/IPHC 2018 -*-
# -*- file:  parse_args.py -*-
# -*- purpose: -*-
 
'''
Parsing command line arguments.
  - `-flag` is added to flags list
  - `--statement` iexecute a statement (usually name=value)
  - `+filename` executes the filename
  - others are appended to `free_params`.

To test, run this file as __main__ and it will print all parsed arguments
'''

import sys
import os.path
import importlib

def parse_args():
    args = sys.argv[1:]
    free_params = []
    to_exec = []
    files_to_exec = []
    flags = []
    modules_to_load = []
    for a in args:
        if a.startswith('--'):
            to_exec.append(a[2:])
        elif a.startswith('-'):
            flags.append(a[1:])
        elif a.startswith('++'):
            modules_to_load.append(a[2:])
        elif a.startswith('+'):
            files_to_exec.append(a[1:])
        else:
            free_params.append(a)
        #end if
    #end for
    #
    for m in modules_to_load:
        importlib.import_module(m)
    for fex in files_to_exec:
        if os.path.exists(fex) and os.path.isfile(fex):
            try:
                print("# executing {0}".format(fex))
                exec(open(fex,'r').read())
            except:
                print("# [Warning] Failed to execute file '{0}'".format(fex))
                print(sys.exc_info())
                pass
            pass #end try
        #end if
    #end for
    for statmt in to_exec:
        try:
            print("# executing {0}".format(statmt))    
            exec(statmt)
        except:
            print("# [Warning] Failed to execute command '{0}'".format(statmt))
            #print(sys.exc_info()[0])
            pass
        pass #end try
    #end for
    # cleanning the local for export
    if 'a' in locals():
        del a
    if 'm' in locals():
        del m
    if 'modules_to_load' in locals():
        del modules_to_load
    if 'to_exec' in locals():
        del to_exec
    if 'statmt' in locals():
        del statmt
    if 'files_to_exec' in locals():
        del files_to_exec
    if 'fex' in locals():
        del fex
    if 'args' in locals():
        del args
    return locals()
    


if __name__=='__main__':
    print(parse_args())
    


