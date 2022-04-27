
import dis
import opcode
import stf

dis.dis(stf.chain_stf)
print([i for i in stf.chain_stf.__code__.co_code])
print(opcode.opmap)

print(stf.chain_stf.__code__.co_name)
print(stf.chain_stf.__code__.co_varnames)
print(stf.chain_stf.__code__.co_argcount)

print(stf.chain_stf.__code__.co_consts)
print(stf.chain_stf.__code__.co_names) # for method

print(stf.chain_stf.__code__.co_stacksize)
print(stf.chain_stf.__code__.co_posonlyargcount)
print(stf.chain_stf.__code__.co_nlocals)
print(stf.chain_stf.__code__.co_kwonlyargcount)
print(stf.chain_stf.__code__.co_cellvars)
print(stf.chain_stf.__code__.co_freevars)

class VM:
    def import_function(self, function_object):
        pass

    def run(self, function_name, args):
        pass


vm = VM()
vm.import_function(stf.chain_stf)
vm.run('chain_stf', [1, 2])
