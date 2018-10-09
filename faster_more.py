'''
This short script outputs events info by ten (like more)

Usage:
 $ faster_more.py file.fast [file2.fast ...]
'''

import faster
import os, sys

import traceback

if __name__=="__main__":
    try:
        assert(len(sys.argv)>1)
        the_argv = sys.argv[1:]
        maxn=faster.const.max_number_of_events_in_file
        if any(map(lambda x:x.startswith('--maxn='), the_argv)):
            maxn=int([x for x in the_argv if x.startswith('--maxn=')][0].split('=')[-1])
            the_argv=[x for x in the_argv if not x.startswith('--maxn=')]
        n_display = 0
        for file_to_read in the_argv:
            try:
                assert(os.path.exists(file_to_read))
                assert(os.path.isfile(file_to_read))
                print("# In file '{0}'".format(file_to_read))
                # opening file
                ffr = faster.File_reader(file_to_read,maxn)
                for evt in ffr:
                    if evt.type_alias==10:
                        print(evt._repr_head())
                        for subevt in evt.data['events']:
                            print("\t {0}".format(str(subevt)))
                    else:
                        print(evt)
                    n_display+=1
                    if n_display==10:
                        n_display=0
                        k = input("# q: quit, any other: continue\n")
                        if k=='q' or k=='Q':
                            break
                
            except:
                print(sys.exc_info())
                traceback.print_exception(*sys.exc_info())
                print("{0} does not exists".format(file_to_read))
                print( __doc__)
    except:
        print(sys.exc_info()[0])
        print("Please provide file to read")
        print(__doc__)
    
