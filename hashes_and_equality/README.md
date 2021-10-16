# Object Equality 
> [Python Hashes and Equality](https://hynek.me/articles/hashes-and-equality/)

## conclusion
`__eq__`를 변경하지 않았다면 `__hash__`를 변경해서는 안 된다.

## `Object Equality`
> By default, those methods are inherited from the object class that compares two instances by their identity – therefore instances are only equal to themselves.
- `__eq__(self, other)`는 ==에 사용된다
- python3부터는 `__ne__`를 재정의 하지 않아도 된다.
    - `!=` now returns the opposite of `==`, unless `==` returns `NotImplemented`
    - For `__ne__()`, by default it delegates to `__eq__()` and inverts the result unless it is `NotImplemented`


## `Object Hashes`
> An object hash is an integer number representing the value of the object and can be obtained using the hash() function if the object is hashable

- `Hashable`
    - =**The hash of an object must never change during its lifetime.**
    - 클래스가 hashable하려면 `__eq__(self)`와 `__hash__(self)`를 구현해야 한다.   

- `Hashable`하다는 것은 해당 엔티티의 unique함을 보장한다. (hash collision 제외)
- 이러한 특성을 통해 hash의 int값으로 빠르게 객체의 equality 비교가 가능하다.
- hashable하기 위해서는 collection이 mutable해서는 안된다.
- 중복이 없어야하는 dict, set의 item을 비교할 때 사용될 수 있다. 따라서, set과 dict의 key값들은 중복이 되면 안되기에, hashable해야한다.


## summary
- `hash()`는 attr이 같으면 같은 int를 만들어낸다. 값이 변경되면 hash값 또한 변경된다.
- `__eq__`는 비교에 사용된다.
- dict의 key와 set에서 사용하려면 hashable해야 한다.
- hashable하다면 두 객체의 동등성을 한번의 연산으로 빠르게 계산할 수 있다.
- `__eq__`만 override한 object를 `hash(object)`에 호출시키면 `TypeError: unhashable`가 발생한다.
- Two objects that compare equal must also have the same hash value, but the reverse is not necessarily true.
    - 이런 hashable한 object을 직접 만든다고 한다면, 해당 규칙은 개발자가 책임진다.

## refs
- https://docs.python.org/3/reference/datamodel.html#object.__ne__
- https://stackoverflow.com/questions/4352244/should-ne-be-implemented-as-the-negation-of-eq