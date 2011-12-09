from server import Server

class LoadBalancer:

  def __init__(self,
    servers)
    self.servers = servers
    self.arrival_time = 0

  def process(req):
    request_type,delay,service_time = req
    self.arrival_time = self.arrival_time + delay
    self.find_available_server().process(request_type,self.arrival_time,service_time)

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
