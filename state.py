
import tornado.escape

import database


CONTRACT_ADDRESS = '0x0000000000000000000000000000000000000001'

contract_address = CONTRACT_ADDRESS


_trie = database.get_conn()
block_number = 0

def put(key, value, addr):
    global _trie
    global block_number
    value_json = tornado.escape.json_encode(value)
    print('%s_%s_%s' % (contract_address, key, str(10**15 - block_number).zfill(16)), value_json)
    _trie.put(('%s_%s_%s' % (contract_address, key, str(10**15 - block_number).zfill(16))).encode('utf8'), value_json.encode('utf8'))


def get(key, default, addr):
    global _trie
    # print('_trie', _trie)
    value = default
    # block_number = 0
    try:
        it = _trie.iteritems()
        it.seek(('%s_%s' % (contract_address, key)).encode('utf8'))

        # value_json = _trie.get(b'%s_%s' % (contract_address, key.encode('utf8')))
        for k, value_json in it:
            if k.startswith(('%s_%s' % (contract_address, key)).encode('utf8')):
                # block_number = 10**15 - int(k.replace(b'%s_%s_' % (contract_address, key.encode('utf8')), b''))
                value = tornado.escape.json_decode(value_json)
            break

    except:
        pass

    return value

