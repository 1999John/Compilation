class MyList(list):
    def __init__(self) -> None:
        super().__init__()

    def index(self, __value, __start: int = ..., __stop: int = ...) -> int:
        for _ in range(len(self)):
            i = self.pop(0)
            if str(i)==__value:
                return i

