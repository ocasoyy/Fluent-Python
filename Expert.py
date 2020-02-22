# Fluent Python
# 1장 파이썬 데이터 모델
# 1.1 파이썬 카드 한 벌

from collections import namedtuple

Card = namedtuple('Card', ['rank', 'suit'])

class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        # 이 _cards안에는 Card(rank, suit) 형식의 52개의 네임드 튜플이 들어 있음
        # 아래와 같이 하면 Combination 처럼 모든 쌍이 리스트 내에 내장됨
        self._cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]

# Tutorial
deck = FrenchDeck()
len(deck)
deck.__getitem__(0)
print(deck[0])

# 임의로 하나 추출
from random import choice
choice(deck)

"""
__getitem__ 특별 메서드는 self._cards의 []연산자에 작업을 위임하므로
deck 객체는 슬라이싱도 자동으로 지원한다.
"""
print(deck[12::13])

# deck 반복: __getitem__ 특별 메서드를 자동으로 구현한 것
for card in reversed(deck):
    print(card)

# 결론
# __len__()과 __getitem__() 특별 메서드를 구현함으로써
# FrenchDeck은 표준 파이썬 시퀀스처럼 작동하므로 반복/슬라이싱 등의 핵심 언어 기능과 표준 라이브러리 사용 가능


# 1.2 특별 메서드는 어떻게 사용되나?
# 특별 메서드를 호출해야 할 때는 len(), iter(), str() 등 관련된 내장 함수를 호출하는 것이 좋음
# 이들 내장함수가 특별 메서드를 호출할 것임
# Vector class 만들기
from math import hypot

class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self):
        # 객체를 문자열로 표현하기 위해 repr() 내장 메서드에 의해 호출됨
        # __repr__()를 구현하지 않으면 Vector 객체는 콘솔에
        # <Vector object at 0x~~~> 형태로 출력된다.
        # %r: repr의 결과
        return 'Vector(%r, %r)' % (self.x, self.y)

    # 만약 아래 메서드를 abs라고 구현했다면,
    # Vector_instance.abs()와 같이 메서드를 사용해야 할 것이다.
    def __abs__(self):
        return hypot(self.x, self.y)

    def __bool__(self):
        # 벡터의 크기가 0이면 False, 아니면 True
        return bool(abs(self))

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x, y)

    def __mul__(self, scalar):
        # 현재로서는 벡터에 숫자를 곱하는 형식으로만 사용이 가능함
        return Vector(self.x * scalar, self.y * scalar)


v1 = Vector(2, 4)
v2 = Vector(2, 1)

abs(v1)
bool(v1)
v1 + v2
v1 * 3

#----------
# 2장 시퀀스
# 컨테이너 시퀀스, 균일 시퀀스
# 2.3 튜플은 단순한 불변 리스트가 아니다.
# 2.3.2 튜플 언패킹
# 인수 앞에 *를 붙여 튜플을 언패킹할 수 있음
# 함수 매개변수에 *를 연결하면 초과된 인수를 가져올 수 있음
t = (20, 8)
divmod(*t)

# 초과 항목을 잡기 위해 * 사용하기
a, b, *rest = range(5)
print(rest)

# 2.3.4 네임드 튜플: 일반적인 객체보다 메모리를 적게 사용함
# import collections
# 아래와 같이 단순히 공백으로 구분해도 됨
City = namedtuple('City', 'name country population coordinates')
tokyo = City('Tokyo', 'JP', 36.933, (35.6, 139.7))
print(tokyo.country)
print(tokyo[3])

# 바이트 코드 보기
import dis

dis.dis('1+1')
temp = ['A', 'B']
dis.dis("temp += 'C'")

# 2.7 list.sort()와 sorted 내장 함수
# sort 메서드는 타깃 객체를 변경하고 새로운 리스트를 생성하지 않았음을 알려주기 위해 None을 반환한다.
fruits = ["grape", "rasberry", "apple", "banana"]
sorted(fruits, reverse=False, key=len)
sorted(fruits, reverse=False, key=str.lower)

# 2.8 정렬된 시퀀스를 bisect로 관리하기
import bisect
haystack = [1, 5, 10]
needles = [6, 7]

