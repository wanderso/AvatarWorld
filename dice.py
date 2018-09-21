import random

class Dice:
    @staticmethod
    def d20():
        return random.randint(1, 20)

    @staticmethod
    def d10():
        return random.randint(1, 10)

    @staticmethod
    def d4():
        return random.randint(1, 4)

    @staticmethod
    def ndn(n, m):
        ret_val = 0
        for _ in range(n):
            ret_val += random.randint(1,m)
        return ret_val
