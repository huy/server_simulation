import scipy.stats
from collections import deque

class RequestGenerator:
  def __init__(self,
    request_type_distribution,
    request_type_mean_time,
    arrival_rate):

    self.number_request_types = len(request_type_distribution)
    self.arrival_time = 0

    self.discrete_dist = scipy.stats.rv_discrete(name="discrete",
      values=(range(self.number_request_types),request_type_distribution))
    self.exponential_dist = scipy.stats.expon(scale=1.0/arrival_rate)
    self.norm_dists = [scipy.stats.norm(loc=request_type_mean_time[z],scale=request_type_mean_time[z]/2) for z
      in range(self.number_request_types)]

    self.cache_service_time = {}
    for z in range(self.number_request_types):
      self.cache_service_time[z] = deque()

  def generate(self,number_of_requests):
    request_type_arr = self.discrete_dist.rvs(size=number_of_requests)
    delay_arr = self.exponential_dist.rvs(size=number_of_requests)
    service_time_arr = self.generate_service_time(request_type_arr)
    return zip(request_type_arr,delay_arr,service_time_arr)

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
