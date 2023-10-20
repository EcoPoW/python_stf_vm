import dis
import types
import json

import mod_calculate
import vm_calculate

if __name__ == '__main__':
    dis.dis(mod_calculate)
    print(mod_calculate.__package__)

    for k, v in mod_calculate.__dict__.items():
        if not k.startswith('_') and type(v) not in [type, types.FunctionType]:
            print(k, type(v))

    for k, v in mod_calculate.__dict__.items():
        if not k.startswith('_') and type(v) in [types.FunctionType]:
            print(k, type(v))

    vm = vm_calculate.VM()
    vm.import_module(mod_calculate)

    for i in range(10000):
        vm.run([], 'testAllByteCode')
    for key in vm.dict_times.keys():
        vm.dict_gas[key] = (vm.dict_gas[key] / vm.dict_times[key])*1000000

    print(vm.dict_gas)
    with open('gas.json', "w") as json_file:
        json.dump(vm.dict_gas, json_file)
    # print(vm.dict_times)