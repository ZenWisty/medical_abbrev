"""SQLite storage layer for persisting medical samples and abbreviation data.

Provides Database and SampleStorage classes for local data persistence
using SQLite.
"""

import json
import sqlite3
from typing import Optional

from providers.data_models import AbbreviationResult, MedicalSample


class Database:
    """SQLite database wrapper for medical data storage.

    Handles connection management, table creation, and migrations.
    """

    def __init__(self, db_path: str = "medabbrev.db"):
        """Initialize database connection and create tables.

        Args:
            db_path: Path to SQLite database file, or ":memory:" for in-memory.
        """
        self.db_path = db_path
        self.connection = sqlite3.connect(db_path)
        self._create_tables()

    def _create_tables(self) -> None:
        """Create necessary tables if they don't exist."""
        cursor = self.connection.cursor()

        # Medical samples table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS medical_samples (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                category TEXT,
                description TEXT,
                content TEXT,
                url TEXT
            )
        """)

        # Abbreviation results table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS abbreviation_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                abbrev TEXT NOT NULL,
                expansions TEXT NOT NULL,
                sample_ids TEXT
            )
        """)

        # Create index on abbreviation for faster searches
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_abbrev
            ON abbreviation_results(abbrev)
        """)

        self.connection.commit()

    def close(self) -> None:
        """Close the database connection."""
        if self.connection:
            self.connection.close()


class SampleStorage:
    """High-level interface for storing and retrieving medical samples.

    Provides methods for saving and loading samples and abbreviations
    with proper serialization.
    """

    def __init__(self, db_path: str = "medabbrev.db"):
        """Initialize storage with database at given path.

        Args:
            db_path: Path to SQLite database file, or ":memory:" for in-memory.
        """
        self.db = Database(db_path)

    def save_samples(self, samples: list[MedicalSample]) -> None:
        """Persist a list of MedicalSample objects.

        Args:
            samples: List of MedicalSample instances to save.
        """
        cursor = self.db.connection.cursor()
        for sample in samples:
            cursor.execute(
                """
                INSERT OR REPLACE INTO medical_samples
                (id, title, category, description, content, url)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    sample.id,
                    sample.title,
                    sample.category,
                    sample.description,
                    sample.content,
                    sample.url,
                ),
            )
        self.db.connection.commit()

    def load_samples(
        self, limit: Optional[int] = None, category: Optional[str] = None
    ) -> list[MedicalSample]:
        """Retrieve persisted medical samples.

        Args:
            limit: Maximum number of samples to return.
            category: Filter by category name.

        Returns:
            List of MedicalSample instances.
        """
        cursor = self.db.connection.cursor()

        query = "SELECT id, title, category, description, content, url FROM medical_samples"
        params = []

        if category:
            query += " WHERE category = ?"
            params.append(category)

        query += " ORDER BY id"

        if limit:
            query += " LIMIT ?"
            params.append(limit)

        cursor.execute(query, params)
        rows = cursor.fetchall()

        return [
            MedicalSample(
                id=row[0],
                title=row[1],
                category=row[2] or "",
                description=row[3] or "",
                content=row[4] or "",
                url=row[5] or "",
            )
            for row in rows
        ]

    def save_abbreviations(self, abbreviations: list[AbbreviationResult]) -> None:
        """Persist a list of AbbreviationResult objects.

        Args:
            abbreviations: List of AbbreviationResult instances to save.
        """
        cursor = self.db.connection.cursor()
        for abbrev in abbreviations:
            sample_ids = json.dumps([s.id for s in abbrev.samples])
            expansions_json = json.dumps(abbrev.expansions)
            cursor.execute(
                """
                INSERT INTO abbreviation_results (abbrev, expansions, sample_ids)
                VALUES (?, ?, ?)
                """,
                (abbrev.abbrev, expansions_json, sample_ids),
            )
        self.db.connection.commit()

    def search_abbreviations(
        self, abbrev: str, limit: Optional[int] = None
    ) -> list[AbbreviationResult]:
        """Search for abbreviation results.

        Args:
            abbrev: Abbreviation to search for (case-insensitive).
            limit: Maximum number of results to return.

        Returns:
            List of AbbreviationResult instances.
        """
        cursor = self.db.connection.cursor()

        query = """
            SELECT id, abbrev, expansions, sample_ids
            FROM abbreviation_results
            WHERE LOWER(abbrev) = LOWER(?)
        """

        params = [abbrev]

        if limit:
            query += " LIMIT ?"
            params.append(limit)

        cursor.execute(query, params)
        rows = cursor.fetchall()

        results = []
        for row in rows:
            expansions = json.loads(row[2])
            sample_ids = json.loads(row[3])

            # Load associated samples
            samples = []
            if sample_ids:
                placeholders = ",".join(["?"] * len(sample_ids))
                cursor.execute(
                    f"""
                    SELECT id, title, category, description, content, url
                    FROM medical_samples
                    WHERE id IN ({placeholders})
                    """,
                    sample_ids,
                )
                sample_rows = cursor.fetchall()
                samples = [
                    MedicalSample(
                        id=sr[0],
                        title=sr[1],
                        category=sr[2] or "",
                        description=sr[3] or "",
                        content=sr[4] or "",
                        url=sr[5] or "",
                    )
                    for sr in sample_rows
                ]

            results.append(
                AbbreviationResult(
                    abbrev=row[1],
                    expansions=expansions,
                    samples=samples,
                )
            )

        return results

    def close(self) -> None:
        """Close the underlying database connection."""
        self.db.close()