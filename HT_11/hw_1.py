class Calc(object):
    last_result = None

    def sum_res(self, dig_1: float, dig_2: float) -> float:
        self.last_result = dig_1+dig_2
        return self.last_result

    sum_res.__doc__ = 'addition of numbers'

    def mul_res(self, dig_1: float, dig_2: float) -> float:
        self.last_result = dig_1*dig_2
        return self.last_result

    mul_res.__doc__ = 'multiplication of numbers'

    def diff_res(self, dig_1: float, dig_2: float) -> float:
        #difference `dig_1` and `dig_2`
        self.last_result = dig_1-dig_2
        return self.last_result

    def division_res(self, dig_1: float, dig_2: float) -> float:
        #division `dig_1` and `dig_2`
        self.last_result = dig_1/dig_2
        return self.last_result

a = Calc()
print(a.last_result)

print('sum: ', a.sum_res(1, 2))
print(a.last_result)

print('mul ', a.mul_res(12, 8))
print(a.last_result)

print('dif ', a.diff_res(25, 6))
print(a.last_result)

print('div ', a.division_res(10, 2))
print(a.last_result)

print(a.sum_res(a.last_result, 12))
print(a.last_result)

print(help(a.sum_res))