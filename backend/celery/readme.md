# Celery

Basic examples for learning Celery, an asynchronous task queue for Python.

## What is Celery?

Celery is a distributed task queue that helps you:
- Run tasks asynchronously
- Schedule periodic tasks
- Process background jobs
- Distribute work across threads or machines
- Handle retries and failures gracefully

## Components of a task queue
1. **Message broker**: Redis or RabbitMQ (stores task queue)
2. **Worker**: Celery workers process tasks from the queue
3. **Result backend** (optional): Stores task results (Redis, PostgreSQL, etc.)
4. **Publisher**: Produces celery task
5. **Consumer**: Celery worker

## Quick Start

```bash
# Install
pip install celery

# With Redis
pip install "celery[redis]"

# With RabbitMQ
pip install "celery[rabbitmq]"

# Run celery worker
celery -A tasks worker --loglevel=info --concurrency=10


-- Testing --
# Cd to celery directory
cd backend/celery

# Start workers (python file)
python start_worker.py

# Start workers (shell script)
chmod +x start_worker.sh
./start_worker.sh

# Run tasks
python run_tasks.py
```

## Best Practices

- Use task timeouts to prevent hung tasks
- Implement proper error handling and retries
- Use task routing for different task types

## Resources

- [Celery Documentation](https://docs.celeryproject.org/)