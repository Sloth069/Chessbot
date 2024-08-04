#!/bin/python3

import math
import os
import random
import re
import sys



if __name__ == '__main__':
    n = int(input().strip())
    if n % 2:
        print("Weird")
    elif n in range(6, 20):
        print("Weird")
    else:
        print("Not Weird")


