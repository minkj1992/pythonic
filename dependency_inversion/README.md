# Dependency Inversion
> `ABC`, `abstractmethod`를 활용한 DI

- 강하게 결합되어있던 부분을 ABC를 활용해 인터페이스를 정의 내린다.
- 정의 내린 인터페이스를 기반으로 실제 `LightBulb`타입을 받던 부분을 `Switchable` 타입으로 변경
- 이를 통해 새로운 스위치 타입이 들어오더라도 유연하게 동작할 수 있도록 함.