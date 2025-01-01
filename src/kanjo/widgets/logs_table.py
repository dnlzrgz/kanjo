from textual.widgets import DataTable


class LogsTable(DataTable):
    def __init__(self, *args, **kwargs):
        super().__init__(
            cursor_type="row",
            header_height=0,
            *args,
            **kwargs,
        )

    def on_mount(self) -> None:
        self.add_column("logs", key="logs")
        self.border_title = "logs"
