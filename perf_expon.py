import scipy.stats
from sys import argv,exit,stderr

expon = scipy.stats.expon(scale=0.5)

if len(argv) > 1:
  cache_size = int(argv[1])
else:
  cache_size = 1

for i in range(50000/cache_size):
  expon.rvs(size=cache_size)
