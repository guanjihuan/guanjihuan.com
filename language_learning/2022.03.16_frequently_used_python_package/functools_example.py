import functools

def func(x, y, z):
    return x-y+z

partial_func = functools.partial(func, x=5, z=0)
print(partial_func(y=2))