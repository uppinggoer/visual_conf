# -*- coding: utf-8 -*-
import os

test_path = os.path.abspath(os.path.dirname(__file__)) + "/test/"
print test_path

if __name__ == '__main__':
    import unittest
    s = unittest.TestSuite()
    loader = unittest.TestLoader()
    s.addTests(loader.discover(test_path))
    run = unittest.TextTestRunner()
    run.run(s)