for needle in needles:
    position = bisect.bisect(haystack, needle)
    print(position)

# bisect: 시퀀스의 오름차순을 유지한 채로 들어갈 위치를 찾아냄
# insort: 시퀀스의 오름차순을 유지한 채로 item을 시퀀스에 삽입함
my_list = [1, 3, 5, 7]
target = 2
bisect.bisect(my_list, target)
bisect.insort(my_list, target)
print(my_list)


# 2.9 리스트가 답이 아닐 때
# 2.9.1 배열
# pop, insert, extend, frombytes, tofile 메서드 이용

# 2.9.4 덱
from collections import deque
dq = deque(range(10), maxlen=10)
dq.rotate(4)
print(dq)

dq.rotate(-3)
print(dq)

dq.appendleft(-1)
print(dq)

dq.extend([11, 22, 33])
print(dq)

dq.extendleft([90])
print(dq)

# 리스트에 구현된 메서드
# append, clear, __contains__, copy, count
# __delitem__(p): p 위치의 아이템 삭제
# extend(i): iterable 한 객체 i를 오른쪽에 추가함
# __getitem__(p): p 위치의 아이템 가져오기
# index(e): 처음 e가 나타난 위치를 반환함
# insert(p, e): p 위치의 항목 앞에 e 요소를 추가함
# __iter__(): 반복자를 반환함
# remove(e): e와 같은 값을 가진 첫 항목을 삭제함
# __setitem__(p, e): s[p] = e, p 위치에 e값을 저장하고 기존 값을 덮어 씀

# 덱에 구현된 메서드
# copy 대신 __copy__
# __contains__, index, insert, sort는 없음
# extendleft, popleft, rotate 등이 있음


#----------
# 3장 딕셔너리와 집합
# 3.1 일반적인 매핑형
# collections.abc 모듈은 dict 및 이와 유사한 자료형의 인터페이스를 정의하기 위해
# Mapping 및 MutableMapping 추상 베이스 클래스 (ABC)를 제공함
# 딕셔너리는 collections.abc.Mapping의 인스턴스임
import collections

ddict = {'A': 1}
isinstance(ddict, collections.abc.Mapping)

# 표준 라이브러리에서 사용하는 Mapping 형은 모두 dict를 이용하여 구현하므로
# 키가 해시가능해야 한다.
# 해시가능: 수명 주기 동안 변하지 않는 해시값을 갖고 있고, 다른 객체와 비교할 수 있음
# -- 위 정의에서 __hash__, __eq__ 메서드가 필요함

# 예를 들어 리스트는 해시가능하지 않다.
hash([1, 2])

# 3.3 공통적인 매핑 메서드
ddict = {'A': 1, 'B': 2}
print(ddict['C'])    # 당연히 KeyError가 뜸

# 임시 방편: get
# KeyError를 처리하지 않고, 값이 존재하지 않는 Key를 호출하였을 때 기본값을 부여하는 get 메서드
ddict = {'A': 1, 'B': 2}
result = {}
for key in ['A', 'B', 'C']:
    value = ddict.get(key, 0)
    result[key] = value

print(result)

# 해결책
# (1) setdefault
def count_letters(word):
    letters = list(word)
    ddict = {}
    for letter in letters:
        ddict.setdefault(letter, 0)
        ddict[letter] += 1

    return ddict

result1 = count_letters('AAABBC')
print(result1)

# (2) defaultdict
def count_letters(word):
    letters = list(word)
    ddict = collections.defaultddict(lambda: 0)
    for letter in letters:
        ddict[letter] += 1

    return ddict

result2 = count_letters('AAABBC')
print(result2)

# 위 함수는 사실 collections.Counter를 이용하면 쉽게 구현할 수 있다.

# (3): __missing__() 메서드
# 기본 클래스인 dict에는 정의되어 있지는 않지만, dict는 이 메서드를 알고 있음
# dict 클래스를 상속하고 __missing__ 메서드를 정의하면,
# dict.__getitem__() 표준 메서드가 키를 발견할 수 없을 때 KeyError를 발생시키지 않고
# __missing__ 메서드를 호출한다.
# __missing__ 메서드는 오직 __getitem__ 메서드를 사용할 때만 호출되기 때문이다.

