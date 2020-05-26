import os


big_list = []


def dive(directory):
    global big_list
    contents = os.listdir(directory)
    picture_holder = []
    for items in contents:
        #print(items)
        try:
            dive(items)
        except:
            if ".py" in items:
                picture_holder.append(items)
    print(picture_holder)
    big_list.append(picture_holder)
    
print(big_list)

