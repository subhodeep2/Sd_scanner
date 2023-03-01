#!/usr/bin/python3

from argparse import ArgumentParser,FileType
from threading import Thread
from requests import get,exceptions
from time import time

subdomains = []

def prepare_args():
	"""Prepare Arguments

		return:
			args(argparse.Namespace)
	"""
	parser = ArgumentParser(description="Sub domain Finder",usage="%(prog)s google.com",epilog="Example: %(prog)s -w /usr/share/worldlist.txt -t 500 -V google.com")
	parser.add_argument(metavar="Domain",dest="domain",help="Domain Name")
	parser.add_argument("-w","--worldlist",dest="worldlist",metavar="\b",type=FileType("r"),help="worldlist of sub domains",default="worldlist.txt")
	parser.add_argument("-t","--threads",dest="threads",metavar="\b",type=int,help="Threads to use",default=600)
	parser.add_argument("-V","--verbose",action="store_true",help="vrebose output")
	parser.add_argument("-v","--version",action="version",help="display version",version="%(prog)s 1.0")
	args = parser.parse_args()
	return args

def prepare_words():
	"""generator function for words
	"""
	words = arguments.wordlist.read().split()
	for word in words:
		yield word

def check_subdomain():
	"""check subdomain
	"""

	while True:
		try:
			word=next(words)
			url = f"https://{word}.{arguments.domain}"
			request = get(url,timeout=5)
			if request.status_code == 200:
				subdomains.append(url)
				if arguments.verbose:
					print(url)
		except (exceptions.ConnectionError,exceptions.ReadTimeout()):
			continue
		except StopIteration:
			break

def prepare_threads():
	"""creat join start threads
	"""
	threads_list = []
	for _ in range(arguments.threads):
		threads_list.append(Thread(target=check_subdomain))

	for thread in threads_list:
		thread.start()

	for thread in threads_list:
		thread.join()

if __name__ == "__main__":
	arguments = prepare_args()
	words = prepare_words()
	start_time = time()
	prepare_threads()
	end_time = time()
	print("Sub Domain Found: \n"+"\n".join(i for i in subdomains))
	print(f"Time Taken: {round(end_time - start_time,2)}")