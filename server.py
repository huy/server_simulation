class Server:
  def __init__(self, capacity_per_request_type):
    self.total_requests = 0
    self.channels = []
    for n in capacity_per_request_type:
      self.channels.append([0 for z in range(n)])
    self.total_wait_time = [0 for z in range(len(capacity_per_request_type))]

  def process(self,request_type,arrival_time,service_time):
    self.total_requests += 1

    available_channel, available_from = self.find_first_available_channel(request_type)
    if arrival_time >= available_from:
      self.assign_request_to_channel(request_type,available_channel,arrival_time,service_time)
    else:
      #print "--- %s wait for %f" % (request_type,(available_from - arrival_time))
      self.total_wait_time[request_type] += (available_from - arrival_time)
      self.assign_request_to_channel(request_type,available_channel,available_from,service_time)

  def find_first_available_channel(self,request_type):
    first_available_at = min(self.channels[request_type])
    return self.channels[request_type].index(first_available_at),first_available_at

  def assign_request_to_channel(self,request_type,channel,assign_at,service_time):
    #print "--- assign %d to %d at %f" % (request_type,channel,assign_at)
    self.channels[request_type][channel] = assign_at + service_time


