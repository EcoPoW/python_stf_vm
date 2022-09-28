
import dis
import codeop
import hashlib
import functools

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

class VM:
    def import_function(self, function_object):
        self.co_code = function_object.__code__.co_code
        self.co_varnames = function_object.__code__.co_varnames
        self.co_consts = function_object.__code__.co_consts
        self.co_names = function_object.__code__.co_names
        self.co_argcount = function_object.__code__.co_argcount

        self.pc = 0
        self.stack = []
        self.vars = {}

    def run(self, function_name, args):
        assert len(args) == self.co_argcount
        self.args = args
        for i, v in enumerate(self.args):
            self.vars[self.co_varnames[i]] = v
        print('---')

        pc = -1
        while pc != self.pc:
            pc = self.pc
            r = self.step()
            if r:
                print("return value", r)

    def step(self):
        print(self.pc, hex(self.co_code[self.pc]))
        print('vars', self.vars)
        if self.co_code[self.pc] == 0x0:
            print()

        elif self.co_code[self.pc] == 0x1: # POP_TOP
            print('POP_TOP')
            self.stack.pop()
            self.pc += 2

        elif self.co_code[self.pc] == 0x3c: # STORE_SUBSCR
            key = self.stack.pop()
            obj = self.stack.pop()
            val = self.stack.pop()
            print('STORE_SUBSCR', obj, '[', key, '] =', val)

            left = self.vars[obj]
            right = self.vars[val]
            left[key] = right
            # self.stack.append(left)
            self.pc += 2

        elif self.co_code[self.pc] == 0x53: # RETURN_VALUE
            print('RETURN_VALUE')
            val = self.stack[-1]
            var = self.vars[val]
            return var

        elif self.co_code[self.pc] == 0x17: # BINARY_ADD
            print('BINARY_ADD')
            # pop the op number
            tos = int.from_bytes(self.stack.pop())
            tos1 = int.from_bytes(self.stack.pop())
            result = (tos+tos1).to_bytes(32)
            self.stack.append(result)
            self.pc += 1

        elif self.co_code[self.pc] == 0x14: # BINARY_MULTIPLY
            print('BINARY_MULTIPLY')
            # pop the op number
            tos = int.from_bytes(self.stack.pop())
            tos1 = int.from_bytes(self.stack.pop())
            result = (tos*tos1).to_bytes(32)
            self.stack.append(result)
            self.pc += 1

        elif self.co_code[self.pc] == 0x13: # BINARY_POWER
            print('BINARY_POWER')
            # pop the op number
            tos = int.from_bytes(self.stack.pop())
            tos1 = int.from_bytes(self.stack.pop())
            result = (tos**tos1).to_bytes(32)
            self.stack.append(result)
            self.pc += 1

        elif self.co_code[self.pc] == 0x15: # BINARY_DIVIDE
            print('BINARY_DIVIDE')
            # pop the op number
            tos = int.from_bytes(self.stack.pop())
            tos1 = int.from_bytes(self.stack.pop())
            result = (tos1/tos).to_int(32).to_bytes(32)
            self.stack.append(result)
            self.pc += 1

        elif self.co_code[self.pc] == 0x16: # BINARY_MODULO
            print('BINARY_MODULO')
            # pop the op number
            tos = int.from_bytes(self.stack.pop())
            tos1 = int.from_bytes(self.stack.pop())
            result = (tos1%tos).to_bytes(32)
            self.stack.append(result)
            self.pc += 1            

        elif self.co_code[self.pc] == 0x18: # BINARY_SUBTRACT
            print('BINARY_SUBTRACT')
            tos = int.from_bytes(self.stack.pop())
            tos1 = int.from_bytes(self.stack.pop())
            result = (tos1-tos).to_bytes(32)
            self.stack.append(result)
            self.pc += 1

        
        elif self.co_code[self.pc] == 0x1a: # BINARY_FLOOR_DIVIDE
            print('BINARY_FLOOR_DIVIDE')
            tos = int.from_bytes(self.stack.pop())
            tos1 = int.from_bytes(self.stack.pop())
            result = (tos1 // tos).to_bytes(32)
            self.stack.append(result)
            self.pc += 1

        elif self.co_code[self.pc] == 0x1a: # BINARY_TRUE_DIVIDE
            print('BINARY_TRUE_DIVIDE')
            tos = int.from_bytes(self.stack.pop())
            tos1 = int.from_bytes(self.stack.pop())
            result = (tos1 / tos).to_bytes(32)
            self.stack.append(result)
            self.pc += 1

        elif self.co_code[self.pc] == 0x64: # LOAD_CONST
            param = self.co_code[self.pc+1]
            print('LOAD_CONST', param)
            self.stack.append(self.co_consts[param])
            self.pc += 2

        elif self.co_code[self.pc] == 0x69: # BUILD_MAP
            param = self.co_code[self.pc+1]
            print('BUILD_MAP', param)
            if param == 0:
                self.stack.append({})
            self.pc += 2

        elif self.co_code[self.pc] == 0x7c: # LOAD_FAST
            param = self.co_code[self.pc+1]
            print('LOAD_FAST', param)
            var = self.co_varnames[param]
            self.stack.append(var)
            self.pc += 2

        elif self.co_code[self.pc] == 0x7d: # STORE_FAST
            param = self.co_code[self.pc+1]
            print('STORE_FAST', param)
            # print('STORE_FAST', self.co_varnames[param])
            var = self.co_varnames[param]
            val = self.stack.pop()
            self.vars[var] = val
            self.pc += 2

        elif self.co_code[self.pc] == 0xa0: # LOAD_METHOD
            param = self.co_code[self.pc+1]
            print('LOAD_METHOD', param)
            self.stack.append(self.co_names[param])
            self.pc += 2

        elif self.co_code[self.pc] == 0xa1: # CALL_METHOD
            param = self.co_code[self.pc+1]
            print('CALL_METHOD', param)
            # print('CALL_METHOD', self.stack[-2-param])
            var = self.vars[self.stack[-2-param]]
            method = self.stack[-1-param]
            params = self.stack[-param:]
            result = functools.partial(var.__getattribute__(method), *params)()
            print('result', result)
            self.stack = self.stack[:-2-param]
            self.stack.append(result)
            self.pc += 2

        print('stack', self.stack)
        print('---')

vm = VM()
vm.import_function(stf.chain_stf)
vm.run('chain_stf', [{}, {'subchains': {1:2}}])
