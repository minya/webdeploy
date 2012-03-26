#!/usr/bin/python
import os
import shutil
import sys
from deploy import Deploy

src = sys.argv[1]
dst = sys.argv[2]
if os.path.exists(dst):
	shutil.rmtree(dst)
os.mkdir(dst)
d = Deploy(src, dst)
d.Deploy()
