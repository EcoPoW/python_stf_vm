
import dis
import types
import codeop

import vm

if __name__ == '__main__':
    vm = vm.VM()
    debug = False
    if debug:
        import mod
        # print(mod.__loader__)
        # print(mod.__builtins__)
        # print(mod.__package__)

        # for k, v in mod.__dict__.items():
        #     if not k.startswith('_') and type(v) not in [type, types.FunctionType]:
        #         print(k, type(v))

        # for k, v in mod.__dict__.items():
        #     if not k.startswith('_') and type(v) in [types.FunctionType]:
        #         print(k, type(v))

        # dis.dis(mod)
        # print(dir(mod))
        vm.import_module(mod)

    else:
        src = open('mod.py', 'r').read()
        mod = codeop.compile_command(src, symbol='exec')
        dis.dis(mod.co_code)
        vm.import_src(mod)


    vm.global_vars['_sender'] = '0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266'
    vm.run([], 'init')
    # vm.run([1000], 'mint')
    # vm.run(['0x1111', 1000], 'transfer')

