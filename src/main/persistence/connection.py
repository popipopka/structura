import enum

from sqlalchemy import create_engine, Engine


class Dialect(enum.Enum):
    POSTGRESQL = "postgresql"

    @staticmethod
    def from_value(value: str) -> "Dialect":
        return Dialect(value)


class Driver(enum.Enum):
    PSYCOPG2 = "psycopg"

    @staticmethod
    def get(dialect: Dialect) -> "Driver":
        mapping = {
            Dialect.POSTGRESQL: Driver.PSYCOPG2,
        }

        return mapping[dialect]


class DatabaseURL:
    def __init__(self, dialect: Dialect, user: str, password: str, host: str, port: int, database: str):
        self.dialect = dialect
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database

        self.url = f"{self._dialect_plus_driver()}://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

    def __str__(self):
        return self.url

    def _dialect_plus_driver(self) -> str:
        driver = Driver.get(self.dialect)
        return f"{self.dialect.value}+{driver.value}"


class Connection:
    def __init__(self, db_url: DatabaseURL):
        self.engine = create_engine(str(db_url))

    def get_engine(self) -> Engine:
        return self.engine

    def close(self) -> None:
        self.engine.dispose()