from tasks import basic_celery_task, task_with_late_acks, task_with_acks_and_retries, task_with_infinite_retries, task_with_finite_retries, task_with_different_status, task_with_time_limit
from celery.result import AsyncResult
import time

# NOTE: .delay() always return the task-id

# Task 1: Basic celery task


def run_basic_celery_task():
    basic_celery_task_results = []
    for i in range(0, 10):
        basic_celery_task_results.append(
            basic_celery_task.delay(
                x=i,
                y=i
            )
        )

    for result in basic_celery_task_results:
        print(result.get())


# Task 2: Celery task with acks
def run_task_with_late_acks():
    task_with_late_acks_results = []
    for i in range(0, 10):
        task_with_late_acks_results.append(
            task_with_late_acks.delay(
                x=i,
                y=i
            )
        )

    for result in task_with_late_acks_results:
        print(result.get())


# Task 3: Celery task with infinite retries
def run_task_with_infinite_retries():
    task_with_infinite_retries_results = []
    for i in range(0, 1):
        task_with_infinite_retries_results.append(
            task_with_infinite_retries.delay(
                x=i,
                y=i
            )
        )

    for result in task_with_infinite_retries_results:
        print(result.get())


# Task 4: Celery task with finite retries
def run_task_with_finite_retries():
    task_with_finite_retries_results = []

    try:
        for i in range(0, 1):
            result = task_with_finite_retries.delay(
                x=i,
                y=i
            )
            task_with_finite_retries_results.append(result)
            print(f"Task ID: {result.id}")

        for result in task_with_finite_retries_results:
            print(result.get())

    except Exception as e:
        print("Failed task: ", e)


# Task 5: Celery task with late acks and retries
def run_task_with_late_acks_and_retries():
    task_with_late_acks_and_retries_results = []
    for i in range(0, 10):
        task_with_late_acks_and_retries_results.append(
            task_with_acks_and_retries.delay(
                x=i,
                y=i
            )
        )

    for result in task_with_late_acks_and_retries_results:
        print(result.get())


# Task 6: Async result
def run_basic_async_result():
    results = []

    for i in range(0, 10):
        # result = basic_celery_task.delay(x=i, y=i)
        # results.append(result)

        result = basic_celery_task.apply_async(args=[i, i])
        results.append(result)

    # .get vs AsyncResult
    # .get -> blocks the main thread
    #         -> until the task is finished the thread is blocked which is waste of resources
    # AsyncResult -> non-blocking
    #         -> get the result of the task without blocking the thread

    time.sleep(5)

    for task_id in results:
        # get async result object
        obj = AsyncResult(task_id)

        if obj.ready():
            print(obj.result)
        else:
            print(f"Not finished yet: {obj.status}")
            # Status can be: "PENDING", "STARTED", "SUCCESS", "FAILURE", "RETRY", "REVOKED", "QUEUED"


# Task 7: Task with different status

def get_task_status(task_ids: list[str]):
    for task_id in task_ids:
        obj = AsyncResult(task_id)
        if obj.ready():
            print(
                f"Task {task_id} - Status: {obj.status} - Result: {obj.result}")
            # Since task is finished, removing it from the list
            task_ids.remove(task_id)
        else:
            status = obj.status
            if status == "PENDING":
                message = "Task is waiting for execution"
            elif status == "STARTED":
                message = "Task has been started by a worker"
            elif status == "RETRY":
                message = "Task is being retried"
            elif status == "REVOKED":
                message = "Task has been revoked"
            elif status == "QUEUED":
                message = "Task is in queue"
            else:
                message = "Task is in progress"

            print(f"Task {task_id} - Status: {status} - {message}")


def run_task_with_different_status():
    tasks_with_different_status = []
    for i in range(0, 20):
        tasks_with_different_status.append(
            task_with_different_status.delay(x=i, y=i)
        )

    time.sleep(2)

    while len(tasks_with_different_status) > 0:
        print("\n\n---\n")
        get_task_status(tasks_with_different_status)


# Task 8: Task with time limit
def run_task_with_time_limit():
    task_with_time_limit_results = []
    for i in range(0, 10):
        task_with_time_limit_results.append(
            task_with_time_limit.delay(x=i, y=i)
        )
    
    while len(task_with_time_limit_results) > 0:
        print("\n\n---\n")
        get_task_status(task_with_time_limit_results)
        
if __name__ == "__main__":
    # run_basic_celery_task()
    # run_task_with_late_acks()
    # run_task_with_infinite_retries()
    # run_task_with_finite_retries()
    # run_task_with_late_acks_and_retries()
    # run_basic_async_result()
    # run_task_with_different_status()
    run_task_with_time_limit()
