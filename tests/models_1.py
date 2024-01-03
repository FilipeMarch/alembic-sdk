from sqlmodel import Field, SQLModel


class User(SQLModel, table=True, extra="allow"):
    __tablename__ = "users"

    id: int = Field(primary_key=True)
    name: str = Field(max_length=100)
