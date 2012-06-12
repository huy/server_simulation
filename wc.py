import glob
import os

total=0
for name in glob.glob('./**/*'):
  if os.path.splitext(name)[1] in [".py",".textile",".yaml"]:
    with open(name) as f:
      nlines = sum([1 for line in f])
    total = total + nlines
    print name,nlines

print "toltal number if lines=",total
