s = input()


def diff():
    pass


s = s.replace('cos', 'c').replace('sin', 's').replace('ln', 'l').replace('exp', 'e').replace('tan', 't')
parenth_closed = {}
parenth_indices = []
k = 0
for c in s:
    if c == '(':
        parenth_indices.append(k)
    if c == ')':
        parenth_closed[parenth_indices.pop()] = k
    k += 1
print(parenth_closed)