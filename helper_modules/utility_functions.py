'''
    Constant property function.
'''
def constant(f):
    def fset(self, value):
        raise TypeError
    def fget(self):
        return f()
    return property(fget, fset)


# Find the key with the greatest value
def keywithmaxval(d):
    return max(d, key = lambda k: d[k])