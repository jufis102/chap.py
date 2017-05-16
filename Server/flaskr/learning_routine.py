
from create_entropy import create_entropy
from create_probabilities import calculate_probability, drop_probability

import time


def learning_routine():
	start_time=time.clock()
	calculate_probability()
	create_entropy()
	end_time=time.clock()
	a_time=end_time-start_time
	print(a_time)
	time.sleep(300)
	learning_routine()
	
if __name__ == "__main__":
	learning_routine()
