
from main import Config, Point
p = 49999
array = []

for i in range(p//100):
    for j in range(p//10):
        if (i**2) % p == (j ** 3  + 1) % p:
            array.append([j, i])
testcurveConfig = Config(0, 1, p)


primes = [i for i in range(p + 1)]
mas = []
primes[1] = 0
i = 2
while i <= p:
    if primes[i] != 0:
        j = i + i
        while j <= p:
            primes[j] = 0
            j = j + i
    i += 1

primes = [i for i in primes if i != 0]
mas = [i+1 for i in primes]
print("----")
#Выбираем точку и расчитываем для нее порядок n, если точка при умножении на число дает бесконечно удаленную
#точку то выбираем другую точку

for q in array:
    Gpoint = Point(q[0], q[1], testcurveConfig)
    for i in range(100, 300):
        i = mas[i]
        Gpoint.multiply(i)
        if (Gpoint.is_equal_to(Gpoint.multiply(i))):
            print(i-1, f"Порядок n для точки {Gpoint.x} , {Gpoint.y}")
            break
#Важно, чтобы порядок образовывал кольцо,