# dict가 아닌 Userdict를 상속하는 것이 좋다.

class StrKeyddict(collections.Userddict):
    def __missing__(self, key):
        # key가 문자열이고 존재하지 않으면 KeyError
        if isinstance(key, str):
            raise KeyError(key)
        return self[str(key)]

    def __contains__(self, key):
        # Userddict는 dict를 상속하지 않고
        # 내부에 실제 항목을 담고 있는 data라는 dict 객체를 갖고 있다.
        # 저장된 키가 모두 str 형이므로 self.data에서 바로 조회할 수 있다.
        return str(key) in self.data

    def __setitem__(self, key, item):
        self.data[str(key)] = item


# 불변 매핑: 실수로 매핑을 변경하지 못하도록 보장하고 싶은 경우
# 원래 매핑(changeable)을 변경하면 mappingproxy에 반영되지만,
# mappingproxy(unchangeable)를 직접 변경할 수는 없다.
from types import MappingProxyType

changeable = {'A': 1}
unchangeable = MappingProxyType(changeable)

changeable['B'] = 2
print(changeable)

# TypeError 발생
unchangeable['B'] = 2

# 그러나 위에서 changeable['B'] = 2 할당을 통해
# 동적인 unchangeable 은 changeable 에 대한 변경을 바로 반영한다.
print(unchangeable)


# 집합: set, frozenset (set의 불변형 버전)
# (1) 집합은 고유함을 보장한다.
# 집합의 요소는 해시가능해야 한다.
# set은 해시 가능하지 않지만 frozenset은 해시 가능하다.

# (2) 집합은 중위 연산자를 이용하여 기본적인 집합 연산을 구현한다.
# | 합집합, & 교집합, - 차집합
needles = set(list('ab'))
haystack = set(list('abcde'))

# haystack 안에 들어 있는 needles 항목 수 구하기
found = len(needles & haystack)


# 3.9 dict와 set의 내부 구조
"""
dict, set에는 in 연산자 검색을 지원하는 해시 테이블이 있어 검색이 빠르다.
dict의 구현 방식을 알아보자.

해시 테이블 = Sparse Array(희소 배열)
해시 테이블 안에 있는 항목 = bucket(버킷)
dict 해시 테이블에는 각 항목 별로 버킷이 있고, 버킷에는 키에 대한 참조와 항목의 값에 대한 참조가 들어간다.
파이썬은 버킷의 1/3 이상을 비워두려고 노력함. 해시 테이블 항목이 많아지면 더 넓은 공간에 복사하여 버킷 공간을 확보함

해시 테이블 안에 항목을 넣을 때, 먼저 항목 키의 해시 값을 계산한다.
내장 자료형은 hash 함수가, 사용자 자료형은 __hash__가 처리한다.
효율성을 높이려먼 비슷해보이는 객체들의 해시값은 상당히 달라져서, 인덱스 공간에 골고루 퍼져야 한다.
Ex) 1.01과 1.02의 해시값은 매우 달라야 한다. (실제로 다르다.)

해시 테이블 알고리즘
my_dict[search_key]에서 값을 가져오기 위해 파이썬은
__hash__(search_key)를 호출하여 search_key의 해시값을 가져오고,
해시값의 최하위 비트를 해시 테이블 안의 버킷에 대한 offset으로 사용한다.
찾아낸 버킷이 비어있으면 KeyError를 발생시키고,
비어있지 않으면, 버킷에 들어있는 항목인 (found_key: found_value) 쌍을 검사해서
search_key == found_key인지 검사한다. 일치하면 제대로 찾은 것이므로 found_value를 반환함

search_key와 found_key가 다른 경우에는 해시 충돌이 발생함
해시 충돌은 해시 함수가 임의의 객체를 적은 수의 비트로 매핑하기 때문에 발생함
이렇게 다른 경우(해시 충돌이 발생하는 경우)에는 알고리즘은 해시의 다른 비트들을 조작하여
그 결과를 이용해 다른 버킷을 조회한다. 계속 이 프로세스를 반복한다.

항목을 추가/갱신하는 과정도 동일하다.
빈 버킷을 찾으면 새로운 항목을 추가하고, 동일한 키를 가진 버킷을 찾으면 새로운 값으로 갱신한다.
"""

