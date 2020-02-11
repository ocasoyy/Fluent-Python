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

dict = {'A': 1}
isinstance(dict, collections.abc.Mapping)

# 표준 라이브러리에서 사용하는 Mapping 형은 모두 dict를 이용하여 구현하므로
# 키가 해시가능해야 한다.
# 해시가능: 수명 주기 동안 변하지 않는 해시값을 갖고 있고, 다른 객체와 비교할 수 있음
# -- 위 정의에서 __hash__, __eq__ 메서드가 필요함

# 예를 들어 리스트는 해시가능하지 않다.
hash([1, 2])

# 3.3 공통적인 매핑 메서드
dict = {'A': 1, 'B': 2}
print(dict['C'])    # 당연히 KeyError가 뜸

# 임시 방편: get
# KeyError를 처리하지 않고, 값이 존재하지 않는 Key를 호출하였을 때 기본값을 부여하는 get 메서드
dict = {'A': 1, 'B': 2}
result = {}
for key in ['A', 'B', 'C']:
    value = dict.get(key, 0)
    result[key] = value

print(result)

# 해결책
# (1) setdefault
def count_letters(word):
    letters = list(word)
    dict = {}
    for letter in letters:
        dict.setdefault(letter, 0)
        dict[letter] += 1

    return dict

result1 = count_letters('AAABBC')
print(result1)

# (2) defaultdict
def count_letters(word):
    letters = list(word)
    dict = collections.defaultdict(lambda: 0)
    for letter in letters:
        dict[letter] += 1

    return dict

result2 = count_letters('AAABBC')
print(result2)

# 위 함수는 사실 collections.Counter를 이용하면 쉽게 구현할 수 있다.

# (3): __missing__() 메서드
# 기본 클래스인 dict에는 정의되어 있지는 않지만, dict는 이 메서드를 알고 있음
# dict 클래스를 상속하고 __missing__ 메서드를 정의하면,
# dict.__getitem__() 표준 메서드가 키를 발견할 수 없을 때 KeyError를 발생시키지 않고
# __missing__ 메서드를 호출한다.
# __missing__ 메서드는 오직 __getitem__ 메서드를 사용할 때만 호출되기 때문이다.

# dict가 아닌 UserDict를 상속하는 것이 좋다.

class StrKeyDict(collections.UserDict):
    def __missing__(self, key):
        # key가 문자열이고 존재하지 않으면 KeyError
        if isinstance(key, str):
            raise KeyError(key)
        return self[str(key)]

    def __contains__(self, key):
        # 저장된 키가 모두 str 형이므로 self.data에서 바로 조회할 수 있다.
        return str(key) in self.data

    def __setitem__(self, key, item):
        self.data[str(key)] = item




