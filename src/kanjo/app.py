from sqlmodel import Session, create_engine, select
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Button, Footer, Header
from kanjo.models import Log, Mood
from kanjo.settings import APP_NAME, DB_URL, Settings
from kanjo.widgets.logs_table import LogsTable
from kanjo.widgets.mood_picker import MoodPicker
from kanjo.db import setup_db_and_tables


class KanjoApp(App):
    """
    A Textual-base mood tracker application.
    """

    TITLE = APP_NAME
    ENABLE_COMMAND_PALETTE = False
    CSS_PATH = "global.tcss"

    BINDINGS = [("ctrl+q", "quit", "quit")]

    def __init__(self):
        super().__init__()

        self.settings = Settings()

        self.engine = create_engine(f"sqlite:///{DB_URL}")
        setup_db_and_tables(self.engine)

        self.theme = self.settings.theme

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

    def on_mount(self) -> None:
        # TODO: refactor db queries out
        with Session(self.engine) as session:
            moods_in_db = session.exec(select(Mood))
            assert moods_in_db

            for mood in moods_in_db:
                self.mood_picker.mount(
                    Button(
                        label=mood.name,
                        variant=mood.variant.button_variant(),
                    )
                )

            logs_in_db = session.exec(select(Log))
            if not logs_in_db:
                return

            for log in logs_in_db:
                self.logs_table.add_row(key=f"{log.id}", label=log.message)
