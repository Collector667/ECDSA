import hashlib
import random

def find_inverse(number, modulus):
    return pow(number, -1, modulus)

class Config:
    def __init__(self, a, b, p):
        self.a = a
        self.b = b
        self.p = p

class Point:
    def __init__(self, xCoor, yCoor, curveConfig):
        a = curveConfig.a
        b = curveConfig.b
        p = curveConfig.p
        if (yCoor ** 2) % p != (xCoor ** 3 + a * xCoor + b) % p:
            self.x = 0
            self.y = 0
            self.curveConfig = curveConfig
        else:
            self.x = xCoor
            self.y = yCoor
            self.curveConfig = curveConfig

    def is_equal_to(self, point):
        return self.x == point.x  and self.y  == point.y

    def add(self, point):
        p = self.curveConfig.p
        if self.is_equal_to(point):
            if point.y % p == 0:
                return Point(0, 0, self.curveConfig)
            else:
                slope = (3 * point.x ** 2) * find_inverse(2 * point.y, p) % p
        else:
            if self.x == point.x:
                return Point(0, 0, self.curveConfig)
            slope = (point.y - self.y) * find_inverse(point.x - self.x, p) % p

        x = (slope ** 2 - point.x - self.x) % p
        y = (slope * (self.x - x) - self.y) % p
        return Point(x, y, self.curveConfig)

    def multiply(self, times):
        current_point = self
        current_coefficient = 1

        previous_points = []
        while current_coefficient < times:
            previous_points.append((current_coefficient, current_point))
            if 2 * current_coefficient <= times:
                current_point = current_point.add(current_point)

                current_coefficient = 2 * current_coefficient
            else:
                next_point = self
                next_coefficient = 1
                for (previous_coefficient, previous_point) in previous_points:
                    if previous_coefficient + current_coefficient <= times:
                        if previous_point.x != current_point.x:
                            next_coefficient = previous_coefficient
                            next_point = previous_point
                current_point = current_point.add(next_point)
                current_coefficient = current_coefficient + next_coefficient

        return current_point

def sign_text(text, private_key):
    textHash = int(hashlib.sha256(text).hexdigest(), 16)

    k = random.randint(1, n-1)
    r_point = Gpoint.multiply(k)
    r = r_point.x % n
    if r == 0:
        return sign_text(text, private_key)

    k_inverse = find_inverse(k, n)
    s = k_inverse * (textHash + r * private_key) % n
    if s == 0:
        return sign_text(text, private_key)
    return r, s

def verify_signature(signature, text, public_key):
    (r, s) = signature
    s_inverse = find_inverse(s, n)
    textHash = int(hashlib.sha256(text).hexdigest(), 16)
    u = (textHash * s_inverse) % n
    v = (r * s_inverse) % n
    c_point = Gpoint.multiply(u).add(public_key.multiply(v))
    return c_point.x % n== r

testcurveConfig = Config(0, 1, 49999)
#1399 Порядок n для точки 519 , 34
secp256k1_curve_config = Config(0, 7, 115792089237316195423570985008687907853269984665640564039457584007908834671663)
x = 55066263022277343669578718895168534326250603453777594175500187360389116729240
y = 32670510020758816978083085130507043184471273380659243275938904335757337482424
n = 115792089237316195423570985008687907852837564279074904382605163141518161494337
Gpoint = Point(x, y, secp256k1_curve_config)


privateKey = 1341341
text1 = "Vasda"
text1 = text1.encode('utf-8')
publicKey1 = Gpoint.multiply(privateKey)
sign = sign_text(text1, privateKey)
print(f"Подпись {sign}")
print(f"Верификация {verify_signature(sign, text1, publicKey1)}")


