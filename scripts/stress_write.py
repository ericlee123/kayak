import time
from multiprocessing import Process

from zatt.client import mtdd
from test_util import init_client_processes

def stress_test():
	d = mtdd.MTDD('localhost', 5254)
	# initialize the key-value store
	d.send_mt({}, {'a': 1}, [])

	mini_txn = {
		'compare': {},
		'write': {'a': 1},
		'read': []
	}
	num_iterations = 100
	client_processes = init_client_processes(mini_txn, 100)

	start_time = time.time()
	# start the threads
	for client_process in client_processes:
		client_process.start()
	# wait for the threads to finish
	for client_process in client_processes:
		client_process.join()
	end_time = time.time()
	print('whole thing took {}'.format(end_time - start_time))

if __name__ == '__main__':
	print('####################################################################')
	print(' WRITE STRESS TEST')
	print('-------------------')
	# this test assumes using ports 5254, 5255, 5256, 5257, and 5258 for the
	# nodes in the cluster
	stress_test()
	print('####################################################################')
