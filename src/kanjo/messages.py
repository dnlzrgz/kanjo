from textual.message import Message


class NewMood(Message):
    pass


class UpdateMood(Message):
    def __init__(self, mood_id: int) -> None:
        self.mood_id = mood_id
        super().__init__()


class DeleteMood(Message):
    def __init__(self, mood_id: int) -> None:
        self.mood_id = mood_id
        super().__init__()


class NewLog(Message):
    def __init__(self, mood_id: int | None = None) -> None:
        self.mood_id = mood_id
        super().__init__()
