class WordWithDistance:
    def __init__(self, word) -> None:
        self.word = word
        self.distance = None

    def __repr__(self) -> str:
        return f'WordWithDistance({self.__dict__})'
