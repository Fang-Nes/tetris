import os

fout = open('install.py', 'w', encoding='UTF-8')
print('import os', file=fout)
q = input().replace('\\', '/')
s = q.rfind('/') + 1


def dfs(a):
    print(a)
    try:
        w = os.listdir(a)
        print('os.mkdir("' + a[s:] + '")', file=fout)
        for i in w: dfs(a + '/' + i)
    except:
        with open(a, 'rb') as g:
            print("with open('" + a[s:] + "','wb') as f:f.write(" + str(g.read()) + ")", file=fout)


dfs(q)