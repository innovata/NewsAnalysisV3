
from inews.base import iter, dbg
import unittest
import inspect
import pprint
pp = pprint.PrettyPrinter(indent=2)


# @unittest.skip("test")
class BaselineTestCase(unittest.TestCase):

    @dbg.utestfunc
    def test01__pageurls(self):
        def f(pageurl):
            pass

        iter.pageurls(f=f, initurl=None)



if __name__ == "__main__":
    unittest.main()
