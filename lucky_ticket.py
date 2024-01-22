import threading
from queue import Queue


def process_worker(ticket_range, results_queue, semaphore):
    for ticket in ticket_range:
        with semaphore:
            result = process_ticket(ticket)
            results_queue.put(result)


def process_ticket(ticket):
    ticket_str = str(ticket).zfill(6)
    first_numb, second_numb, third_numb, fourth_numb, fifth_numb, sixth_numb = map(int, ticket_str)
    return first_numb + second_numb + third_numb == fourth_numb + fifth_numb + sixth_numb


if __name__ == "__main__":
    data = [format(i, '06d') for i in range(1000000)]
    results_queue = Queue()
    semaphore = threading.Semaphore(4)

    num_threads = 4
    chunk_size = len(data) // num_threads

    threads = []
    for i in range(num_threads):
        start_index = i * chunk_size
        end_index = (i + 1) * chunk_size if i < num_threads - 1 else len(data)
        thread_data = data[start_index:end_index]

        thread = threading.Thread(target=process_worker, args=(thread_data, results_queue, semaphore))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    results = [results_queue.get() for _ in range(len(data))]

    print(f"Number of Lucky tickets: {results.count(True)}")
