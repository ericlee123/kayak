from stress_combination_fat import stress_test

def run():
	for i in range(10, 70):
		time_elapsed = stress_test(set_size=i, should_print=False, should_spin_down=False)
		print('set size {} \t - {} seconds'.format(i, time_elapsed))

if __name__ == "__main__":
	print('####################################################################')
	print(' Fat Mini-transaction Stress Test')
	print('	\t - variable set size')
	print(' \t - constant num iterations')
	print('----------------------------------')
	run()
	print('####################################################################')