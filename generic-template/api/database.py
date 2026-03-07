"""
Generic Analysis Platform - Database
SQLite database with user auth, items, analyses, and audit logs.
"""

import json
import os
import secrets
import sqlite3
from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash

DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, 'platform.db')


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            name TEXT,
            security_question TEXT,
            security_answer_hash TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            category_id TEXT NOT NULL,
            metadata_json TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            has_video BOOLEAN DEFAULT 0,
            overall_score REAL,
            grade TEXT,
            primary_score REAL,
            secondary_score REAL,
            motion_score REAL,
            behavior_score REAL,
            results_json TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (item_id) REFERENCES items (id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            token TEXT UNIQUE NOT NULL,
            expires_at TIMESTAMP NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS password_reset_tokens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            token TEXT UNIQUE NOT NULL,
            expires_at TIMESTAMP NOT NULL,
            used BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            analysis_id INTEGER,
            user_id INTEGER,
            item_id INTEGER,
            algorithm_version TEXT NOT NULL,
            input_type TEXT NOT NULL,
            axis_scores_json TEXT,
            final_score REAL,
            grade TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Migration for existing DBs
    cursor.execute("PRAGMA table_info(users)")
    columns = [row[1] for row in cursor.fetchall()]
    if 'security_question' not in columns:
        cursor.execute('ALTER TABLE users ADD COLUMN security_question TEXT')
    if 'security_answer_hash' not in columns:
        cursor.execute('ALTER TABLE users ADD COLUMN security_answer_hash TEXT')

    conn.commit()
    conn.close()


# =========================================================================
# User Functions
# =========================================================================

def create_user(email, password, name=None, security_question=None, security_answer=None):
    conn = get_db()
    cursor = conn.cursor()
    password_hash = generate_password_hash(password)
    answer_hash = generate_password_hash(security_answer.strip().lower()) if security_answer else None
    try:
        cursor.execute(
            'INSERT INTO users (email, password_hash, name, security_question, security_answer_hash) VALUES (?, ?, ?, ?, ?)',
            (email.lower(), password_hash, name, security_question, answer_hash)
        )
        conn.commit()
        uid = cursor.lastrowid
        conn.close()
        return {'id': uid, 'email': email, 'name': name}
    except sqlite3.IntegrityError:
        conn.close()
        return None


def verify_user(email, password):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ?', (email.lower(),))
    row = cursor.fetchone()
    conn.close()
    if row and check_password_hash(row['password_hash'], password):
        return {'id': row['id'], 'email': row['email'], 'name': row['name'], 'created_at': row['created_at']}
    return None


def get_user_by_id(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, email, name, created_at FROM users WHERE id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def get_user_by_email(email):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, email, name, security_question, security_answer_hash FROM users WHERE email = ?',
                   (email.lower(),))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def verify_security_answer(email, answer):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, email, name, security_answer_hash FROM users WHERE email = ?', (email.lower(),))
    row = cursor.fetchone()
    conn.close()
    if row and row['security_answer_hash'] and check_password_hash(row['security_answer_hash'], answer.strip().lower()):
        return {'id': row['id'], 'email': row['email'], 'name': row['name']}
    return None


def update_user_password(user_id, new_password):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET password_hash = ? WHERE id = ?',
                   (generate_password_hash(new_password), user_id))
    conn.commit()
    conn.close()


# =========================================================================
# Session Functions
# =========================================================================

def create_session(user_id, days=30):
    conn = get_db()
    cursor = conn.cursor()
    token = secrets.token_urlsafe(32)
    expires_at = datetime.fromtimestamp(datetime.now().timestamp() + days * 86400)
    cursor.execute('INSERT INTO sessions (user_id, token, expires_at) VALUES (?, ?, ?)',
                   (user_id, token, expires_at))
    conn.commit()
    conn.close()
    return token


