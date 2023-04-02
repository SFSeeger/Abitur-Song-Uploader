# Django Helpers

## Commands
### `register_tasks`

The settings below runs clearsessions at 16 o'clock every day
```python
# settings.py
CRON_TASKS = {
    "clearsessions": {
        "args": "clearsessions",
        "schedule_type": "D",
        "run_at": "16:00"
    }
}
```