import time


if __name__ == '__main__':
    start = time.time()
    list = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    #
    # r = its.product(list, repeat=4)
    # for i in r:
    #     print(i)
    num = 0
    for i in (a + b + c + d for a in list for b in list for c in list for d in list):
        num = num + 1
        print(i)

    end = time.time()

    print(end-start)
    print(num)