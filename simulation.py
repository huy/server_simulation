import numpy
import scipy.stats
from server import Server
from generator import RequestGenerator

class WaitTimeSimulator:

  def __init__(self,
    number_of_servers,
    request_type_capacity,
    request_type_distribution,
    request_type_mean_time,
    arrival_rate):

    self.number_request_types = len(request_type_distribution)

    self.generator = RequestGenerator(request_type_distribution,
      request_type_mean_time,
      arrival_rate)

    server_capacity = self.distribute_server_capacity(number_of_servers,request_type_capacity)
     
    print "server capacity:", server_capacity

    self.servers = [Server(server_capacity[z]) for z in range(number_of_servers)]
  
  def distribute_server_capacity(self,number_of_servers,request_type_capacity):
    server_capacity = [[0 for z in range(self.number_request_types)]
      for server in range(number_of_servers)]

    for z in range(self.number_request_types):
      #print "request type:",z,",capacity:",request_type_capacity[z]
      while (request_type_capacity[z]>0):
        for server in range(number_of_servers):
          if request_type_capacity[z] <= 0:
            break
          server_capacity[server][z]+=1
          request_type_capacity[z]-=1

    return server_capacity
        

  def simulate(self,max_observed_requests):
    arrival_time = 0
    while True:     
       for req in self.generator.generate(100):
         request_type,delay,service_time = req
         arrival_time = arrival_time + delay
         self.find_available_server().process(request_type,arrival_time,service_time)

       if  self.total_requests()>=max_observed_requests:
          break
  
  def find_available_server(self):
    server,min = self.servers[0],self.servers[0].total_requests
    for z in self.servers:
      if z.total_requests < min:
        min = z.total_requests
        server = z
    return server
  
  def total_requests(self):
    result = sum([z.total_requests for z in self.servers])
    return result

  def total_wait_time(self):
    result = []
    for z in range(self.number_request_types):
      result.append(sum([server.total_wait_time[z] for server in self.servers]))
    return result
     
if __name__ == "__main__":
  from sys import argv,exit,stderr
  
  if len(argv) < 2:
    number_of_servers = 6
  else:
    number_of_servers = int(argv[1]) 

  if len(argv) < 3:
    max_observed = 5000
  else:
    max_observed = int(argv[2])

  simulator = WaitTimeSimulator(
    number_of_servers=number_of_servers,
    request_type_capacity=[20,600],
    request_type_distribution=[0.05, 0.95],
    request_type_mean_time=[4.5, 1.15],
    arrival_rate=30.0)

  simulator.simulate(max_observed)

  print "total requests:",simulator.total_requests()
  print "wait time:",simulator.total_wait_time()

