from random import randint

def gene_id(num=6, letter=False, lower=False):
    origin = '1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
    rang = 10
    if letter:
        rang = 62
        if lower:
            rang = 36
    res = ''
    for i in range(num):
        res = res + origin[randint(0, rang-1)]
    return res

def unpack_id(s):
    arr = s.split('&')
    res = {}
    for i in range(len(arr)):
        res[i] = arr[i].split(',')
        if '' in res[i]:
           res[i].remove('')
    return res

def pack_id(dic):
    arr = []
    for i in dic:
        arr.append(','.join(dic[i]))
    res = '&'.join(arr)
    return res


if __name__ == '__main__':
    test_arr = ['&', '1&', '&a', '2&3,4']
    for i in test_arr:
        #print(i)
        #print(unpack_id(i))
        #print(pack_id(unpack_id(i)))
        print(i, unpack_id(i), pack_id(unpack_id(i)))

