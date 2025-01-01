from sqlmodel import Field, Relationship, SQLModel


class Mood(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    color: str = Field(unique=True)

    logs: list["Log"] = Relationship(back_populates="mood", cascade_delete=True)


class Log(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    message: str | None

    mood_id: int = Field(default=None, foreign_key="mood.id", ondelete="CASCADE")
    mood: Mood = Relationship(back_populates="logs")
