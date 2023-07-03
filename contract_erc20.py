
import hashlib
import time

import tornado.escape
import web3

import database

class address(str):pass
class uint256(int):pass

# function name() public view returns (string)
# function symbol() public view returns (string)
# function decimals() public view returns (uint8)
# function totalSupply() public view returns (uint256)
# function balanceOf(address _owner) public view returns (uint256 balance)
# function transfer(address _to, uint256 _value) public returns (bool success)
# function transferFrom(address _from, address _to, uint256 _value) public returns (bool success)
# function approve(address _spender, uint256 _value) public returns (bool success)
# function allowance(address _owner, address _spender) public view returns (uint256 remaining)

# event Transfer(address indexed _from, address indexed _to, uint256 _value)
# event Approval(address indexed _owner, address indexed _spender, uint256 _value)

CONTRACT_ADDRESS = b'0x0000000000000000000000000000000000000001'

_sender = None

# def init(_name, _symbol, _decimals):
#     global name
#     global symbol
#     global decimals

#     if not (name, symbol, decimals):
#         name = _name
#         symbol = _symbol
#         decimals = _decimals
#     pass


def mint(_to:address, _amount:uint256):
    amount = web3.main.to_int(hexstr=_amount)
    try:
        current_amount_json = _mpt.get(b'%s_balance_%s' % (CONTRACT_ADDRESS, _to.encode('utf8')))
        current_amount = tornado.escape.json_decode(current_amount_json)
    except:
        current_amount = 0

    new_amount = current_amount + amount
    print('before mint', current_amount)
    print('mint to', _to, amount)
    print('after mint', new_amount)
    new_amount_json = tornado.escape.json_encode(new_amount)
    _mpt.update(b'%s_balance_%s' % (CONTRACT_ADDRESS, _to.encode('utf8')), new_amount_json.encode('utf8'))

    current_total_json = _mpt.get(b'%s_total' % CONTRACT_ADDRESS)
    current_total = tornado.escape.json_decode(current_total_json)
    new_total = current_total + amount
    print('after mint total', new_total)
    new_total_json = tornado.escape.json_encode(new_total)
    _mpt.update(b'%s_total' % CONTRACT_ADDRESS, new_total_json.encode('utf8'))


def approve(_spender:address, _value:uint256):
    pass


def allowance(_owner:address, _spender:address):
    pass


def transfer(_to:address, _value:uint256):
    # to_bytes = web3.main.to_bytes(hexstr=_to)
    # to_addr = web3.main.to_checksum_address(to_bytes[-20:])
    amount = web3.main.to_int(hexstr=_value)
    print('transfer to', _to, amount)

    try:
        sender_amount_json = _mpt.get(b'%s_balance_%s' % (CONTRACT_ADDRESS, _sender.encode('utf8')))
        sender_amount = tornado.escape.json_decode(sender_amount_json)
    except:
        sender_amount = 0

    sender_new_amount = sender_amount - amount
    assert sender_new_amount >= 0
    print('after transfer sender', sender_new_amount)
    sender_new_amount_json = tornado.escape.json_encode(sender_new_amount)
    _mpt.update(b'%s_balance_%s' % (CONTRACT_ADDRESS, _sender.encode('utf8')), sender_new_amount_json.encode('utf8'))

    try:
        current_amount_json = _mpt.get(b'%s_balance_%s' % (CONTRACT_ADDRESS, _to.encode('utf8')))
        current_amount = tornado.escape.json_decode(current_amount_json)
    except:
        current_amount = 0

    new_amount = current_amount + amount
    print('after transfer receiver', new_amount)
    new_amount_json = tornado.escape.json_encode(new_amount)
    _mpt.update(b'%s_balance_%s' % (CONTRACT_ADDRESS, _to.encode('utf8')), new_amount_json.encode('utf8'))


def transferFrom(_from:address, _to:address, _value:uint256):
    print('transferFrom')


def balanceOf(_owner:address):
    try:
        amount_json = _mpt.get(b'%s_balance_%s' % (CONTRACT_ADDRESS, _owner.encode('utf8')))
        amount = tornado.escape.json_decode(amount_json)
    except:
        amount = 0
    print('balanceOf', _owner, amount)

    return f'0x{amount:0>64x}'
    # return '0x0000000000000000000000000000000000000000000000000000000000001000'


def name():
    return None

def symbol():
    sym = hex(ord('U'))[2:]
    print('sym', sym)
    return '0x00000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000000001%s00000000000000000000000000000000000000' % sym
    # return '0x00000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000000003504f570000000000000000000000000000000000' #POW

def decimals():
    return f'0x{18:0>64x}'

def totalSupply():
    return 0



# db = database.get_conn()
# blockhash = db.get(b'chain_%s' % CONTRACT_ADDRESS)
# print(blockhash)
# if not blockhash:
#     contract_state = {'balance': _balance}
#     new_msg = ['0'*64, '', '', contract_state]
#     new_contract_hash = hashlib.sha256(tornado.escape.json_encode(new_msg).encode('utf8')).hexdigest()
#     new_contract_hash_bytes = new_contract_hash.encode('utf8')

#     db.put(b'msgstate_%s' % new_contract_hash_bytes, tornado.escape.json_encode(contract_state).encode('utf8'))
#     db.put(b'msg_%s' % new_contract_hash_bytes, tornado.escape.json_encode([new_contract_hash] + new_msg).encode('utf8'))
#     db.put(b'chain_%s' % CONTRACT_ADDRESS, new_contract_hash_bytes)

_mpt = database.get_mpt()
_mpt.update(b'%s_balance_0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266' % CONTRACT_ADDRESS, tornado.escape.json_encode(10**20))
_mpt.update(b'%s_total' % CONTRACT_ADDRESS, tornado.escape.json_encode(10**20))
print('root', _mpt.root())
print('root hash', _mpt.root_hash())

# hardhat test Account #0: 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266
# Private Key: 0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80


if __name__ == '__main__':
    for i in range(2):
        mint('0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266', '0x1000')
    _sender = '0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266'
    transfer('0x0000000000000000000000000000000000000002', '0x1000')
    balanceOf('0x0000000000000000000000000000000000000002')

    # t0 = time.time()
    # for i in range(10000):
    #     balanceOf('0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266')
    # print(time.time() - t0)
