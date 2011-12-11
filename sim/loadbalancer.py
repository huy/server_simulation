from server import Server

class LoadBalancer:

  def __init__(self,servers):
    self.servers = servers
    self.arrival_time = 0

  def number_of_servers(self):
    return len(self.servers)

  def server(self,index):
    return self.servers[index]

  def process(self,req):
    request_type,delay,service_time = req
    self.arrival_time = self.arrival_time + delay
    self.elect_server().process(request_type,self.arrival_time,service_time)

  def elect_server(self):
    server,min = self.servers[0],self.servers[0].total_requests
    for z in self.servers:
      if z.total_requests < min:
        min = z.total_requests
        server = z
    return server
  
  def calculate_servers_stats(self,func):
    result=[]
    for server in self.servers:
      for type, val in enumerate(func(server)):
        if type < len(result):
           result[type]+=val
        else:
           result.append(val)
    return result

  def output_capacities(self):
    return self.calculate_servers_stats(lambda s: s.output_capacities())

  def total_requests(self):
    return self.calculate_servers_stats(lambda s: s.total_requests)

  def total_wait_time(self):
    return self.calculate_servers_stats(lambda s: s.total_wait_time)

  def total_wait_requests(self):
    return self.calculate_servers_stats(lambda s: s.total_wait_requests)

