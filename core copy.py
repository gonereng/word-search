import concurrent.futures
from multiprocessing import Process
import time

start = time.perf_counter()

def do_something(seconds):
    print(f"Sleeping for {seconds} second(s)")
    time.sleep(seconds)
    return "Done sleeping"

if __name__ == "__main__":

    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = [executor.submit(do_something, 1) for _ in range(10)]

        for f in concurrent.futures.as_completed(results):
            print(f.result())
        # processes = []

        # for _ in range(10):

        #     p = Process(target=do_something, args=[1.5])
        #     p.start()
        #     processes.append(p)

        # for process in processes:
        #     process.join()

    end = time.perf_counter()

    print(f"Finished in {round(end-start, 2)} second(s)")