import unittest
import yaml
import os
from sim.server import *
from sim.generator import *
from sim.loadbalancer import *
from sim.simulator import *

class TestServer(unittest.TestCase):

  def test_load_parameters(self):
    simulator = Simulator(yaml.load(file(os.path.dirname(__file__) + "/sample1.yaml")))
    lb = simulator.loadbalancer

    self.assertEqual(6,lb.number_of_servers())
    self.assertEqual([4,10],lb.server(0).output_capacity())
    self.assertEqual([3,10],lb.server(5).output_capacity())

if __name__ == '__main__':
    unittest.main()
