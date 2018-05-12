from zatt.client import mtdd

if __name__ == "__main__":
	dd = mtdd.MTDD('localhost', 5254)
	print(dd.send_mt({}, {'a': 0, 'b': 1}, []))
	print(dd.send_mt({'a': 0}, {'a': 0}, ['a']))
	print(dd.send_mt({}, {'a': 0, 'b': 1}, []))
