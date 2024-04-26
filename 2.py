count = 0

def f(n, k):
    if n == 29:
        k = True

    if n == 68 and k is True:
        global count
        count += 1
    elif n < 68:
        f(n+2, k)
        z = 0
        for i in str(n):
            z +=  int(i)
        f(n+z, k)

f(3, False)
print(count)
