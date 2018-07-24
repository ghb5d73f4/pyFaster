import faster


f = faster.File_reader("data/test_0001.fast", 250)

for evt in f:
    if evt.type_alias==10:
        print(evt._repr_head())
        for subevt in evt.data:
            print("\t"+str(subevt))
    

