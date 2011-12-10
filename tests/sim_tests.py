import unittest
import yaml
import os

from sim.server import *
from sim.generator import *
from sim.loadbalancer import *
from sim.simulator import *

class TestLoadParameters(unittest.TestCase):
  def setUp(self):
    self.simulator = Simulator(yaml.load(file(os.path.dirname(__file__) + "/sample1.yaml")))
    self.lb = self.simulator.loadbalancer

  def test_load_parameters(self):
    self.assertEqual(6,self.lb.number_of_servers())

    self.assertEqual(30,self.simulator.number_request_per_sec)
    self.assertEqual(50000,self.simulator.number_of_requests)

  def test_distribute_output_capacity(self):
    self.assertEqual([20,60],self.lb.output_capacities())

    for serverno in [0,1]:
      self.assertEqual([4,10],self.lb.server(serverno).output_capacities())
    for serverno in [2,3,4,5]:
      self.assertEqual([3,10],self.lb.server(serverno).output_capacities())

class TestLoadBalancer(unittest.TestCase):
  def test_elect_server_with_less_load(self):
     s1 = Server(output_capacities=[5,5])
     s1.total_number_requests=100
     s2 = Server(output_capacities=[5,5])
     s2.total_number_requests=109

     lb = LoadBalancer(servers=[s1,s2])
     self.assertEqual(s1,lb.elect_server())

class TestServer(unittest.TestCase):
  def test_find_first_available_channel(self):
     s = Server(output_capacities=[3,2])

     s.channels = [[3.0,2.1,1.5],[0.0,2.5]]

     self.assertEqual(2,s.find_first_available_channel(request_type=0)[0])
     self.assertEqual(1.5,s.find_first_available_channel(request_type=0)[1])

     self.assertEqual(0,s.find_first_available_channel(request_type=1)[0])
     self.assertEqual(0.0,s.find_first_available_channel(request_type=1)[1])

class TestGenerator(unittest.TestCase):
  def test_generate_request(self):
    generator = RequestGenerator([0.05,0.95],[2.5,0.75],30)
      
    num_type1,num_type2 = 0.0,0.0
    total_time = 0.0
    
    num_type2_closed_to_mean = 0.0
    delta = 0.3

    for type,arrival_time,service_time in generator.generate(10000):
      if type==0:
        num_type1+=1
      else:
        num_type2+=1
        if service_time > 0.75 - delta and service_time < 0.75 + delta:
          num_type2_closed_to_mean+=1

      total_time+=arrival_time

    # assert below may fail but very unlikely, this is to make sure that generator 
    # do the good job
    self.assertTrue(num_type1>5) 
    self.assertTrue(num_type2>9000)

    actual_rate = 10000/total_time
    self.assertTrue(actual_rate>25)
    self.assertTrue(actual_rate<35)

    print num_type2_closed_to_mean,num_type2
    self.assertTrue((num_type2_closed_to_mean/num_type2) > 0.5)

if __name__ == '__main__':
    unittest.main()
