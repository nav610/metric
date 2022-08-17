from metric import Metric #, DatabaseFactory
import time

@Metric
def context_manager(): 
	time.sleep(5)

if __name__ == "__main__": 
	context_manager()
