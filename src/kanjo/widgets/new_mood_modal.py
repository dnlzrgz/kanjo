from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Select, Static
from textual.validation import Length
from kanjo.models import MoodVariant


class NewMoodModal(ModalScreen[dict | None]):
    BINDINGS = [Binding("escape", "dismiss", "dismiss")]

    def compose(self) -> ComposeResult:
        with VerticalScroll(classes="modal modal--new-mood") as container:
            container.border_title = "new mood"

            yield Container(
                Container(
                    Static("name"),
                    Input(
                        placeholder="happy",
                        validators=[
                            Length(
                                minimum=1,
                                failure_description="mood name is too short",
                            )
                        ],
                    ),
                    classes="modal__mood-name",
                ),
                Container(
                    Static("variant"),
                    Select(
                        (
                            (variant[1], variant[1])
                            for variant in MoodVariant.list_variants()
                        ),
                        value=MoodVariant.NEUTRAL.value,
                        allow_blank=False,
                    ),
                    classes="modal__mood-variant",
                ),
                classes="modal__form",
            )
            yield Button(
                label="add",
                classes="modal__submit",
                disabled=True,
            )

    @on(Input.Changed)
    def validate_input_name(self, event: Input.Changed) -> None:
        submit_button: Button = self.query_one(Button)
        if event.validation_result.is_valid:
            submit_button.disabled = False
        else:
            submit_button.disabled = True

    @on(Input.Submitted)
    @on(Button.Pressed)
    async def submit_form(self) -> None:
        name_input: Input = self.query_one(Input)
        variant_input: Select = self.query_one(Select)

        self.dismiss(
            {
                "name": name_input.value,
                "variant": variant_input.value,
            }
        )
