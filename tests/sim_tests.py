import unittest
from sim.server import *

class TestServer(unittest.TestCase):

  def test_process_request(self):
    self.assertEqual(1,1)

if __name__ == '__main__':
    unittest.main()
