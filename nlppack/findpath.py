import os

sep = '/' if os.name != 'nt' else '\\'
cwd = os.getcwd().split(sep)
while len(cwd) > 1 and cwd[-1] != 'JX3Price':
    cwd.pop()
cwd.append('nlppack')
cwd.append('data')
def nlppath(name):
    return sep.join(cwd + [name])
