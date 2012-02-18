from server import Server

class LoadBalancer:

  def __init__(self,servers,method="roundrobin"):
    self.servers = servers
    self.method = method

  def number_of_servers(self):
    return len(self.servers)

  def server(self,index):
    return self.servers[index]

  def process(self,req,arrival_time):
    request_type,delay,service_time = req
    self.elect_server(arrival_time).process(request_type,arrival_time,service_time)

  def elect_server(self,arrival_time):
    if self.method == "roundrobin":
       return self.elect_server_by_roundrobin()
    if self.method == "busyness":
       return self.elect_server_by_busyness(arrival_time)
    raise Exception("unknown balancer method %s" % self.method)
    
  def elect_server_by_roundrobin(self):
    server,min = self.servers[0],self.servers[0].total_requests()
    for z in self.servers:
      if z.total_requests() < min:
        min = z.total_requests()
        server = z
    return server

  def elect_server_by_busyness(self,arrival_time):
    server,min = self.servers[0],self.servers[0].number_of_pending_requests(arrival_time)
    for z in self.servers:
      if z.number_of_pending_requests(arrival_time) < min:
        min = z.number_of_pending_requests(arrival_time)
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

  def number_of_requests_per_type(self):
    return self.calculate_servers_stats(lambda s: s.number_of_requests_per_type)

  def number_of_failed_requests_per_type(self):
    return self.calculate_servers_stats(lambda s: s.total_failed_requests)

  def total_wait_time(self):
    return self.calculate_servers_stats(lambda s: s.total_wait_time)

  def total_wait_requests(self):
    return self.calculate_servers_stats(lambda s: s.total_wait_requests)

  def total_service_time(self):
    return self.calculate_servers_stats(lambda s: s.total_service_time)
