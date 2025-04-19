def A():
    print("A")
    return True

def B():
    print("B")
    return False

print(B() and A())