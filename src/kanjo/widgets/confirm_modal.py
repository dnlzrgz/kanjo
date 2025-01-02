from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Static


class ConfirmModal(ModalScreen[bool | None]):
    BINDINGS = [
        Binding("escape,n", "dismiss", "dismiss"),
        Binding("enter,y", "confirm", "confirm"),
    ]

    def __init__(
        self,
        border_title: str,
        message: str,
        action_name: str,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)

        self.border_title = border_title
        self.message = message
        self.action_name = action_name

    def compose(self) -> ComposeResult:
        with Vertical(classes="modal modal--confirm") as container:
            container.border_title = self.border_title

            yield Static(
                self.message,
                classes="modal__message",
            )
            yield Button(
                label=self.action_name,
                classes="modal__submit modal__submit--confirm",
            )

    def on_mount(self) -> None:
        self.query_one(Button).focus()

    def action_dismiss_overlay(self) -> None:
        self.dismiss(False)

    def action_confirm(self) -> None:
        self.dismiss(True)

    @on(Button.Pressed)
    def confirm_action(self) -> None:
        self.dismiss(True)
