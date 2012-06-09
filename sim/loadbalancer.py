from server import Server

class LoadBalancer:

  def __init__(self,servers,method="roundrobin"):
    self.servers = servers
    self.method = method

  def number_of_servers(self):
    return len(self.servers)

  def server(self,index):
    return self.servers[index]

  def process(self,request_type,arrival_time,service_time):
    self.elect_server(arrival_time).process(request_type,arrival_time,service_time)

  def elect_server(self,arrival_time):
    if self.method == "roundrobin":
       return self.elect_server_by_roundrobin()
    if self.method == "busyness":
       return self.elect_server_by_busyness(arrival_time)
    raise Exception("unknown balancer method '%s'" % self.method)
    
  def elect_server_with_min(self,func):
    server,min = self.servers[0],func(self.servers[0])
    for z in self.servers:
      current = func(z)
      if current < min:
        min = current
        server = z
    return server

  def elect_server_by_roundrobin(self):
    return self.elect_server_with_min(lambda s: s.total_requests())

  def elect_server_by_busyness(self,arrival_time):
    return self.elect_server_with_min(lambda s: s.number_of_pending_requests(arrival_time))

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
    return self.calculate_servers_stats(lambda s: s.stats["number_of_requests_per_type"])

  def number_of_failed_requests_per_type(self):
    return self.calculate_servers_stats(lambda s: s.stats["total_failed_requests"])

  def total_wait_time(self):
    return self.calculate_servers_stats(lambda s: s.stats["total_wait_time"])

  def total_wait_requests(self):
    return self.calculate_servers_stats(lambda s: s.stats["total_wait_requests"])

  def total_service_time(self):
    return self.calculate_servers_stats(lambda s: s.stats["total_service_time"])
