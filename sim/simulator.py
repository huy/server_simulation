from pprint import PrettyPrinter
from server import Server
from loadbalancer import LoadBalancer
from generator import RequestGenerator

class Simulator:

  def __init__(self,params):
    number_of_servers=int(params["number_of_servers"])

    self.number_of_requests = int(params["number_of_requests"])
    self.number_of_types = len(params["types_of_requests"])

    self.number_of_requests_per_sec = int(params["number_of_requests_per_sec"])
    self.generator = RequestGenerator(params["types_of_requests"],int(params["number_of_requests_per_sec"]))

    request_type_capacity=[x["output_capacity"] for x in params["types_of_requests"].values()]
    server_capacity = self.distribute_output_capacity(number_of_servers,request_type_capacity)
     
    #print "server capacity:", server_capacity

    servers = [Server(server_capacity[z]) for z in range(number_of_servers)]
    self.loadbalancer = LoadBalancer(servers=servers,method=params["method"])
  
  def distribute_output_capacity(self,number_of_servers,type_capacity):
    server_capacity = [[0 for z in range(self.number_of_types)]
      for server in range(number_of_servers)]

    for z in range(self.number_of_types):
      while (type_capacity[z]>0):
        for server in range(number_of_servers):
          if type_capacity[z] <= 0:
            break
          server_capacity[server][z]+=1
          type_capacity[z]-=1

    return server_capacity
        
  def number_of_servers(self):
    return self.loadbalancer.number_of_servers()

  def total_service_time(self):
    return self.loadbalancer.total_service_time()

  def total_wait_time(self):
    return self.loadbalancer.total_wait_time()

  def total_wait_requests(self):
    return self.loadbalancer.total_wait_requests()

  def number_of_requests_per_type(self):
    return self.loadbalancer.number_of_requests_per_type()

  def number_of_failed_requests_per_type(self):
    return self.loadbalancer.number_of_failed_requests_per_type()

  def simulate(self):
    arrival_time = 0
    reqno = 0
    while True:     
       for req in self.generator.generate(number_of_requests=100):
         reqno += 1
         request_type,delay,service_time=req
         arrival_time += delay

         #print "--- %s arrive at %f" % (request_type,arrival_time)
         self.loadbalancer.process(request_type,arrival_time,service_time)

       if  reqno >=self.number_of_requests:
          break
  
if __name__ == "__main__":
  from sys import argv,exit,stderr
  import yaml
  
  if len(argv) < 2:
    print >> stderr,"Usage:\n\t%s parameters-file [--number_of_servers=2] [--number_of_requests=50000] [--number_of_requests_per_sec=30]" % argv[0] 
    exit(1)

  filename=argv[1]
  input = open(filename) 
  params = yaml.load(input.read())
  input.close() 
  
  for arg in argv[2:]:
    for option in ("--number_of_servers=","--number_of_requests=","--number_of_requests_per_sec=","--method="):
      if arg.startswith(option):
        name,val=arg.split("=")
        params[name[2:]]=val
       
  print >> stderr, "--- simulation's parameters"
  PrettyPrinter().pprint(params)

  sim = Simulator(params)

  sim.simulate()

  print >> stderr, "--- result"

  print "requests per server:",sim.number_of_servers(),[sim.loadbalancer.server(i).total_requests() for i in range(sim.number_of_servers())]
  print "requests per type:",sim.number_of_requests_per_type(),["%.02f %%" % (x*100.0/sim.number_of_requests) for x in sim.number_of_requests_per_type()]
  print "failed requests per type:",sim.number_of_failed_requests_per_type(),["%.02f %%" % (x[0]*100.0/x[1]) for x in zip(sim.number_of_failed_requests_per_type(),sim.number_of_requests_per_type())]
  print "wait requests per type:",sim.total_wait_requests(),["%.02f %%" % (x[0]*100.0/x[1]) for x in zip(sim.total_wait_requests(),sim.number_of_requests_per_type())]
  print "wait time per type:",["%.02f" % x for x in sim.total_wait_time()],["%.02f %%" % (x[0]*100.0/x[1]) for x in zip(sim.total_wait_time(),sim.total_service_time())]

  exit(0)
