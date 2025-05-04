from celery import Celery, Task
import time
import random
from celery.exceptions import SoftTimeLimitExceeded


app = Celery(
    'celery_app',
)

app.config_from_object('celeryconfig')

@app.task(
    queue='basic_task_queue' # default queue name would be celery
)
def basic_celery_task(x:int,y:int) -> int:
    # simulate a long running task
    
    # Issue: If worker dies, the task will be lost.
    # Cause the task is acknowledged as soon as it is received.
    
    time.sleep(10)
    return x+y


@app.task(
    queue='basic_task_queue',
    acks_late=True, # delay the acknowledgement until the task is finished, fixes the task loss issue
)
def task_with_late_acks(x:int,y:int) -> int:
    # simulate a long running task
    # acks_late -> requeues message if worker dies
    
    time.sleep(30)
    return x+y


@app.task(
    queue='basic_task_queue',
    bind=True,
)
def task_with_infinite_retries(self:Task, x:int, y:int) -> int:
    # This task will always fail
    
    # Once task fails, it will be acknowledged hence it will be removed from the queue
    # But, the task will be requeued by the worker as a new message in the queue
    # The new message will have the same metadata as original but the retry count will be incremented
    
    #Sample self.request body i.e. message body
    # {
    #     'id': '123e4567-e89b-12d3-a456-426614174000',
    #     'task': 'tasks.task_with_infinite_retries',
    #     'args': [],
    #     'kwargs': {'x': 1, 'y': 2},
    #     'retries': 0 / 1 / 2 / 3 ... so on
    # }
    
    try:
        # simulate a long running task
        time.sleep(10)
        raise Exception("This task will always fail")
    
    except Exception as e:
        self.retry(exc=e)
        

@app.task(
    queue='basic_task_queue',
    bind=True,
    max_retries=3, # limit the number of retries
    default_retry_delay=5, # delay the retry in 5 seconds
)
def task_with_finite_retries(self:Task, x:int,y:int) -> int:
    # This task will always fail
    # The task will be retried 3 times with a delay of 5 seconds between each retry

    try:
        # simulate a long running task, before failing
        time.sleep(10)
        print(f"Task {self.request.id} failed")
        print(f"Retrying task {self.request}")
        
        raise Exception("This task will always fail")
    
    except Exception as e:
        self.retry(exc=e)
        

@app.task(
    bind=True,
    queue='basic_task_queue',
    acks_late=True,
    max_retries=3, # limit the number of retries
    default_retry_delay=5, # delay the retry in 5 seconds
)
def task_with_acks_and_retries(self:Task, x:int,y:int) -> int:
    # Ideal
    # acks_late -> requeues message if worker dies
    # retries -> fixed number of retries for each message, prevents resource exhaustion
    
    try:
        # simulate a long running task, before failing
        tt = random.randint(3,10)
        time.sleep(tt)
        
        if tt % 2 == 0:
            raise Exception("This task will always fail")
        
        return x+y
    
    except Exception as e:
        self.retry(exc=e)


@app.task(
    bind=True,
    queue='basic_task_queue',
    acks_late=True,
    max_retries=2, # limit the number of retries
    default_retry_delay=5, # delay the retry in 5 seconds
)
def task_with_different_status(self:Task, x:int,y:int) -> int:
    # Ideal
    # acks_late -> requeues message if worker dies
    # retries -> fixed number of retries for each message, prevents resource exhaustion
    
    try:
        # simulate a long running task, before failing
        time.sleep(5)
        
        if x % 2 == 0:
            raise Exception("This task will always fail")
        
        return x
    
    except Exception as e:
        self.retry(exc=e)
    
    else:
        return x+y
    
    
@app.task(
    queue='basic_task_queue',
    soft_time_limit=10, # time limit for the task to finish
    time_limit=20, # if exceeded, the task will be killed
)
def task_with_time_limit(x:int,y:int) -> int:
    
    # Soft time limit:
    # If the task exceeds the soft time limit, it will raise a SoftTimeLimitExceeded exception
    # The task will be able to respond back with a message
    
    # Time limit:
    # If the task exceeds the time limit, it will be killed
    # The task will be completely killed and will not be able to respond back
    # Issue: Infinite retries -> If the task is killed, the message will be requeued because it didn't send the acknowledgement
    # The issue can occur only with acks_late=True
    
    t = random.choices([2, 7, 10, 15, 20, 25])[0]
    
    try:
        # simulate a long running task
        print(f"Task {x} will run for {t} seconds")
        time.sleep(t)
        return x+y
    
    except SoftTimeLimitExceeded:
        # Ensure to stop the task here, else it will continue to run and will be killed by the time limit
        
        raise SoftTimeLimitExceeded("Task exceeded soft time limit.")