from datetime import datetime, timedelta
import uuid


def new_uuid():
    return str(uuid.uuid4())


def recheck_time():
    return datetime.utcnow() + timedelta(seconds=10)
