import unittest
import time
import scipy.stats

class TestGenerateRandomValues(unittest.TestCase):

  def generate_expon_rvs(self,size):
    expon = scipy.stats.expon(scale=0.5)
    start = time.time()
    for i in range(50000/size):
      expon.rvs(size)
    return (time.time() - start)
     
  def test_generate_multivalues_will_be_faster(self):
    self.assertTrue(self.generate_expon_rvs(1)>80*self.generate_expon_rvs(100))

if __name__ == '__main__':
    unittest.main()

