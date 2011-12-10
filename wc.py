import os

total=0
for top, dirs, files in os.walk('./'):
  for name in files:       
    if os.path.splitext(name)[1]==".py":
      fullpath=os.path.join(top, name)
      with open(fullpath) as f:
        fl = sum([1 for line in f])
      total = total + fl
      print fullpath,fl

print "toltal number if lines=",total
