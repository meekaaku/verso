#!/usr/bin/python
from dynamixel_sdk import *
from lib.mkDynamixel import mkDynamixel


def tester():
    return 1, 2, 3

print("Hello")

result = tester()
print(result)

j1 = mkDynamixel(1, 1, 1, 1)
j1.connect()

