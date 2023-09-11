a = open("l&T_GST_LIST.txt", "r+")
data = a.readlines()
for i in data:
    print(i.split(',')[0])
