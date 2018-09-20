'''
This short script outputs statistics on faster files.

Usage:
 $ faster_stats.py file.fast [file2.fast ...]
'''

import faster
import os, sys

if __name__=="__main__":
    try:
        assert(len(sys.argv)>1)
        the_argv = sys.argv[1:]
        maxn=faster.const.max_number_of_events_in_file
        if any(map(lambda x:x.startswith('--maxn='), the_argv)):
            maxn=int([x for x in the_argv if x.startswith('--maxn=')][0].split('=')[-1])
            the_argv=[x for x in the_argv if not x.startswith('--maxn=')]
        print("[")
        for file_to_read in the_argv:
            try:
                assert(os.path.exists(file_to_read))
                assert(os.path.isfile(file_to_read))
                #
                # Preping the variables
                number_of_events = 0
                types = {}
                labels = {}
                types_in_groups = {}
                labels_in_groups = {}
                #
                # opening file
                ffr = faster.File_reader(file_to_read,maxn)
                for evt in ffr:
                    number_of_events+=1
                    types[evt.type]=types.get(evt.type,0)+1
                    labels[evt.label]=labels.get(evt.label,0)+1
                    if evt.type=='group':
                        for subevt in evt.data:
                            types_in_groups[subevt.type]=types_in_groups.get(subevt.type,0)+1
                            labels_in_groups[subevt.label]=labels_in_groups.get(subevt.label,0)+1
                        #end for subevt
                #end for event
                print("   {")
                print("    'number_of_events_to_read':'{0}',".format(maxn))
                print("    'file_name':'{0}',".format(file_to_read))
                print("    'number_of_events': {0},".format(number_of_events))
                print("    'types': {")
                for t in types:
                    print("        '{0}': {1},".format(t, types[t]))
                print('      },')
                print("    'labels': {")
                for t in labels:
                    print("        '{0}': {1},".format(t, labels[t]))
                print('      },')
                print("    'in_groups': {")
                print("         'types': {")
                for t in types_in_groups:
                    print("           '{0}': {1},".format(t, types_in_groups[t]))
                print('       },')
                print("         'labels': {")
                for t in labels_in_groups:
                    print("           '{0}': {1},".format(t, labels_in_groups[t]))
                print('       },')
                
            except:
                print(sys.exc_info())
                print("{0} does not exists".format(file_to_read))
                print( __doc__)
        print("]")
    except:
        print(sys.exc_info()[0])
        print("Please provide file to read")
        print(__doc__)
    
