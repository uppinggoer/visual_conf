# -*- coding: utf-8 -*-

def assert_error(self, message, func):
    try:
        func()
        assert 0
    except AssertionError as e:
        self.assertEqual(e.message, message)