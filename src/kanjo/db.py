from sqlmodel import SQLModel, Session, select, text
from kanjo.models import Mood, MoodVariant


def setup_db_and_tables(engine) -> None:
    SQLModel.metadata.create_all(engine)
    with engine.connect() as connection:
        connection.execute(text("PRAGMA foreign_keys=ON"))
        connection.execute(text("PRAGMA synchronous=NORMAL"))

    with Session(engine) as session:
        stmt = select(Mood)
        results = session.exec(stmt).all()

        if not results:
            default_moods = [
                Mood(name="very happy", variant=MoodVariant.VERY_POSITIVE),
                Mood(name="happy", variant=MoodVariant.POSITIVE),
                Mood(name="meh", variant=MoodVariant.NEUTRAL),
                Mood(name="sad", variant=MoodVariant.NEGATIVE),
                Mood(name="very sad", variant=MoodVariant.VERY_NEGATIVE),
            ]
            session.add_all(default_moods)
            session.commit()
