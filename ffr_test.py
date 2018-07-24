import faster


f = faster.File_reader("data/test_0001.fast", 150)

for evt in f:
    if evt.type_alias!=70:
        print(evt)
    else:
        print(evt._repr_head())

