myList = list("123")

def permutation(mylist, level = 1):
    if level == 3:
        return
    for i in range(len(myList)):
        if level == 0:
            print("\n")
        print(myList[i], end = " ")
        permutation(myList, level + 1)

permutation(myList)