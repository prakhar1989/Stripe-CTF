#!/usr/bin/python
import sys

path = sys.argv[2] if len(sys.argv) > 1 else "/usr/share/dict/words"
entries = set(open(path, 'r').read().split('\n'))

lines = sys.stdin.read().split('\n')
for line in lines:
	for word in line.split():
		if str.lower(word) in entries:
			print word,
		else:
			print "<%s>" % word,
	print 
