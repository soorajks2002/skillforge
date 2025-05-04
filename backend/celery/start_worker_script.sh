#!/bin/bash

# Step 1: Set environment variables
export CELERY_LOG_LEVEL="info"
export AUTO_SCALING_MAX_WORKERS="10"
export AUTO_SCALING_MIN_WORKERS="3"
export QUEUE_NAME="basic_task_queue"
export TASKS_FILE="tasks"

# Step 2: Start worker
celery -A $TASKS_FILE worker \
    --loglevel=$CELERY_LOG_LEVEL \
    --queues=$QUEUE_NAME \
    --autoscale=$AUTO_SCALING_MAX_WORKERS,$AUTO_SCALING_MIN_WORKERS