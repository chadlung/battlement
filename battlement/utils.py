from datetime import datetime, timedelta
import uuid


def new_uuid():
    return str(uuid.uuid4())


def recheck_time(seconds=5):
    return datetime.utcnow() + timedelta(seconds=seconds)
