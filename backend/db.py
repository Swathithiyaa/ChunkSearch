import sqlite3
from typing import List, Dict, Any

DB_PATH = 'chunks.db'

def get_connection():
    return sqlite3.connect(DB_PATH)

def create_table():
    with get_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS chunks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_source TEXT,
                label TEXT,
                content TEXT,
                page_number INTEGER,
                created_at TEXT,
                author TEXT,
                category TEXT,
                tags TEXT
            );
        ''')
        conn.commit()

def insert_chunk(chunk: Dict[str, Any]):
    with get_connection() as conn:
        # Check for existing chunk
        cursor = conn.execute(
            '''
            SELECT id FROM chunks
            WHERE file_source = ? AND label = ? AND content = ?
            ''',
            (chunk.get('file_source'), chunk.get('label'), chunk.get('content'))
        )
        if cursor.fetchone():
            return  # Duplicate found, do not insert

        conn.execute('''
            INSERT INTO chunks (file_source, label, content, page_number, created_at, author, category, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            chunk.get('file_source'),
            chunk.get('label'),
            chunk.get('content'),
            chunk.get('page_number'),
            chunk.get('created_at'),
            chunk.get('author'),
            chunk.get('category'),
            ','.join(chunk.get('tags', [])) if chunk.get('tags') else None
        ))
        conn.commit()

def get_all_chunks() -> List[Dict[str, Any]]:
    with get_connection() as conn:
        cursor = conn.execute('SELECT * FROM chunks')
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()] 