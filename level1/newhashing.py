#!/usr/bin/python
import hashlib
import sys
import subprocess
import time

USER = "user-jpgjctdq"
TREE = subprocess.check_output(['git', 'write-tree']).strip()
PARENT = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip()
TIMESTAMP = int(time.time())
DIFFICULTY = '000001'
DEBUG = False

BASE_STRING = """tree {tree}
parent {parent}
author prakhar <prakhar@stripe.com> {timestamp} +0000
committer prakhar <prakhar@stripe.com> {timestamp} +0000

nonce:""".format(tree=TREE, parent=PARENT, timestamp=TIMESTAMP)

def getHash(content):
	header = "commit %s\0" % len(content)
	store = header + content
	return hashlib.sha1(store).hexdigest()

def prepare_index():
	with open('LEDGER.txt', 'w') as myfile:
		contents = myfile.read()
		myfile.write("{user}: 1".format(user=USER))
	subprocess.check_output(['git', 'add', 'LEDGER.txt'])

def reset():
	subprocess.call(['git', 'fetch'])
	subprocess.call(['git', 'reset', '--hard', 'origin/master'])

def solve():
	counter = 2
	sha = getHash(BASE_STRING + str(counter))

	# start looping
	while sha > DIFFICULTY:
		counter += 1
		sha = getHash(BASE_STRING + str(counter))

	# write the correct body to a file
	filename = 'final_commit_message'
	op = open(filename, 'w').write(BASE_STRING + str(counter))
	print sha

	# commit to git
	cmd_test = "git hash-object -t commit " + filename
	commit_sha = subprocess.check_output(cmd_test, shell=True).rstrip('\n')
	subprocess.call(['git', 'reset','--hard', commit_sha])

	# OH NO! 
	if sha != commit_sha:
		print "ERROR: SHA not matching"
		sys.exit(0)

	# print some stats
	print "Hashes run:", counter
	print "Mined a Gitcoin with sha:", sha

if __name__ == "__main__":
	# reset()
	# prepare_index()
	solve()

	done = subprocess.call(['git', 'push', 'origin', 'master'])
	if done == 1:
		print "GG! :("
	else:
		print "Success"	
