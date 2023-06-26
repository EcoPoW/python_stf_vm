
import hashlib

import tornado.escape
import web3
import eth_utils

import database

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

_mpt = database.get_mpt()
_mpt.update(b'%s_balance_0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266' % CONTRACT_ADDRESS, tornado.escape.json_encode(10**20))
print('root', _mpt.root())
print('root hash', _mpt.root_hash())

# hardhat test Account #0: 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266
# Private Key: 0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80


# def init(_name, _symbol, _decimals):
#     global name
#     global symbol
#     global decimals

#     if not (name, symbol, decimals):
#         name = _name
#         symbol = _symbol
#         decimals = _decimals
#     pass


def mint(_to, _amount):
    to_bytes = web3.main.to_bytes(hexstr=_to)
    to_addr = web3.main.to_checksum_address(to_bytes[-20:])
    amount = web3.main.to_int(hexstr=_amount)
    print('mint', to_addr, amount)

    prev_contract_hash = db.get(b'chain_%s' % CONTRACT_ADDRESS)
    print('mint', prev_contract_hash)
    msgstate_bytes = db.get(b'msgstate_%s' % prev_contract_hash)
    msgstate = tornado.escape.json_decode(msgstate_bytes)
    print('mint', msgstate)
    msg = db.get(b'msg_%s' % prev_contract_hash)
    print('mint', msg)

    new_msg = [prev_contract_hash.decode('utf8'), '', to_addr, amount]
    print('mint', to_addr, amount)
    new_contract_state = msgstate
    new_contract_state['balance'].setdefault(to_addr, 0)
    new_contract_state['balance'][to_addr] += amount
    new_contract_hash = hashlib.sha256(tornado.escape.json_encode(new_msg).encode('utf8')).hexdigest()
    new_contract_hash_bytes = new_contract_hash.encode('utf8')
    db.put(b'msgstate_%s' % new_contract_hash_bytes, tornado.escape.json_encode(new_contract_state).encode('utf8'))
    db.put(b'msg_%s' % new_contract_hash_bytes, tornado.escape.json_encode([new_contract_hash] + new_msg).encode('utf8'))
    db.put(b'chain_%s' % CONTRACT_ADDRESS, new_contract_hash_bytes)


def approve():
    pass


def allowance():
    pass


def transfer(_to, _amount):
    to_bytes = web3.main.to_bytes(hexstr=_to)
    to_addr = web3.main.to_checksum_address(to_bytes[-20:])
    amount = web3.main.to_int(hexstr=_amount)

    prev_contract_hash = db.get(b'chain_%s' % CONTRACT_ADDRESS)
    print('transfer', prev_contract_hash)
    msgstate_bytes = db.get(b'msgstate_%s' % prev_contract_hash)
    msgstate = tornado.escape.json_decode(msgstate_bytes)
    print('transfer', msgstate)
    msg = db.get(b'msg_%s' % prev_contract_hash)
    print('transfer', msg)

    new_msg = [prev_contract_hash.decode('utf8'), '', to_addr, amount]
    print('transfer', _sender, to_addr, amount)
    new_contract_state = msgstate
    new_contract_state['balance'].setdefault(_sender, 0)
    new_contract_state['balance'][_sender] -= amount
    new_contract_state['balance'].setdefault(to_addr, 0)
    new_contract_state['balance'][to_addr] += (amount - 10**16)
    new_contract_hash = hashlib.sha256(tornado.escape.json_encode(new_msg).encode('utf8')).hexdigest()
    new_contract_hash_bytes = new_contract_hash.encode('utf8')
    db.put(b'msgstate_%s' % new_contract_hash_bytes, tornado.escape.json_encode(new_contract_state).encode('utf8'))
    db.put(b'msg_%s' % new_contract_hash_bytes, tornado.escape.json_encode([new_contract_hash] + new_msg).encode('utf8'))
    db.put(b'chain_%s' % CONTRACT_ADDRESS, new_contract_hash_bytes)


def transferFrom():
    print('transferFrom')


def balanceOf(user):
    user_bytes = web3.main.to_bytes(hexstr=user)
    user_addr = web3.main.to_checksum_address(user_bytes[-20:])
    amount_json = _mpt.get(b'%s_balance_%s' % (CONTRACT_ADDRESS, user_addr.encode('utf8')))
    amount = tornado.escape.json_decode(amount_json)
    # print('balanceOf', amount)

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


interface_map = {
    '0x'+eth_utils.keccak(b'transfer(address,uint256)').hex()[:8]: transfer,
    '0x'+eth_utils.keccak(b'balanceOf(address)').hex()[:8]: balanceOf,
    '0x'+eth_utils.keccak(b'decimals()').hex()[:8]: decimals,
    '0x'+eth_utils.keccak(b'allowance(address,address)').hex()[:8]: allowance,
    '0x'+eth_utils.keccak(b'symbol()').hex()[:8]: symbol,
    '0x'+eth_utils.keccak(b'totalSupply()').hex()[:8]: totalSupply,
    '0x'+eth_utils.keccak(b'name()').hex()[:8]: name,
    '0x'+eth_utils.keccak(b'approve(address,uint256)').hex()[:8]: approve,
    '0x'+eth_utils.keccak(b'transferFrom(address,address,uint256)').hex()[:8]: transferFrom,
    '0x'+eth_utils.keccak(b'mint(address,uint256)').hex()[:8]: mint,
}

# transfer(address,uint256)： 0xa9059cbb
# balanceOf(address)：0x70a08231
# decimals()：0x313ce567
# allowance(address,address)： 0xdd62ed3e
# symbol()：0x95d89b41
# totalSupply()：0x18160ddd
# name()：0x06fdde03
# approve(address,uint256)：0x095ea7b3
# transferFrom(address,address,uint256)： 0x23b872dd


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

if __name__ == '__main__':
    balanceOf('0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266')
