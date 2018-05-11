import time
import threading

from zatt.client import mtdd

# multiple versions of this will be spun up in different threads. Ideally this
# would be tested with multiple processes.
def client(id, port):
	mini_txn = {
		'compare': {'a': 1},
		'write': {'a': 1},
		'read': ['a']
	}
	# connect
	d = mtdd.MTDD('localhost', port)
	# determine beginning time
	start_time = time.time()
	# run mini transactions
	for i in range(10):
		d.send_mt(mini_txn['compare'], mini_txn['write'], mini_txn['read'])
	# determine ending time
	end_time = time.time()
	# print time elapsed for this client
	print('client #{} ran for {}'.format(id, end_time - start_time))

def stress_test():
	d = mtdd.MTDD('localhost', 5254)
	# initialize the key-value store
	d.send_mt({}, {'a': 1, 'b': 2}, [])

	# create the threads
	client_threads = list()
	client_threads.append(threading.Thread(name='client0', target=client, args=(0, 5254)))
	client_threads.append(threading.Thread(name='client1', target=client, args=(1, 5255)))
	client_threads.append(threading.Thread(name='client2', target=client, args=(2, 5256)))
	client_threads.append(threading.Thread(name='client3', target=client, args=(3, 5257)))
	client_threads.append(threading.Thread(name='client4', target=client, args=(4, 5258)))
	# start the threads
	for client_thread in client_threads:
		client_thread.start()
	# wait for the threads to finish
	for client_thread in client_threads:
		client_thread.join()

if __name__ == '__main__':
	# this test assumes using ports 5254, 5255, 5256, 5257, and 5258 for the
	# nodes in the cluster
	stress_test()