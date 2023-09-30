
import dis
import types
import time

import eth_utils

import state
import contract_erc20 as mod
import vm


# interface_map = {
#     '0x'+eth_utils.keccak(b'transfer(address,uint256)').hex()[:8]: transfer,
#     '0x'+eth_utils.keccak(b'balanceOf(address)').hex()[:8]: balanceOf,
#     '0x'+eth_utils.keccak(b'decimals()').hex()[:8]: decimals,
#     '0x'+eth_utils.keccak(b'allowance(address,address)').hex()[:8]: allowance,
#     '0x'+eth_utils.keccak(b'symbol()').hex()[:8]: symbol,
#     '0x'+eth_utils.keccak(b'totalSupply()').hex()[:8]: totalSupply,
#     '0x'+eth_utils.keccak(b'name()').hex()[:8]: name,
#     '0x'+eth_utils.keccak(b'approve(address,uint256)').hex()[:8]: approve,
#     '0x'+eth_utils.keccak(b'transferFrom(address,address,uint256)').hex()[:8]: transferFrom,
#     '0x'+eth_utils.keccak(b'mint(address,uint256)').hex()[:8]: mint,
# }

# transfer(address,uint256)： 0xa9059cbb
# balanceOf(address)：0x70a08231
# decimals()：0x313ce567
# allowance(address,address)： 0xdd62ed3e
# symbol()：0x95d89b41
# totalSupply()：0x18160ddd
# name()：0x06fdde03
# approve(address,uint256)：0x095ea7b3
# transferFrom(address,address,uint256)： 0x23b872dd


if __name__ == '__main__':
    dis.dis(mod)
    print(dir(mod))
    # print(mod.__loader__)
    # print(mod.__builtins__)
    # print(mod.__package__)

    # for k, v in mod.__dict__.items():
    #     if not k.startswith('_') and type(v) not in [type, types.FunctionType]:
    #         print(k, type(v))

    for k, v in mod.__dict__.items():
        if not k.startswith('_') and type(v) in [types.FunctionType]:
            # print(k, type(v))
            # print(v.__code__.co_kwonlyargcount, v.__code__.co_posonlyargcount)
            # print(v.__code__.co_varnames[:v.__code__.co_argcount])
            # for i in v.__code__.co_varnames[:v.__code__.co_argcount]:
            #     print(v.__annotations__[i].__name__)
            params = [v.__annotations__[i].__name__ for i in v.__code__.co_varnames[:v.__code__.co_argcount]]
            func_sig = '%s(%s)' % (k, ','.join(params))
            print(func_sig, '0x'+eth_utils.keccak(func_sig.encode('utf8')).hex()[:8])


    vm = vm.VM()
    state.block_number = 1
    vm.import_module(mod)
    # state._sender = '0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266'
    vm.global_vars['_sender'] = '0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266'
    vm.global_vars['_self'] = '0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266'
    vm.global_vars['_get'] = state.get
    vm.global_vars['_put'] = state.put
    vm.global_vars['print'] = print
    # vm.run([], 'init')
    # vm.run(['0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266', 1000], 'mint')
    # vm.run(['0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266', 1000], 'transfer')
    t0 = time.time()
    for i in range(1):
        print('run init')
        vm.run(['ERC20', 'U', 18, '0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266'], 'init')
        print('run mint')
        vm.run(['0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266', 1000], 'mint')
        print('run transfer')
        vm.run(['0x0000000000000000000000000000000000000002', 1000], 'transfer')
        #print('run balanceOf')
        #vm.run(['0x0000000000000000000000000000000000000002'], 'balanceOf')
    print(time.time() - t0)
