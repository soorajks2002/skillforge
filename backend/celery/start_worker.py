from tasks import app


def start_basic_task_queue_worker():
    worker = app.Worker(
        queues=['basic_task_queue'],
        loglevel='info',
        concurrency=2,  # number of worker threads
    )

    # Equivalent to:
    # celery -A tasks worker --queues=basic_task_queue --loglevel=info --concurrency=1

    worker.start()


def start_high_priority_task_queue_worker():
    worker = app.Worker(
        queues=['high_priority_task_queue'],
        loglevel='info',
        autoscale='10,3', # Max 10 workers, Min 3 workers
    )

    # Equivalent to:
    # celery -A tasks worker --queues=high_priority_task_queue --loglevel=info --concurrency=10

    worker.start()


if __name__ == "__main__":
    start_basic_task_queue_worker()
    # start_high_priority_task_queue_worker()
