import scipy.stats
from collections import deque

class RequestGenerator:
  def __init__(self,
    types_of_requests,
    arrival_rate):

    request_type_distribution=[float(x["proportion"]) for x in types_of_requests.values()]
    request_type_mean=[float(x["avg_service_time_secs"]) for x in types_of_requests.values()]
    request_type_std_deviation=[float(x["deviation_service_time_secs"]) for x in types_of_requests.values()]

    self.number_request_types = len(types_of_requests)
    self.arrival_time = 0

    self.discrete_dist = scipy.stats.rv_discrete(name="discrete",
      values=(range(self.number_request_types),request_type_distribution))
    #print "expon scale = %f" % (1.0/arrival_rate)
    self.exponential_dist = scipy.stats.expon(scale=1.0/arrival_rate)
    self.norm_dists = [scipy.stats.norm(loc=request_type_mean[z],scale=request_type_std_deviation[z]) for z
      in range(self.number_request_types)]

    self.cache_service_time = {}
    for z in range(self.number_request_types):
      self.cache_service_time[z] = deque()

  def generate(self,number_of_requests):
    request_type_arr = self.discrete_dist.rvs(size=number_of_requests)
    time_from_prev_arr = self.exponential_dist.rvs(size=number_of_requests)
    service_time_arr = self.generate_service_time(request_type_arr)
    return zip(request_type_arr,time_from_prev_arr,service_time_arr)

  def generate_service_time(self,request_type_arr):
    return [self.guess_service_time(z) for z in request_type_arr]
       
  def guess_service_time(self,request_type):
    if not self.cache_service_time[request_type]:
      self.cache_service_time[request_type].extend(
       [z for z in self.norm_dists[request_type].rvs(size=100) if z > 0.0])

    return self.cache_service_time[request_type].popleft()

if __name__ == "__main__":
  generator = RequestGenerator([0.05,0.95],[2.5,0.75],30)
  print generator.generate(10)
