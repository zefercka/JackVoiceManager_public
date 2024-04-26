c = 0
for i in range(271453, 10**7):
    x = i
    l, m = 0, 0
    while x > 0:
        l += 1
        if x % 12 == 0:
            m += 1
        x = x//12

    if l == 6 and m == 0:
        c += 1

print(c)
