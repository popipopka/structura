import enum

from sqlalchemy import create_engine, Engine, URL


class Dialect(enum.Enum):
    POSTGRESQL = "postgresql"
    MARIADB = "mariadb"
    MYSQL = "mysql"

    @staticmethod
    def from_value(value: str) -> "Dialect":
        return Dialect(value)


class Driver(enum.Enum):
    PSYCOPG2 = "psycopg"
    PYMYSQL = "pymysql"

    @staticmethod
    def get(dialect: Dialect) -> "Driver":
        mapping = {
            Dialect.POSTGRESQL: Driver.PSYCOPG2,
            Dialect.MARIADB: Driver.PYMYSQL,
            Dialect.MYSQL: Driver.PYMYSQL,
        }

        return mapping[dialect]


class DatabaseURL:
    def __init__(self, dialect: Dialect, user: str, password: str, host: str, port: int, database: str):
        self.dialect = dialect
        self.dialect_driver = self._dialect_plus_driver()
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database

        self.url = f"{self.dialect_driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

    def __str__(self):
        return self.url

    def _dialect_plus_driver(self) -> str:
        driver = Driver.get(self.dialect)
        return f"{self.dialect.value}+{driver.value}"


class Connection:
    def __init__(self, db_url: DatabaseURL):
        self.engine = create_engine(URL.create(
            drivername=db_url.dialect_driver,
            username=db_url.user,
            password=db_url.password,
            host=db_url.host,
            port=db_url.port,
            database=db_url.database,
        ))

    def get_engine(self) -> Engine:
        return self.engine

    def close(self) -> None:
        self.engine.dispose()