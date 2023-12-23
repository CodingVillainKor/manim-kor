def A():
    print("A")
    return True

def B():
    print("B")
    return False

print(A() or 9/0)
print(B() and 9/0)