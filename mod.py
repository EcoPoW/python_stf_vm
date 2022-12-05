from mock import msg

total = 0
users = {}
owner = ''

def init():
    global owner
    owner = msg.sender

def mint(amount):
    global total, users
    total += amount

if __name__ == '__main__':
    init()

# bad example

_hidden = 1
__hidden = 2

class Empty:
    pass
