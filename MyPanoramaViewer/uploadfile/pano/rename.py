import os

l1=os.listdir()

for i in l1:
    if os.path.isdir(i):
        l2=os.listdir(i)
        for j in l2:
            if j.endswith(".jpg") and j!="preview.jpg":
                newName="pano_"+j[-5:]
                print(newName)
                os.rename(i+"/"+j, i+"/"+newName)