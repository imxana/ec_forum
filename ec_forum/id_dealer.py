from random import randint
import datetime

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
        while '' in res[i]:
           res[i].remove('')
    return res

def pack_id(dic):
    arr = []
    for i in dic:
        arr.append(','.join(dic[i]))
    res = '&'.join(arr)
    return res

def gmt_to_timestamp(TIME='now'):
    GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'
    if TIME == 'now':
        t = datetime.datetime.utcnow()
        return int(t.timestamp())
    t = datetime.datetime.strptime(TIME, GMT_FORMAT)
    return int(t.timestamp())




if __name__ == '__main__':
    # for i in range(10):
    #     print(gene_id(num=6, letter=True, lower=True))


    print(gmt_to_timestamp())
    print(gmt_to_timestamp(TIME="Tue, 11 Oct 2016 23:20:45 GMT"))
    # test_arr = ['&', '1&', '&a', '2&3,4','32','&,,,&',',&','&,','哈哈','哈&_','&哈哈']
    # for i in test_arr:
    #     print(i, unpack_id(i), pack_id(unpack_id(i)))
