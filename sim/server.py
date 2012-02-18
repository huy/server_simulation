class Server:
  def __init__(self, output_capacities):
    self.channels = []
    for n in output_capacities:
      self.channels.append([0 for z in range(n)])
    self.number_of_requests_per_type = [0 for z in range(len(output_capacities))]
    self.total_service_time = [0 for z in range(len(output_capacities))]
    self.total_wait_time = [0 for z in range(len(output_capacities))]
    self.total_wait_requests = [0 for z in range(len(output_capacities))]
    self.total_failed_requests = [0 for z in range(len(output_capacities))]

  def output_capacities(self):
    return [len(x) for x in self.channels]    

  def process(self,request_type,arrival_time,service_time):

    self.number_of_requests_per_type[request_type] += 1
    self.total_service_time[request_type] += service_time

    if len(self.channels[request_type]) == 0:
      self.total_failed_requests[request_type] += 1
    else:
      available_channel, available_from = self.find_first_available_channel(request_type)
      if arrival_time >= available_from:
        self.assign_request_to_channel(request_type,available_channel,arrival_time,service_time)
      else:
        #print "--- %s wait for %f" % (request_type,(available_from - arrival_time))
        self.total_wait_time[request_type] += (available_from - arrival_time)
        self.total_wait_requests[request_type] +=1
        self.assign_request_to_channel(request_type,available_channel,available_from,service_time)

  def find_first_available_channel(self,request_type):
    first_available_at = min(self.channels[request_type])
    return self.channels[request_type].index(first_available_at),first_available_at

  def assign_request_to_channel(self,request_type,channel,assign_at,service_time):
    #print "--- assign %d to %d at %f" % (request_type,channel,assign_at)
    self.channels[request_type][channel] = assign_at + service_time

  def number_of_pending_requests(self,at):
    return sum([len([r for r in ch if r > at]) for ch in self.channels])

  def total_requests(self):
    return sum(self.number_of_requests_per_type)
