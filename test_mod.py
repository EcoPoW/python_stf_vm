
import dis
import types

import mod
import vm


if __name__ == '__main__':
    dis.dis(mod)
    # print(dir(mod))
    # print(mod.__loader__)
    # print(mod.__builtins__)
    print(mod.__package__)

    for k, v in mod.__dict__.items():
        if not k.startswith('_') and type(v) not in [type, types.FunctionType]:
            print(k, type(v))

    for k, v in mod.__dict__.items():
        if not k.startswith('_') and type(v) in [types.FunctionType]:
            print(k, type(v))

    vm = vm.VM()
    vm.import_module(mod)
    vm.run([], 'init')
    vm.run([1000], 'mint')
    vm.run(['0x1111', 100], 'transfer')
