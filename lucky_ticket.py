import threading
from queue import Queue


def process_worker(data_chunk, results_queue, semaphore):
    with semaphore:
        result = process_data(data_chunk)
        results_queue.put(result)


def process_data(data_chunk):
    data_chunk = str(data_chunk).zfill(6)

    first_numb, second_numb, third_numb, fourth_numb, fifth_numb, sixth_numb = map(int, data_chunk)

    return first_numb + second_numb + third_numb == fourth_numb + fifth_numb + sixth_numb


if __name__ == "__main__":
    data = int(input("Enter number: "))
    results_queue = Queue()
    semaphore = threading.Semaphore(4)

    chunk_size = max(len(str(data)) // 4, 6)
    data_chunks = [int(str(data)[i:i + chunk_size]) for i in range(0, len(str(data)), chunk_size)]

    threads = []
    for chunk in data_chunks:
        thread = threading.Thread(target=process_worker, args=(chunk, results_queue, semaphore))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    results = [results_queue.get() for _ in range(len(data_chunks))]
    print(results[1])
