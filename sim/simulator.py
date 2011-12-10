from server import Server
from loadbalancer import LoadBalancer
from generator import RequestGenerator

class Simulator:

  def __init__(self,params):
    number_of_servers=params["number_of_servers"]
    request_type_capacity=[x["output_capacity"] for x in params["types_of_requests"].values()]
    request_type_distribution=[x["proportion"] for x in params["types_of_requests"].values()]
    request_type_mean_time=[x["avg_service_time_secs"] for x in params["types_of_requests"].values()]
    arrival_rate=params["number_request_per_sec"]

    self.number_of_requests = params["number_of_requests"]
    self.number_request_types = len(request_type_distribution)

    self.generator = RequestGenerator(request_type_distribution,
      request_type_mean_time,
      arrival_rate)

    server_capacity = self.distribute_output_capacity(number_of_servers,request_type_capacity)
     
    #print "server capacity:", server_capacity

    servers = [Server(server_capacity[z]) for z in range(number_of_servers)]
    self.loadbalancer = LoadBalancer(servers)
  
  def distribute_output_capacity(self,number_of_servers,request_type_capacity):
    server_capacity = [[0 for z in range(self.number_request_types)]
      for server in range(number_of_servers)]

    for z in range(self.number_request_types):
      while (request_type_capacity[z]>0):
        for server in range(number_of_servers):
          if request_type_capacity[z] <= 0:
            break
          server_capacity[server][z]+=1
          request_type_capacity[z]-=1

    return server_capacity
        
  def total_wait_time(self):
    return self.loadbalancer.total_wait_time()

  def simulate(self):
    arrival_time = 0
    while True:     
       for req in self.generator.generate(number_of_requests=100):
         self.loadbalancer.process(req)

       if  self.loadbalancer.total_requests()>=self.number_of_requests:
          break
  
if __name__ == "__main__":
  from sys import argv,exit,stderr
  import yaml
  
  if len(argv) < 2:
    print >> stderr,"Usage:\n\t%s parameters-file",argv[0] 
    exit(1)

  script,filename=argv
  input = open(filename) 
  params = yaml.load(input.read())
  input.close() 
  
  simulator = Simulator(params)

  simulator.simulate()

  print "wait time:",simulator.total_wait_time()

  exit(0)
