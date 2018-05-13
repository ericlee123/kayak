from multiprocessing import Process
from zatt.client import mtdd
import time

# spawns 5 client threads with the pre-specified ports which will run the
# minitransaction that is passed in for the number of times specified by the
# argument num_iterations
def init_client_processes(mini_txn, num_iterations):
	# create the threads
	client_processes = list()
	client_processes.append(Process(name='client0', target=client, args=(0, 5254, mini_txn, num_iterations)))
	client_processes.append(Process(name='client1', target=client, args=(1, 5255, mini_txn, num_iterations)))
	client_processes.append(Process(name='client2', target=client, args=(2, 5256, mini_txn, num_iterations)))
	client_processes.append(Process(name='client3', target=client, args=(3, 5257, mini_txn, num_iterations)))
	client_processes.append(Process(name='client4', target=client, args=(4, 5258, mini_txn, num_iterations)))
	return client_processes

def client(client_id, port, mini_txn, num_iterations):
	# make sure that the dict isn't missing any of the 3 fields
	if 'compare' not in mini_txn:
		mini_txn['compare'] = {}
	if 'write' not in mini_txn:
		mini_txn['write'] = {}
	if 'read' not in mini_txn:
		mini_txn['read'] = []
	# connect
	d = mtdd.MTDD('localhost', port)
	# determine beginning time
	start_time = time.time()
	# run mini transactions
	for i in range(num_iterations):
		d.send_mt(mini_txn['compare'], mini_txn['write'], mini_txn['read'])
	# determine ending time
	end_time = time.time()
	# print time elapsed for this client
	print('client #{} ran for {}'.format(client_id, end_time - start_time))
