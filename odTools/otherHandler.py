import sys
import os

def dict_merge(a, b):
    c = a.copy()
    c.update(b)
    return c