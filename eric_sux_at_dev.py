from zatt.client.mtdd import MTDD

def main():
    mtdd = MTDD('localhost', 5257)
    
    mini_txn_1 = {
        'compare_set': {},
        'write_set': {'buster_numbah_one': 'ericlee123'},
        'read_set': []
    }
    response = mtdd.send_mt(mini_txn_1['compare_set'], mini_txn_1['write_set'], mini_txn_1['read_set'])
    # Response I saw:
    # {'reads': {}, 'type': 'result', 'success': True}
    print('mini_txn_1 response:')
    print(response)

    mini_txn_2 = {
        'compare_set': {},
        'write_set': {'total_dingus': 'ericlee123'},
        'read_set': ['buster_numbah_one']
    }
    response = mtdd.send_mt(mini_txn_2['compare_set'], mini_txn_2['write_set'], mini_txn_2['read_set'])
    # Response I saw:
    # {'reads': {}, 'type': 'result', 'success': True}
    print('mini_txn_2 response:')
    print(response) 

if __name__ == '__main__':
    main()
