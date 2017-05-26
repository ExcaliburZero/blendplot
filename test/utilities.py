import io
import sys

def capture_stderr(func):
    err, sys.stderr = sys.stderr, io.StringIO()
    value = None
    try:
        ret = func(None)
        sys.stderr.seek(0)
        value = (ret, sys.stderr.read())
    finally:
        sys.stderr = err

    return value
