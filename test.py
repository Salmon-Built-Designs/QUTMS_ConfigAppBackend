oof = [1,2,3,4]
print(oof)
for i in oof:
    del oof[0]
    oof.append('a')
    print(oof)