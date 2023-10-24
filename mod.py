
total = 0
users = {}
owner = ''
_hidden = 1

def init():
    global owner
    owner = _sender

def mint(amount):
    assert type(amount) is int and amount > 0
    assert owner == _sender
    global total, users
    total += amount
    users.setdefault(_sender, 0)
    users[_sender] += amount

def transfer(user, amount):
    assert type(amount) is int and amount > 0
    global total, users
    assert users[_sender] >= amount
    users[_sender] -= amount
    users.setdefault(user, 0)
    users[user] += amount

if __name__ == '__main__':
    init()
    mint(1000)
    transfer('0x1111', 1000)


# bad example

__hidden = 2

# class Empty:
#     pass
