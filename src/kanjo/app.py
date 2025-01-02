from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, create_engine, select
from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container
from textual.widgets import Button, Footer, Header
from kanjo.messages import NewLog, NewMood, DeleteMood, UpdateMood
from kanjo.models import Log, Mood, MoodVariant
from kanjo.settings import APP_NAME, DB_URL, Settings
from kanjo.widgets import NewMoodModal, LogsTable, MoodPicker
from kanjo.db import setup_db_and_tables
from kanjo.widgets.confirm_modal import ConfirmModal


class KanjoApp(App):
    """
    A Textual-base mood tracker application.
    """

    TITLE = APP_NAME
    ENABLE_COMMAND_PALETTE = False
    CSS_PATH = "global.tcss"

    BINDINGS = [
        Binding("ctrl+q,ctrl+c", "quit", "quit"),
        Binding("enter,ctrl+n", "new log", "new log"),
    ]

    def __init__(self):
        super().__init__()

        self.settings = Settings()
        self.theme = self.settings.theme

        self.engine = create_engine(f"sqlite:///{DB_URL}")
        setup_db_and_tables(self.engine)

    def compose(self) -> ComposeResult:
        self.mood_picker = MoodPicker()
        self.logs_table = LogsTable()

        yield Header()
        yield Container(
            self.mood_picker,
            self.logs_table,
            id="main",
        )
        yield Footer()

    async def on_mount(self) -> None:
        # TODO: refactor db queries out
        await self.refresh_moods()
        with Session(self.engine) as session:
            logs_in_db = session.exec(select(Log))
            if not logs_in_db:
                return

            for log in logs_in_db:
                self.logs_table.add_row(key=f"{log.id}", label=log.message)

    @on(NewMood)
    async def create_mood(self) -> None:
        async def callback(response: dict | None = None) -> None:
            if not response:
                return

            assert isinstance(response, dict)
            with Session(self.engine) as session:
                try:
                    variant = response["variant"]
                    new_mood = Mood(
                        name=response["name"],
                        variant=MoodVariant[variant.upper()],
                    )
                    session.add(new_mood)
                    session.commit()

                    await self.refresh_moods()
                    self.notify("new mood added")
                except IntegrityError:
                    self.notify(
                        "mood names must be unique",
                        severity="error",
                    )
                    session.rollback()
                except Exception:
                    self.notify(
                        "something went wrong while saving new mood",
                        severity="error",
                    )
                    session.rollback()

        self.push_screen(NewMoodModal(), callback)

    @on(UpdateMood)
    def update_mood(self, message: UpdateMood) -> None:
        self.notify(f"updatting mood {message.mood_id}")

    @on(DeleteMood)
    def delete_mood(self, message: DeleteMood) -> None:
        mood_id = message.mood_id
        with Session(self.engine) as session:
            mood = session.exec(select(Mood).where(Mood.id == mood_id)).first()
            if not mood:
                self.notify("selected mood not found!", severity="error")
                return

        async def callback(response: bool | None = False) -> None:
            if not response:
                return

            with Session(self.engine) as session:
                try:
                    session.delete(mood)
                    session.commit()

                    await self.refresh_moods()
                except Exception:
                    self.notify(
                        f'something went wrong while deleting mood "{mood.name}"',
                        severity="error",
                    )

        self.push_screen(
            ConfirmModal(
                border_title="delete mood",
                message=f'are you sure that you want to delete mood "{mood.name}"?',
                action_name="delete",
            ),
            callback,
        )

    @on(NewLog)
    def add_log(self, message: NewLog) -> None:
        if message.mood_id:
            self.notify(f"adding log with mood {message.mood_id}")
            return

        self.notify("adding log")

    async def refresh_moods(self) -> None:
        await self.mood_picker.remove_children(Button)

        with Session(self.engine) as session:
            moods_in_db = session.exec(select(Mood)).all()
            assert moods_in_db

            for mood in moods_in_db:
                self.mood_picker.mount(
                    Button(
                        label=mood.name,
                        variant=mood.variant.button_variants(),
                        id=f"mood_{mood.id}",
                    )
                )
