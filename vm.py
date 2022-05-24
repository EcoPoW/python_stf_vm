
import dis
import opcode
import codeop
import hashlib

import stf


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
print([hex(i) for i in stf.chain_stf.__code__.co_code])
# print(opcode.opmap)

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
        self.co_code = function_object.__code__.co_code
        self.co_varnames = function_object.__code__.co_varnames
        self.co_consts = function_object.__code__.co_consts
        self.co_names = function_object.__code__.co_names
        self.co_argcount = function_object.__code__.co_argcount

        self.pc = 0
        self.stack = []
        self.memory = []

    def run(self, function_name, args):
        pc = -1
        while pc != self.pc:
            pc = self.pc
            r = self.step()
            if r:
                print("return value", r)

    def step(self):
        print(self.pc, hex(self.co_code[self.pc]))
        if self.co_code[self.pc] == 0x0:
            print()

        elif self.co_code[self.pc] == 0x1: # POP_TOP
            self.pc += 2

        elif self.co_code[self.pc] == 0x3c: # STORE_SUBSCR
            self.pc += 2

        elif self.co_code[self.pc] == 0x53: # RETURN_VALUE
            return 'value'

        elif self.co_code[self.pc] == 0x64: # LOAD_CONST
            self.pc += 2

        elif self.co_code[self.pc] == 0x69: # BUILD_MAP
            self.pc += 2

        elif self.co_code[self.pc] == 0x7c: # LOAD_FAST
            param = self.co_code[self.pc+1]
            print('LOAD_FAST', param)
            self.pc += 2

        elif self.co_code[self.pc] == 0x7d: # STORE_FAST
            param = self.co_code[self.pc+1]
            print('STORE_FAST', param)
            self.pc += 2

        elif self.co_code[self.pc] == 0xa0: # LOAD_METHOD
            self.pc += 2

        elif self.co_code[self.pc] == 0xa1: # CALL_METHOD
            self.pc += 2

vm = VM()
vm.import_function(stf.chain_stf)
vm.run('chain_stf', [1, 2])
