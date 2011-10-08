from multiprocessing import Manager

last_updated_times = None
manager = None

def init_times():
	global manager
	global last_updated_times
	manager = Manager()
	last_updated_times = manager.dict()

def update_time(key, time):
	global manager
	global last_updated_times
	last_updated_times[key] = time

def get_time(key):
	global manager
	global last_updated_times
	if key not in last_updated_times:
		last_updated_times[key] = 0
	return last_updated_times[key]