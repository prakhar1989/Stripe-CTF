#!/usr/bin/python
import hashlib
import sys
import subprocess
import time

BODY = """tree {tree}
parent {parent}
author prakhar <prakhar@stripe.com> {timestamp} +0000
committer prakhar <prakhar@stripe.com> {timestamp} +0000

nonce:{counter}
"""

USER = "user-jpgjctdq"
TREE = subprocess.check_output(['git', 'write-tree']).strip()
PARENT = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip()
TIMESTAMP = int(time.time())
DIFFICULTY = '000001'
DEBUG = False

def getHash(content, object_type="commit"):
	header = "%s %s\0" % (object_type, len(content))
	store = header + content
	return hashlib.sha1(store).hexdigest()

def gen_string(counter, tree=TREE, parent=PARENT):
	return BODY.format(tree=tree, parent=parent, 
		timestamp=TIMESTAMP, counter=counter)

def prepare_index():
	with open('LEDGER.txt', 'a') as myfile:
		myfile.write("{user}: 1".format(user=USER))
	subprocess.check_output(['git', 'add', 'LEDGER.txt'])

def reset():
	subprocess.call(['git', 'fetch'])
	subprocess.call(['git', 'reset', '--hard', 'origin/master'])

def solve():
	counter = 2
	body_string = gen_string(counter)
	sha = getHash(body_string)

	# start looping
	while sha > DIFFICULTY:
		counter += 1
		# if DEBUG and counter % 100000 == 0: print "%d hashes..." % counter
		body_string = gen_string(counter)
		sha = getHash(body_string)

	# write the correct body to a file
	filename = 'final_commit_message'
	op = open(filename, 'w').write(body_string)

	print sha

	# commit to git
	commit_sha = subprocess.check_output(['git', 'hash-object', '-t', 
					'commit', '-w', filename]).strip()
	subprocess.call(['git', 'reset','--hard', commit_sha])

	# OH NO! 
	if sha != commit_sha:
		print "ERROR: SHA not matching"
		sys.exit(0)

	# print some stats
	print "Hashes run:", counter
	print "Mined a Gitcoin with sha:", sha

if __name__ == "__main__":
	reset()
	prepare_index()
	solve()
	done = subprocess.call(['git', 'push', 'origin', 'master'])
	if done == 1:
		print "GG! :("
	else:
		print "Success"	
