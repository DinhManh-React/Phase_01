import time
import random


def retry_call(func, max_retries=5, base_delay=1, backoff=2):
    for attempt in range(max_retries):
        try:
            return func()

        except Exception as e:
            print(f"Lỗi: {e} | attempt {attempt+1}")

            # hết retry
            if attempt == max_retries - 1:
                raise

            # tính delay
            delay = base_delay * (backoff ** attempt)

            # thêm jitter nhỏ (optional) để tránh nhiều request retry cùng lúc
            delay += random.uniform(0, 0.3)

            time.sleep(delay)
def call_api(url):
    r = random.random()
    if r < 0.5:
        raise TimeoutError("Timeout")
    return {"status": 200, "data": "OK"}

result = retry_call(
    lambda: call_api("https://chiaki.vn/thuc-pham-chuc-nang"),
    max_retries=5,
    base_delay=1,
    backoff=2
)

print(result)