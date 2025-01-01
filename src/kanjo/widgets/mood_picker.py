from textual.containers import HorizontalScroll


class MoodPicker(HorizontalScroll):
    def __init__(self) -> None:
        super().__init__()
        self.classes = "mood_picker__container"
        self.border_title = "moods"
