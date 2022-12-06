from mock import msg

total = 0
users = {}
owner = ''
_hidden = 1

def init():
    global owner
    owner = msg.sender

def mint(amount):
    assert type(amount) is int and amount > 0
    assert owner == msg.sender
    global total, users
    total += amount
    users.setdefault(msg.sender, 0)
    users[msg.sender] += amount

def transfer(user, amount):
    assert type(amount) is int and amount > 0
    global total, users
    assert users[msg.sender] >= amount
    users[msg.sender] -= amount
    users.setdefault(user, 0)
    users[user] += amount

if __name__ == '__main__':
    init()
    mint(1000)
    transfer('0x1111', 1000)


# bad example

__hidden = 2

class Empty:
    pass
