def callFunction():
    return False

def testAllByteCode():
    a = 1
    b = 2
    c = a + b
    a, b = b, a
    a, b, c = b, c, a
    c = a ** b
    c = a * b
    c = a % b
    c = a + b
    c = a - b
    d = a > b
    tp = (a, b, c)
    ls = [1, 2, 3, 4]
    ls_2 = ls[1:2]
    dt = {'a': 1}
    index = 2
    element = ls[index]
    c = a // b
    c = a / b
    a += b
    a -= b
    value = 1
    callf = callFunction()
    e = f"{a}"
    ls[index] = value
    for item in ls:
        e = 0
    try:
        print("Inside try block")
    except:
        print("Inside except block")
    finally:
        print("Inside finally block")
    if True:
        a = 1
    if False:
        a = 2

