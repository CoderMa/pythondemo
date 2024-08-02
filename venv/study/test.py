import sys

# print(range(5))
# print(type(range(5)))
# print(list(range(5)))
#
# print(1, 2, 2, file=sys.stdout)
# print(1, 2, 3, file=sys.stderr)

print([x + 1 for x in range(42)])

print(sys.intern("abc1234567890"))

result = [i for i in range(10)]
print(type(result))
print(result)

result2 = list(range(10))
print("type of result2:", type(result2))
print(result2)