def verify_session(token):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT s.*, u.email, u.name FROM sessions s
        JOIN users u ON s.user_id = u.id
        WHERE s.token = ? AND s.expires_at > datetime('now')
    ''', (token,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {'id': row['user_id'], 'email': row['email'], 'name': row['name']}
    return None


def delete_session(token):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM sessions WHERE token = ?', (token,))
    conn.commit()
    conn.close()


# =========================================================================
# Reset Token Functions
# =========================================================================

def create_reset_token(user_id, hours=1):
    conn = get_db()
    cursor = conn.cursor()
    token = secrets.token_urlsafe(32)
    expires_at = datetime.fromtimestamp(datetime.now().timestamp() + hours * 3600)
    cursor.execute('INSERT INTO password_reset_tokens (user_id, token, expires_at) VALUES (?, ?, ?)',
                   (user_id, token, expires_at))
    conn.commit()
    conn.close()
    return token


def verify_reset_token(token):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM password_reset_tokens
        WHERE token = ? AND used = 0 AND expires_at > datetime('now')
    ''', (token,))
    row = cursor.fetchone()
    if row:
        cursor.execute('UPDATE password_reset_tokens SET used = 1 WHERE id = ?', (row['id'],))
        conn.commit()
        conn.close()
        return row['user_id']
    conn.close()
    return None


# =========================================================================
# Item Functions
# =========================================================================

def create_item(user_id, name, category_id, metadata=None):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO items (user_id, name, category_id, metadata_json) VALUES (?, ?, ?, ?)',
        (user_id, name, category_id, json.dumps(metadata or {}, ensure_ascii=False))
    )
    conn.commit()
    item_id = cursor.lastrowid
    conn.close()
    return {'id': item_id, 'name': name, 'category_id': category_id}


def get_items_by_user(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT i.*,
               (SELECT COUNT(*) FROM analyses WHERE item_id = i.id) as analysis_count,
               (SELECT overall_score FROM analyses WHERE item_id = i.id ORDER BY created_at DESC LIMIT 1) as latest_score
        FROM items i WHERE i.user_id = ? ORDER BY i.created_at DESC
    ''', (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_item_by_id(item_id, user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM items WHERE id = ? AND user_id = ?', (item_id, user_id))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def delete_item(item_id, user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM analyses WHERE item_id = ? AND user_id = ?', (item_id, user_id))
    cursor.execute('DELETE FROM items WHERE id = ? AND user_id = ?', (item_id, user_id))
    conn.commit()
    conn.close()


# =========================================================================
# Analysis Functions
# =========================================================================

def save_analysis(item_id, user_id, has_video, results):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO analyses (item_id, user_id, has_video, overall_score, grade,
                              primary_score, secondary_score, motion_score, behavior_score,
                              results_json)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        item_id, user_id, has_video,
        results.get('overall_score'), results.get('grade'),
        results.get('scores', {}).get('primary', {}).get('score'),
        results.get('scores', {}).get('secondary', {}).get('score'),
        results.get('scores', {}).get('motion', {}).get('score'),
        results.get('scores', {}).get('behavior', {}).get('score'),
        json.dumps(results, ensure_ascii=False)
    ))
    conn.commit()
    aid = cursor.lastrowid
    conn.close()
    return aid


def get_analyses_by_item(item_id, user_id, limit=50):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM analyses WHERE item_id = ? AND user_id = ? ORDER BY created_at DESC LIMIT ?',
                   (item_id, user_id, limit))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_recent_analyses(user_id, limit=10):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT a.*, i.name as item_name, i.category_id
        FROM analyses a JOIN items i ON a.item_id = i.id
        WHERE a.user_id = ? ORDER BY a.created_at DESC LIMIT ?
    ''', (user_id, limit))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def save_audit_log(analysis_id, user_id, item_id, algorithm_version,
                   input_type, axis_scores, final_score, grade):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO audit_logs (analysis_id, user_id, item_id, algorithm_version,
                                input_type, axis_scores_json, final_score, grade)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (analysis_id, user_id, item_id, algorithm_version, input_type,
          json.dumps(axis_scores, ensure_ascii=False), final_score, grade))
    conn.commit()
    conn.close()


init_db()
