import time


def retry_until(assertion, timeout=10):

    end_time = time.time() + timeout

    last_error = None

    while time.time() < end_time:

        try:
            assertion()
            return

        except AssertionError as e:
            last_error = e
            time.sleep(1)

    raise last_error