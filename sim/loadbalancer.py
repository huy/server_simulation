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
  
  def output_capacities(self):
    result=[]
    for server in self.servers:
      for type, val in enumerate(server.output_capacities()):
        if type < len(result):
           result[type]+=val
        else:
           result.append(val)
    return result

  def total_requests(self):
    result = sum([z.total_requests for z in self.servers])
    return result

  def total_wait_time(self):
    result=[]
    for server in self.servers:
      for type, val in enumerate(server.total_wait_time):
        if type < len(result):
           result[type]+=val
        else:
           result.append(val)
    return result
