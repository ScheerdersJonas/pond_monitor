from .base import Storage
import logging
import duckdb

logger = logging.getLogger(__name__)

class DuckDbStorage(Storage):
    def __init__(self, db_path: str, read_only: bool = False):
        self.db_path = db_path
        self.conn = duckdb.connect(db_path, read_only=read_only)
        if not read_only:
            self.create_table()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self.conn.close()
        logger.debug("Closed DuckDB connection to %s", self.db_path)

    def create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS readings (
                timestamp TIMESTAMP,
                apower DOUBLE,
                voltage DOUBLE,
                current DOUBLE
            )
        """)

    def write(self, data):
        self.conn.execute(
            "INSERT INTO readings VALUES (?, ?, ?, ?)",
            [data["timestamp"], data["apower"], data["voltage"], data["current"]]
        )