import enum
from sqlmodel import Column, Enum, Field, Relationship, SQLModel


class MoodVariant(enum.Enum):
    VERY_POSITIVE = "very positive"
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"
    VERY_NEGATIVE = "very negative"

    def button_variants(self) -> str:
        return {
            MoodVariant.VERY_POSITIVE: "success",
            MoodVariant.POSITIVE: "primary",
            MoodVariant.NEUTRAL: "default",
            MoodVariant.NEGATIVE: "warning",
            MoodVariant.VERY_NEGATIVE: "error",
        }.get(self, "default")

    @classmethod
    def list_variants(cls) -> list[tuple[str, str]]:
        return [(mood.name, mood.value) for mood in cls]


class Mood(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    variant: MoodVariant = Field(
        sa_column=Column(
            Enum(MoodVariant),
            default=MoodVariant.NEUTRAL,
        )
    )

    logs: list["Log"] = Relationship(back_populates="mood", cascade_delete=True)


class Log(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    message: str | None

    mood_id: int = Field(default=None, foreign_key="mood.id", ondelete="CASCADE")
    mood: Mood = Relationship(back_populates="logs")
