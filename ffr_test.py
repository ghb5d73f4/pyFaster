import faster


f = faster.File_reader("data/test_0001.fast", 120)

for evt in f:
    if evt.type=='group':
        print(evt)

