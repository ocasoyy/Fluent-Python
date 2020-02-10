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


# 2 시퀀스
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

# 커다란 실수 배열의 생성, 저장, 로딩
from array import array
from random import random

floats = array('d', )









