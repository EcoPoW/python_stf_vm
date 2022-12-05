
import dis
import types

import mod

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
