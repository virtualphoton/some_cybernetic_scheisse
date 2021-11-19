def gen(n):
    q = [[''] * n for _ in range(n)]
    for i in range(n):
        q[i][(i * 2) % n] = '0'
        q[i][(i * 2 + 1) % n] = '1'
    for i in range(n - 1, 0, -1):
        q[i][i] = f'({q[i][i]})*' if len(q[i][i]) else ''
        for j in range(i):
            for k in range(i):
                if q[j][i] and q[i][k]:
                    q[j][k] = ''.join((f'{q[j][k]}|' if q[j][k] else '',
                                       f'({q[j][i]})' if len(q[j][i]) > 1 else q[j][i],
                                       f'({q[i][i]})' if len(q[i][i]) > 1 else q[i][i],
                                       f'({q[i][k]})' if len(q[i][i]) > 1 else q[i][k]))
    return f'({q[0][0].replace("(", "(?:")})+$'


a = gen(1)
print(len(a))
print(a)
