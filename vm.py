
import dis
import codeop
import hashlib
import functools
import types
import mock

class VM:
    def __init__(self):
        self.module_object = None
        self.co_code = None

    def import_function(self, function_object, global_vars = {}):
        self.co_code = function_object.__code__.co_code
        self.co_varnames = function_object.__code__.co_varnames
        self.co_consts = function_object.__code__.co_consts
        self.co_names = function_object.__code__.co_names
        self.co_argcount = function_object.__code__.co_argcount

        self.pc = 0
        self.stack = []
        self.local_vars = {}
        self.global_vars = global_vars

    def import_module(self, module_object):
        self.module_object = module_object

    def run(self, args, function_name = None):
        if self.module_object and function_name:
            function_object = self.module_object.__dict__[function_name]
            assert type(function_object) == types.FunctionType
            global_vars = {'msg': mock.msg}
            self.import_function(function_object, global_vars)

        assert self.co_code
        # assert self.co_varnames
        # assert self.co_consts
        # assert self.co_names
        assert self.co_argcount == len(args)
        self.args = args
        for i, v in enumerate(self.args):
            self.local_vars[self.co_varnames[i]] = v
        print('---')

        pc = -1
        while pc != self.pc:
            pc = self.pc
            r = self.step()
            if r:
                print("return value", r)

    def step(self):
        print('PC', self.pc, hex(self.co_code[self.pc]))
        print('local_vars', self.local_vars)
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

        elif self.co_code[self.pc] == 0x18: # BINARY_SUBTRACT
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

        elif self.co_code[self.pc] == 0x61: # STORE_GLOBAL
            param = self.co_code[self.pc+1]
            val = self.stack.pop()
            global_var = self.co_names[param]
            print('STORE_GLOBAL', param, global_var, val)
            self.global_vars[global_var] = val
            self.pc += 2

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
            right = self.stack.pop()
            left = self.stack.pop()
            print('COMPARE_OP', param, left, right)
            if param == 0:
                self.stack.append(left < right)
            elif param == 1:
                self.stack.append(left <= right)
            elif param == 2:
                self.stack.append(left == right)
            elif param == 3:
                self.stack.append(left != right)
            elif param == 4:
                self.stack.append(left > right)
            elif param == 5:
                self.stack.append(left >= right)

            self.pc += 2

        elif self.co_code[self.pc] == 0x71: # JUMP_ABSOLUTE
            param = self.co_code[self.pc+1]
            print('JUMP_ABSOLUTE', param)
            self.pc = param

        elif self.co_code[self.pc] == 0x72: # POP_JUMP_IF_FALSE
            param = self.co_code[self.pc+1]
            print('POP_JUMP_IF_FALSE', param)
            val = self.stack.pop()
            if val:
                self.pc += 2
            else:
                self.pc = param

        elif self.co_code[self.pc] == 0x74: # LOAD_GLOBAL
            param = self.co_code[self.pc+1]
            global_var = self.co_names[param]
            print('LOAD_GLOBAL', param, global_var)
            val = self.global_vars[global_var]
            self.stack.append(val)
            self.pc += 2

        elif self.co_code[self.pc] == 0x7c: # LOAD_FAST
            param = self.co_code[self.pc+1]
            print('LOAD_FAST', param)
            varname = self.co_varnames[param]
            val = self.local_vars[varname]
            self.stack.append(val)
            self.pc += 2

        elif self.co_code[self.pc] == 0x7d: # STORE_FAST
            param = self.co_code[self.pc+1]
            print('STORE_FAST', param)
            # print('STORE_FAST', self.co_varnames[param])
            var = self.co_varnames[param]
            val = self.stack.pop()
            self.local_vars[var] = val
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
