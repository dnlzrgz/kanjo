from sqlmodel import SQLModel, create_engine, text
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header
from kanjo.settings import APP_NAME, DB_URL, Settings
from kanjo.models import *


def setup_db_and_tables(engine) -> None:
    SQLModel.metadata.create_all(engine)
    with engine.connect() as connection:
        connection.execute(text("PRAGMA foreign_keys=ON"))


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
        yield Header()
        yield Footer()
