
import dis
import codeop
import hashlib
import functools

import stf


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
        if self.co_code[self.pc] == 0x0: # NOP
            print('NOP')

        elif self.co_code[self.pc] == 0x1: # POP_TOP
            print('POP_TOP')
            self.stack.pop()
            self.pc += 2

        elif self.co_code[self.pc] == 0x13: # BINARY_POWER
            exp = self.stack.pop()
            base = self.stack.pop()
            print('BINARY_POWER', base, exp)
            self.stack.append(base ** exp)
            self.pc += 2

        elif self.co_code[self.pc] == 0x14: # BINARY_MULTIPLY
            right = self.stack.pop()
            left = self.stack.pop()
            print('BINARY_MULTIPLY', left, right)
            self.stack.append(left*right)
            self.pc += 2

        elif self.co_code[self.pc] == 0x17: # BINARY_ADD
            right = self.stack.pop()
            left = self.stack.pop()
            print('BINARY_ADD', left, right)
            self.stack.append(left+right)
            self.pc += 2

        elif self.co_code[self.pc] == 0x17: # BINARY_SUBTRACT
            right = self.stack.pop()
            left = self.stack.pop()
            print('BINARY_SUBTRACT', left, right)
            self.stack.append(left-right)
            self.pc += 2

        elif self.co_code[self.pc] == 0x1b: # BINARY_TRUE_DIVIDE
            right = self.stack.pop()
            left = self.stack.pop()
            print('BINARY_TRUE_DIVIDE', left, right)
            self.stack.append(left/right)
            self.pc += 2

        elif self.co_code[self.pc] == 0x37: # INPLACE_ADD
            val = self.stack.pop()
            obj = self.stack.pop()
            print('INPLACE_ADD', obj, '+=', val)

            self.stack.append(obj + val)
            self.pc += 2

        elif self.co_code[self.pc] == 0x38: # INPLACE_SUBTRACT
            val = self.stack.pop()
            obj = self.stack.pop()
            print('INPLACE_SUBTRACT', obj, '-=', val)

            self.stack.append(obj - val)
            self.pc += 2

        elif self.co_code[self.pc] == 0x3c: # STORE_SUBSCR
            key = self.stack.pop()
            obj = self.stack.pop()
            val = self.stack.pop()
            print('STORE_SUBSCR', obj, '[', key, '] =', val)

            obj[key] = val
            self.pc += 2

        elif self.co_code[self.pc] == 0x53: # RETURN_VALUE
            val = self.stack.pop()
            print('RETURN_VALUE', val)
            return val

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

        elif self.co_code[self.pc] == 0x6b: # COMPARE_OP
            param = self.co_code[self.pc+1]
            val = self.stack.pop()
            print('COMPARE_OP', param, val)
            if param == val:
                self.stack.append(True)
            else:
                self.stack.append(False)
            self.pc += 2

        elif self.co_code[self.pc] == 0x72: # POP_JUMP_IF_FALSE
            param = self.co_code[self.pc+1]
            print('POP_JUMP_IF_FALSE', param)
            val = self.stack.pop()
            if val:
                self.pc += 2
            else:
                self.pc = param

        elif self.co_code[self.pc] == 0x7c: # LOAD_FAST
            param = self.co_code[self.pc+1]
            print('LOAD_FAST', param)
            varname = self.co_varnames[param]
            val = self.vars[varname]
            self.stack.append(val)
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
            var = self.stack[-2-param]
            method = self.stack[-1-param]
            params = self.stack[-param:]
            result = functools.partial(var.__getattribute__(method), *params)()
            print('result', result)
            self.stack = self.stack[:-2-param]
            self.stack.append(result)
            self.pc += 2

        print('stack', self.stack)
        print('---')


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

    vm = VM()
    vm.import_function(stf.chain_stf)
    vm.run('chain_stf', [{}, {'subchains': {1:2}}])