# 3.9.3 dict 작동 방식에 의한 영향
# dict: 키 검색이 빠른 대신 메모리 공간 효율이 낮다.
# 내부적으로 해시테이블을 사용하고 있기 때문에 해시가 제대로 작동하려면 빈 공간이 커야 한다.
# 많은 양의 레코드를 처리하는 경우네는 dict 의 리스트를 사용하는 것보다 NameTuple 의 리스트를 사용하는 것이 낫다.
# dict 에 항목을 추가하면 기존 키의 순서가 변경될 수 있다.


#------------ -----------------
# 7장: 함수 데커레이터와 클로저
# 7.1 데커레이터 기본 지식
# 데커레이터: 다른 함수를 인수로 받는 callable(호출가능한 객체)
# -- 데커레이트된 함수에 어떤 처리를 수행하고, 함수를 반환하거나 함수를 다른 함수나 callable 객체로 대체한다.

# 7.2 파이썬이 데커레이터를 실행하는 시점
# -- 데커레이터는 데커레이트된 함수가 정의된 직후에 실행된다.
# 일반적으로 파이썬이 모듈을 로딩하는 시점, 즉 임포트 타임에 실행된다. (p252 참조)

# 7.4 변수 범위(글로벌, 지역) 규칙
# 파이썬은 변수가 선언되어 있기를 요구하지는 않지만, 함수 본체 안에서 할당된 변수는 지역변수로 판단한다.

# 예: 함수 본체 안에서 값을 할당하기 때문에 이미 이전에 선언했음에도 지역변수가 되어버리는 p2
p2 = 6
def print_p1_p2(p1):
    print(p1)
    print(p2)
    p2 = 3

print_p1_p2(p1=10)

# --> 함수 안에 할당하는 문장이 있지만 Interpreter가 p2를 전역 변수로 다루기 원한다면
# global 키워드를 이용해서 선언해야 한다.
p2 = 6
def new_print(p1):
    global p2
    print(p1)
    print(p2)
    p2 = 3

new_print(p1=10)

# 위 두 함수의 바이트 코드가 다른지 알아보고 싶다면 dis module을 사용하면 된다.
from dis import dis
dis(print_p1_p2)
dis(new_print)


# 7.5 클로저

















#----------
# Project
import numpy as np
import pandas as pd
from time import perf_counter

mcc = np.random.choice(['1101', '1102', '1103', '1201', '1202', '1203', '1301', '1302', '2101',
                       '2102', '2201', '2202', '2203', '2301', '2302'], size=(4000000, ), replace=True)
avt = np.random.choice(['01', '02', '03', '04', '05', '06', '07', '08'], size=(4000000, ), replace=True)
amt = np.random.randint(low=1000, high=100000, size=(4000000, ))

data = pd.DataFrame({'mcc': mcc, 'avt': avt, 'amt': amt})

def mcc_by_avt(data=data, mcc_col=None, avt_col=None, squeeze=False):
    if mcc_col == None:
        mcc_col = set(data['mcc'])
    if avt_col == None:
        avt_col = set(data['avt'])

    data['mcc_group'] = [data['mcc'][i][0:2] for i in range(data.shape[0])]

    mask1 = data['mcc'].isin(mcc_col)
    mask2 = data['avt'].isin(avt_col)
    masked_data = data[mask1][mask2]

    if squeeze:
        output = masked_data['amt'].groupby([data['mcc_group'], data['avt']]).size().unstack('mcc_group')
    else:
        output = masked_data['amt'].groupby([data['mcc'], data['avt']]).size().unstack('mcc')

    return output

start = perf_counter()
output = mcc_by_avt(data=data,
                    mcc_col=['1101', '1102', '1103', '1201', '1202', '1203'],
                    avt_col=['01', '02', '03', '04'],
                    squeeze=False)
print(output)
print("Time: {}".format(perf_counter() - start))


















