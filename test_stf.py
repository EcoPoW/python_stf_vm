
import dis
import codeop

import vm
import stf


if __name__ == '__main__':
    c = codeop.compile_command('''
#a=1
#b=2

def chain_stf(state, data):
    subchains = state.get('subchains', {})
    subchains.update(data.get('subchains', {}))
    new_state = {}
    new_state['subchains'] = subchains
    return new_state

''', symbol="exec")
    # print(c)
    # print(c.co_code)
    # print(c.co_consts[0].co_code)
    # print(stf.chain_stf.__code__.co_code)
    # print(hashlib.sha256(stf.chain_stf.__code__.co_code).hexdigest())

    dis.dis(stf.chain_stf)
    print('co_code', [hex(i) for i in stf.chain_stf.__code__.co_code])
    # print(stf.chain_stf.__code__)

    print('co_name', stf.chain_stf.__code__.co_name)
    print('co_varnames', stf.chain_stf.__code__.co_varnames)
    print('co_argcount', stf.chain_stf.__code__.co_argcount)

    print('co_consts', stf.chain_stf.__code__.co_consts)
    print('co_names', stf.chain_stf.__code__.co_names) # for method

    print('co_stacksize', stf.chain_stf.__code__.co_stacksize)
    print('co_posonlyargcount', stf.chain_stf.__code__.co_posonlyargcount)
    print('co_nlocals', stf.chain_stf.__code__.co_nlocals)
    print('co_kwonlyargcount', stf.chain_stf.__code__.co_kwonlyargcount)
    print('co_cellvars', stf.chain_stf.__code__.co_cellvars)
    print('co_freevars', stf.chain_stf.__code__.co_freevars)

    vm = vm.VM()
    vm.import_function(stf.chain_stf)
    vm.run([{}, {'subchains': {1:2}}], 'chain_stf')
