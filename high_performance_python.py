# 고성능 파이썬
# 1. 고성능을 위한 파이썬 이해하기
"""
1) 파이썬에서는 전역 인터프리터 락(GIL: Global Interpreter Lock) 때문에 여러 개의 코어를 활용하기 쉽지 않음
 GIL은 현재 사용 중인 코어의 개수와 상관 없이 한 번에 하나의 명령만 실행되도록 강제함
2) 파이썬의 추상화는 다음 계산에 사용될 데이터를 L1/L2 캐시에 유지해야 하는 최적화에 방해가 된다.
 - 파이썬 객체가 메모리에 최적화된 형태로 저장되지 않는다. 파이썬은 메모리를 자동으로 할당/해제하는
   Garbage Collector하는데, 이는 CPU 캐시에 데이터를 전송하는 데 영향을 미치는 메모리 단편화를 초래함
 - 파이썬은 동적 타입을 사용하며 컴파일되지 않는다. -> Cython으로 극복 가능하다.
 - GIL
"""

# 2. 프로파일링으로 병목 지점 찾기
# 2.4. 시간을 측정하는 간단한 방법
# 시간 측정 자동화 데커레이터
from functools import wraps
from time import perf_counter

def timefn(fn):
    @wraps(fn)
    def measure_time(*args, **kwargs):
        start = perf_counter()
        result = fn(*args, **kwargs)
        end = perf_counter()
        print("elapsed time of {}: {}".format(fn.__name__, end-start))
        return result

    return measure_time()

@timefn
def calculate_loop(n=1000):
    cnt = 0
    for i in range(n):
        cnt += 0.01
    return cnt























