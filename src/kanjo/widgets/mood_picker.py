from textual.binding import Binding
from textual.containers import HorizontalScroll
from textual.widgets import Button
from kanjo.messages import NewLog, NewMood, DeleteMood, UpdateMood


class MoodPicker(HorizontalScroll):
    BINDINGS = [
        Binding("ctrl+a", "new_mood", "new mood"),
        Binding("ctrl+e", "update", "update"),
        Binding("backspace", "delete", "delete"),
        Binding("enter,ctrl+n", "new_log", "new log", priority=True),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.border_title = "moods"

    def action_new_mood(self) -> None:
        self.post_message(NewMood())

    def action_update(self) -> None:
        focused_widget = self.app.focused
        if isinstance(focused_widget, Button) and focused_widget.id:
            mood_id = int(focused_widget.id.split("_")[1])
            self.post_message(UpdateMood(mood_id))
            return

        self.notify("no mood selected!", severity="warning")

    def action_delete(self) -> None:
        focused_widget = self.app.focused
        if isinstance(focused_widget, Button) and focused_widget.id:
            mood_id = int(focused_widget.id.split("_")[1])
            self.post_message(DeleteMood(mood_id))
            return

        self.notify("no mood selected!", severity="warning")

    def action_new_log(self) -> None:
        focused_widget = self.app.focused
        if isinstance(focused_widget, Button) and focused_widget.id:
            mood_id = int(focused_widget.id.split("_")[1])
            self.post_message(NewLog(mood_id))
