import time
from multiprocessing import Process

from zatt.client import mtdd
from test_util import spin_up, spin_down, init_client_processes

def stress_test(set_size=50, num_iterations=50, should_print=True, should_spin_down=True):
	spin_up()

	d = mtdd.MTDD('localhost', 5254)

	# create the write, compare, and read sets for this stress test
	write_compare_set = {}
	read_set = []
	for i in range(set_size):
		write_compare_set[i] = i
		read_set.append(i)

	# initialize the key-value store
	d.send_mt({}, write_compare_set, [])

	mini_txn = {
		'compare': write_compare_set,
		'write': write_compare_set,
		'read': read_set
	}

	client_processes = init_client_processes(mini_txn, num_iterations)

	start_time = time.time()
	# start the threads
	for client_process in client_processes:
		client_process.start()
	# wait for the threads to finish
	for client_process in client_processes:
		client_process.join()
	end_time = time.time()

	if should_print:
		print('whole thing took {} seconds'.format(end_time - start_time))

	if should_spin_down:
		spin_down()

	return end_time - start_time

if __name__ == '__main__':
	print('####################################################################')
	print(' FAT MINI-TRANSACTION COMBINATION STRESS TEST')
	print('----------------------------------------------')
	# this test assumes using ports 5254, 5255, 5256, 5257, and 5258 for the
	# nodes in the cluster
	stress_test()
	print('####################################################################')
