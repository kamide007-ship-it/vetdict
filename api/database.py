"""
Database models for ShowDog Analysis Platform
Supports SQLite (default) and PostgreSQL/Supabase via DATABASE_URL.

Backend selection:
  - Set DATABASE_URL env var for PostgreSQL (e.g. Supabase, Render Postgres)
  - Otherwise falls back to SQLite (local development)
"""

import hashlib
import json
import logging
import os
import secrets
import sqlite3
from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash

logger = logging.getLogger(__name__)

# =============================================================================
# Dual-Backend Connection Abstraction
# =============================================================================

DATABASE_URL = os.environ.get('DATABASE_URL', '')

# Detect PostgreSQL backend
_USE_PG = bool(DATABASE_URL and ('postgres' in DATABASE_URL))

if _USE_PG:
    try:
        import psycopg2
        import psycopg2.extras
        import psycopg2.pool
        logger.info(f"[DB] PostgreSQL backend detected")
    except ImportError:
        logger.warning("[DB] psycopg2 not installed, falling back to SQLite")
        _USE_PG = False

# SQLite path (used when _USE_PG is False)
_disk_path = os.environ.get('RENDER_DISK_PATH') or os.environ.get('DATABASE_PATH')
DB_DIR = _disk_path or os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, 'showdog.db')

# PostgreSQL connection pool (lazy-initialized)
_pg_pool = None


def _get_pg_pool():
    """Get or create the PostgreSQL connection pool."""
    global _pg_pool
    if _pg_pool is None:
        db_url = DATABASE_URL
        # Render/Supabase may use postgres:// but psycopg2 needs postgresql://
        if db_url.startswith('postgres://'):
            db_url = db_url.replace('postgres://', 'postgresql://', 1)
        _pg_pool = psycopg2.pool.ThreadedConnectionPool(
            minconn=1, maxconn=10, dsn=db_url
        )
        logger.info("[DB] PostgreSQL connection pool created (1-10 connections)")
    return _pg_pool


class _PGCursorWrapper:
    """Wraps a psycopg2 cursor to auto-convert ? placeholders to %s."""

    def __init__(self, cursor):
        self._cursor = cursor
        self._lastrowid = None

    def execute(self, sql, params=None):
        # Convert ? placeholders to %s for PostgreSQL
        pg_sql = sql.replace('?', '%s')
        # Convert SQLite datetime functions to PostgreSQL equivalents
        pg_sql = pg_sql.replace("datetime('now', 'utc')", "NOW() AT TIME ZONE 'UTC'")
        pg_sql = pg_sql.replace("datetime('now')", "NOW()")
        # Auto-add RETURNING id for INSERT statements to capture lastrowid
        stripped = pg_sql.strip()
        is_insert = stripped.upper().startswith('INSERT')
        if is_insert and 'RETURNING' not in stripped.upper():
            pg_sql = stripped.rstrip(';') + ' RETURNING id'
        self._cursor.execute(pg_sql, params)
        # Capture lastrowid from RETURNING clause
        if is_insert:
            try:
                if self._cursor.description and self._cursor.rowcount > 0:
                    row = self._cursor.fetchone()
                    if row:
                        self._lastrowid = row['id'] if isinstance(row, dict) else row[0]
            except Exception:
                pass

    def executemany(self, sql, params_list):
        pg_sql = sql.replace('?', '%s')
        self._cursor.executemany(pg_sql, params_list)

    def fetchone(self):
        return self._cursor.fetchone()

    def fetchall(self):
        return self._cursor.fetchall()

    @property
    def lastrowid(self):
        return self._lastrowid

    @lastrowid.setter
    def lastrowid(self, value):
        self._lastrowid = value

    @property
    def rowcount(self):
        return self._cursor.rowcount

    @property
    def description(self):
        return self._cursor.description


class _PGConnectionWrapper:
    """Wraps a psycopg2 connection to provide sqlite3-compatible interface."""

    def __init__(self, conn):
        self._conn = conn

    def cursor(self):
        return _PGCursorWrapper(
            self._conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        )

    def commit(self):
        self._conn.commit()

    def rollback(self):
        self._conn.rollback()

    def close(self):
        _get_pg_pool().putconn(self._conn)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.rollback()
        self.close()


def get_db():
    """Get database connection (PostgreSQL or SQLite)."""
    if _USE_PG:
        conn = _get_pg_pool().getconn()
        conn.autocommit = False
        return _PGConnectionWrapper(conn)
    else:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn


def is_postgres():
    """Check if using PostgreSQL backend."""
    return _USE_PG


def _pk():
    """Return primary key definition for current backend."""
    if _USE_PG:
        return 'SERIAL PRIMARY KEY'
    return 'INTEGER PRIMARY KEY AUTOINCREMENT'


def _bool_default(val):
    """Return boolean default for current backend."""
    if _USE_PG:
        return 'BOOLEAN DEFAULT FALSE' if not val else 'BOOLEAN DEFAULT TRUE'
    return f'BOOLEAN DEFAULT {1 if val else 0}'


def _json_type():
    """Return JSON column type for current backend."""
    return 'JSONB' if _USE_PG else 'TEXT'


def _float_type():
    """Return float type for current backend."""
    return 'DOUBLE PRECISION' if _USE_PG else 'REAL'


def init_db():
    """Initialize database tables (PostgreSQL or SQLite)."""
    conn = get_db()
    cursor = conn.cursor()

    pk = _pk()
    bool_false = _bool_default(False)
    json_t = _json_type()
    float_t = _float_type()

    # Users table
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS users (
            id {pk},
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            name TEXT,
            security_question TEXT,
            security_answer_hash TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Dogs table
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS dogs (
            id {pk},
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            breed_id TEXT NOT NULL,
            birth_date DATE,
            weight {float_t},
            gender TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    # Analyses table
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS analyses (
            id {pk},
            dog_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            age_years {float_t},
            has_video {bool_false},
            overall_score {float_t},
            grade TEXT,
            structure_score {float_t},
            coat_score {float_t},
            gait_score {float_t},
            temperament_score {float_t},
            results_json {json_t},
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (dog_id) REFERENCES dogs (id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    # Sessions table (for login tokens)
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS sessions (
            id {pk},
            user_id INTEGER NOT NULL,
            token TEXT UNIQUE NOT NULL,
            expires_at TIMESTAMP NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    # Password reset tokens table
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS password_reset_tokens (
            id {pk},
            user_id INTEGER NOT NULL,
            token TEXT UNIQUE NOT NULL,
            expires_at TIMESTAMP NOT NULL,
            used {bool_false},
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    # --- Column migration helpers ---
    def _get_columns(table_name):
        """Get column names for a table (works on both SQLite and PostgreSQL)."""
        if _USE_PG:
            cursor.execute(
                "SELECT column_name FROM information_schema.columns WHERE table_name = %s",
                (table_name,)
            )
            return [row['column_name'] if isinstance(row, dict) else row[0] for row in cursor.fetchall()]
        else:
            cursor.execute(f"PRAGMA table_info({table_name})")
            return [row[1] if not isinstance(row, dict) else row['name'] for row in cursor.fetchall()]

    def _get_column_info(table_name):
        """Get column info dict {name: notnull} for migration checks."""
        if _USE_PG:
            cursor.execute(
                "SELECT column_name, is_nullable FROM information_schema.columns WHERE table_name = %s",
                (table_name,)
            )
            return {
                (row['column_name'] if isinstance(row, dict) else row[0]):
                (0 if (row['is_nullable'] if isinstance(row, dict) else row[1]) == 'NO' else 1)
                for row in cursor.fetchall()
            }
        else:
            cursor.execute(f"PRAGMA table_info({table_name})")
            return {row[1]: row[3] for row in cursor.fetchall()}

    # Migrate sessions table: add token_hash column for hashed token storage
    session_columns = _get_columns('sessions')
    if 'token_hash' not in session_columns:
        cursor.execute('ALTER TABLE sessions ADD COLUMN token_hash TEXT')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_sessions_token_hash ON sessions(token_hash)')

    # Migrate existing users table: add security columns if missing
    columns = _get_columns('users')
    if 'security_question' not in columns:
        cursor.execute('ALTER TABLE users ADD COLUMN security_question TEXT')
    if 'security_answer_hash' not in columns:
        cursor.execute('ALTER TABLE users ADD COLUMN security_answer_hash TEXT')

    # Migrate users table: add Stripe subscription columns if missing
    if 'subscription_plan' not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN subscription_plan TEXT DEFAULT 'free'")
    if 'stripe_subscription_id' not in columns:
        cursor.execute('ALTER TABLE users ADD COLUMN stripe_subscription_id TEXT')
    if 'subscription_updated_at' not in columns:
        cursor.execute('ALTER TABLE users ADD COLUMN subscription_updated_at TIMESTAMP')

    # Migrate users table: add PayPal subscription column if missing
    if 'paypal_subscription_id' not in columns:
        cursor.execute('ALTER TABLE users ADD COLUMN paypal_subscription_id TEXT')

    # Audit log table (for algorithm governance)
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS audit_logs (
            id {pk},
            analysis_id INTEGER,
            user_id INTEGER,
            dog_id INTEGER,
            algorithm_version TEXT NOT NULL,
            model_version TEXT NOT NULL,
            weights_hash TEXT NOT NULL,
            input_type TEXT NOT NULL,
            axis_scores_json {json_t},
            final_score {float_t},
            grade TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # --- Dog Medical Records (カルテ) ---

    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS dog_medical_records (
            id {pk},
            user_id INTEGER,
            dog_id INTEGER,
            dog_name TEXT NOT NULL,
            breed TEXT,
            color TEXT,
            sex TEXT CHECK(sex IN ('オス', 'メス', '不明')),
            date_of_birth DATE,
            body_length_cm {float_t},
            body_height_cm {float_t},
            body_weight_kg {float_t},
            microchip_number TEXT UNIQUE,
            microchip_date DATE,
            microchip_location TEXT DEFAULT '頸部',
            microchip_type TEXT,
            owner_name TEXT NOT NULL,
            owner_address TEXT,
            owner_phone TEXT,
            purchase_date DATE,
            purchase_place TEXT,
            keeping_place TEXT,
            veterinary_clinic TEXT,
            veterinarian_name TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (dog_id) REFERENCES dogs (id)
        )
    ''')

    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_microchip
        ON dog_medical_records(microchip_number)
    ''')

    # --- Dog Export Application Tables (MAFF 別記様式第１号) ---

    # Export applications main table
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS dog_export_applications (
            id {pk},
            user_id INTEGER,
            dog_id INTEGER,
            applicant_name TEXT NOT NULL,
            applicant_address TEXT,
            applicant_phone TEXT,
            applicant_company_name TEXT,
            applicant_company_representative TEXT,
            animal_species TEXT DEFAULT '犬',
            animal_quantity INTEGER DEFAULT 1,
            animal_name TEXT NOT NULL,
            breed TEXT,
            color TEXT,
            sex TEXT,
            usage_purpose TEXT,
            date_of_birth DATE,
            age_years {float_t},
            destination_country TEXT,
            body_length_cm {float_t},
            body_height_cm {float_t},
            body_weight_kg {float_t},
            embarkation_date DATE,
            embarkation_place TEXT,
            vessel_name TEXT,
            flight_number TEXT,
            consignor_name TEXT,
            consignor_address TEXT,
            consignee_name TEXT,
            consignee_address TEXT,
            keeping_place TEXT,
            purchase_date DATE,
            scheduled_reentry_date DATE,
            identification_method TEXT DEFAULT 'マイクロチップ',
            identification_number TEXT,
            identification_date DATE,
            identification_location TEXT,
            microchip_type TEXT DEFAULT 'ISO 11784/11785',
            microchip_reader_type TEXT,
            laboratory_name TEXT,
            laboratory_address TEXT,
            remarks TEXT,
            application_date DATE DEFAULT CURRENT_DATE,
            status TEXT DEFAULT 'draft',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (dog_id) REFERENCES dogs (id)
        )
    ''')

    # Vaccination records for export applications
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS dog_vaccinations (
            id {pk},
            application_id INTEGER NOT NULL,
            vaccination_type TEXT NOT NULL DEFAULT '狂犬病',
            vaccination_date DATE NOT NULL,
            expiry_date DATE,
            vaccine_kind TEXT,
            product_name TEXT,
            manufacturer TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (application_id)
                REFERENCES dog_export_applications(id) ON DELETE CASCADE
        )
    ''')

    # Rabies serological test records
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS dog_rabies_tests (
            id {pk},
            application_id INTEGER NOT NULL,
            blood_sampling_date DATE NOT NULL,
            antibody_titer_1 {float_t},
            antibody_titer_2 {float_t},
            unit TEXT DEFAULT 'IU/ml',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (application_id)
                REFERENCES dog_export_applications(id) ON DELETE CASCADE
        )
    ''')

    # Migrate dog_rabies_tests: add antibody_titer_2 if missing, rename antibody_titer
    rt_columns = _get_columns('dog_rabies_tests')
    if 'antibody_titer' in rt_columns and 'antibody_titer_1' not in rt_columns:
        cursor.execute('ALTER TABLE dog_rabies_tests RENAME COLUMN antibody_titer TO antibody_titer_1')
    if 'antibody_titer_2' not in rt_columns:
        cursor.execute(f'ALTER TABLE dog_rabies_tests ADD COLUMN antibody_titer_2 {float_t}')

    # Migrate: add medical_record_id to export applications, vaccinations, and tests
    ea_columns = _get_columns('dog_export_applications')
    if 'medical_record_id' not in ea_columns:
        cursor.execute('ALTER TABLE dog_export_applications ADD COLUMN medical_record_id INTEGER REFERENCES dog_medical_records(id)')

    # Migrate dog_vaccinations: make application_id nullable, add medical_record_id
    vac_info = _get_column_info('dog_vaccinations')
    has_vac_mr = 'medical_record_id' in vac_info
    needs_vac_rebuild = vac_info.get('application_id') == 1  # NOT NULL needs to be removed
    if needs_vac_rebuild:
        if _USE_PG:
            # PostgreSQL: ALTER COLUMN directly
            cursor.execute('ALTER TABLE dog_vaccinations ALTER COLUMN application_id DROP NOT NULL')
            if not has_vac_mr:
                cursor.execute('ALTER TABLE dog_vaccinations ADD COLUMN medical_record_id INTEGER REFERENCES dog_medical_records(id)')
        else:
            # SQLite: rebuild table (no ALTER COLUMN support)
            cursor.execute('ALTER TABLE dog_vaccinations RENAME TO _dog_vaccinations_old')
            cursor.execute(f'''
                CREATE TABLE dog_vaccinations (
                    id {pk},
                    application_id INTEGER,
                    medical_record_id INTEGER REFERENCES dog_medical_records(id),
                    vaccination_type TEXT NOT NULL DEFAULT '狂犬病',
                    vaccination_date DATE NOT NULL,
                    expiry_date DATE,
                    vaccine_kind TEXT,
                    product_name TEXT,
                    manufacturer TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (application_id)
                        REFERENCES dog_export_applications(id) ON DELETE CASCADE
                )
            ''')
            if has_vac_mr:
                cursor.execute('''
                    INSERT INTO dog_vaccinations (id, application_id, medical_record_id,
                        vaccination_type, vaccination_date, expiry_date, vaccine_kind,
                        product_name, manufacturer, created_at)
                    SELECT id, application_id, medical_record_id,
                        vaccination_type, vaccination_date, expiry_date, vaccine_kind,
                        product_name, manufacturer, created_at
                    FROM _dog_vaccinations_old
                ''')
            else:
                cursor.execute('''
                    INSERT INTO dog_vaccinations (id, application_id,
                        vaccination_type, vaccination_date, expiry_date, vaccine_kind,
                        product_name, manufacturer, created_at)
                    SELECT id, application_id,
                        vaccination_type, vaccination_date, expiry_date, vaccine_kind,
                        product_name, manufacturer, created_at
                    FROM _dog_vaccinations_old
                ''')
            cursor.execute('DROP TABLE _dog_vaccinations_old')
    elif not has_vac_mr:
        cursor.execute('ALTER TABLE dog_vaccinations ADD COLUMN medical_record_id INTEGER REFERENCES dog_medical_records(id)')

    # Migrate dog_rabies_tests: make application_id nullable, add medical_record_id
    rt_info = _get_column_info('dog_rabies_tests')
    has_rt_mr = 'medical_record_id' in rt_info
    needs_rt_rebuild = rt_info.get('application_id') == 1
    if needs_rt_rebuild:
        if _USE_PG:
            cursor.execute('ALTER TABLE dog_rabies_tests ALTER COLUMN application_id DROP NOT NULL')
            if not has_rt_mr:
                cursor.execute('ALTER TABLE dog_rabies_tests ADD COLUMN medical_record_id INTEGER REFERENCES dog_medical_records(id)')
        else:
            cursor.execute('ALTER TABLE dog_rabies_tests RENAME TO _dog_rabies_tests_old')
            cursor.execute(f'''
                CREATE TABLE dog_rabies_tests (
                    id {pk},
                    application_id INTEGER,
                    medical_record_id INTEGER REFERENCES dog_medical_records(id),
                    blood_sampling_date DATE NOT NULL,
                    antibody_titer_1 {float_t},
                    antibody_titer_2 {float_t},
                    unit TEXT DEFAULT 'IU/ml',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (application_id)
                        REFERENCES dog_export_applications(id) ON DELETE CASCADE
                )
            ''')
            if has_rt_mr:
                cursor.execute('''
                    INSERT INTO dog_rabies_tests (id, application_id, medical_record_id,
                        blood_sampling_date, antibody_titer_1, antibody_titer_2, unit, created_at)
                    SELECT id, application_id, medical_record_id,
                        blood_sampling_date, antibody_titer_1, antibody_titer_2, unit, created_at
                    FROM _dog_rabies_tests_old
                ''')
            else:
                cursor.execute('''
                    INSERT INTO dog_rabies_tests (id, application_id,
                        blood_sampling_date, antibody_titer_1, antibody_titer_2, unit, created_at)
                    SELECT id, application_id,
                        blood_sampling_date, antibody_titer_1, antibody_titer_2, unit, created_at
                    FROM _dog_rabies_tests_old
                ''')
            cursor.execute('DROP TABLE _dog_rabies_tests_old')
    elif not has_rt_mr:
        cursor.execute('ALTER TABLE dog_rabies_tests ADD COLUMN medical_record_id INTEGER REFERENCES dog_medical_records(id)')

    # --- Medical Visits (診察記録) ---

    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS medical_visits (
            id {pk},
            user_id INTEGER,
            dog_id INTEGER,
            medical_record_id INTEGER,
            visit_date DATE NOT NULL,
            visit_time TIME,
            chief_complaint TEXT NOT NULL,
            health_checks_json {json_t},
            mapped_symptoms_json {json_t},
            detailed_memo TEXT,
            body_weight_kg {float_t},
            body_temperature {float_t},
            heart_rate INTEGER,
            respiratory_rate INTEGER,
            diagnosis TEXT,
            treatment TEXT,
            prescription TEXT,
            next_visit_date DATE,
            analysis_result_json {json_t},
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (dog_id) REFERENCES dogs (id),
            FOREIGN KEY (medical_record_id) REFERENCES dog_medical_records (id)
        )
    ''')

    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_visit_dog
        ON medical_visits(dog_id)
    ''')

    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_visit_date
        ON medical_visits(visit_date)
    ''')

    # Search indexes for export applications
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_identification_number
        ON dog_export_applications(identification_number)
    ''')
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_animal_name
        ON dog_export_applications(animal_name)
    ''')
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_application_date
        ON dog_export_applications(application_date)
    ''')

    # --- Genetic Test Results (遺伝子検査結果) ---

    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS dog_genetic_tests (
            id {pk},
            user_id INTEGER,
            dog_id INTEGER,
            medical_record_id INTEGER,
            test_company TEXT,
            test_date DATE,
            registration_number TEXT,
            results_json {json_t},
            color_results_json {json_t},
            overall_risk TEXT DEFAULT 'unknown',
            clear_count INTEGER DEFAULT 0,
            carrier_count INTEGER DEFAULT 0,
            affected_count INTEGER DEFAULT 0,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (dog_id) REFERENCES dogs (id),
            FOREIGN KEY (medical_record_id) REFERENCES dog_medical_records (id)
        )
    ''')

    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_genetic_dog
        ON dog_genetic_tests(dog_id)
    ''')

    # Migrations: Add new columns to existing tables if missing
    try:
        cols = set(_get_columns('dogs'))
        if 'weight' not in cols:
            cursor.execute(f'ALTER TABLE dogs ADD COLUMN weight {float_t}')
        if 'gender' not in cols:
            cursor.execute('ALTER TABLE dogs ADD COLUMN gender TEXT')
        if 'updated_at' not in cols:
            cursor.execute('ALTER TABLE dogs ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP')
    except Exception as e:
        logger.warning(f"Database migration warning (non-fatal): {e}")

    conn.commit()
    conn.close()


# =============================================================================
# User Functions
# =============================================================================

def create_user(email, password, name=None, security_question=None, security_answer=None):
    """Create a new user"""
    conn = get_db()
    cursor = conn.cursor()

    password_hash = generate_password_hash(password)
    security_answer_hash = generate_password_hash(security_answer.strip().lower()) if security_answer else None

    try:
        cursor.execute(
            'INSERT INTO users (email, password_hash, name, security_question, security_answer_hash) VALUES (?, ?, ?, ?, ?)',
            (email.lower(), password_hash, name, security_question, security_answer_hash)
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return {'id': user_id, 'email': email, 'name': name}
    except Exception as e:
        # Handle unique constraint violations across both SQLite and PostgreSQL
        err_msg = str(e).lower()
        is_unique_violation = (
            isinstance(e, sqlite3.IntegrityError)
            or 'unique' in err_msg
            or 'duplicate' in err_msg
        )
        if is_unique_violation:
            conn.close()
            return None  # Email already exists
        conn.close()
        raise


def verify_user(email, password):
    """Verify user credentials"""
    try:
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users WHERE email = ?', (email.lower(),))
        row = cursor.fetchone()
        conn.close()

        if row:
            logging.debug(f"User found: {email}, checking password...")
            if check_password_hash(row['password_hash'], password):
                logging.info(f"Login successful for user: {email}")
                return {
                    'id': row['id'],
                    'email': row['email'],
                    'name': row['name'],
                    'created_at': row['created_at']
                }
            else:
                logging.warning(f"Password mismatch for user: {email}")
        else:
            logging.warning(f"User not found: {email}")
        return None
    except Exception as e:
        logging.error(f"Error verifying user {email}: {e}")
        return None


def get_user_by_id(user_id):
    """Get user by ID"""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('SELECT id, email, name, created_at FROM users WHERE id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return dict(row)
    return None


def get_user_by_email(email):
    """Get user by email (including security question)"""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('SELECT id, email, name, security_question, security_answer_hash FROM users WHERE email = ?',
                   (email.lower(),))
    row = cursor.fetchone()
    conn.close()

    if row:
        return dict(row)
    return None


def verify_security_answer(email, answer):
    """Verify the security answer for a user. Returns user dict if correct, None otherwise."""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('SELECT id, email, name, security_answer_hash FROM users WHERE email = ?', (email.lower(),))
    row = cursor.fetchone()
    conn.close()

    if row and row['security_answer_hash'] and check_password_hash(row['security_answer_hash'], answer.strip().lower()):
        return {'id': row['id'], 'email': row['email'], 'name': row['name']}
    return None


def update_user_password(user_id, new_password):
    """Update a user's password and invalidate all existing sessions for security"""
    conn = get_db()
    cursor = conn.cursor()

    new_hash = generate_password_hash(new_password)
    cursor.execute('UPDATE users SET password_hash = ? WHERE id = ?', (new_hash, user_id))

    # Invalidate all existing sessions for this user (security best practice)
    cursor.execute('DELETE FROM sessions WHERE user_id = ?', (user_id,))
    logger.info(f"Password updated for user {user_id}, invalidated all sessions")

    conn.commit()
    conn.close()
    return cursor.rowcount > 0


def create_reset_token(user_id, hours=1):
    """Create a password reset token (expires in 1 hour by default)"""
    conn = get_db()
    cursor = conn.cursor()

    token = secrets.token_urlsafe(32)
    expires_at = datetime.utcnow().timestamp() + (hours * 60 * 60)

    cursor.execute(
        'INSERT INTO password_reset_tokens (user_id, token, expires_at) VALUES (?, ?, ?)',
        (user_id, token, datetime.utcfromtimestamp(expires_at).strftime('%Y-%m-%d %H:%M:%S'))
    )
    conn.commit()
    conn.close()
    return token


def verify_reset_token(token):
    """Verify a reset token and return user_id if valid"""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM password_reset_tokens
        WHERE token = ? AND NOT used AND expires_at > datetime('now', 'utc')
    ''', (token,))
    row = cursor.fetchone()

    if row:
        # Mark token as used
        cursor.execute('UPDATE password_reset_tokens SET used = TRUE WHERE id = ?', (row['id'],))
        conn.commit()
        conn.close()
        return row['user_id']

    conn.close()
    return None


# =============================================================================
# Session Functions (hashed token storage with backward-compatible migration)
# =============================================================================

def _hash_token(token):
    """SHA-256 hash a session token for secure storage."""
    return hashlib.sha256(token.encode('utf-8')).hexdigest()


def create_session(user_id, days=30):
    """Create a new session token (stores hash only)."""
    conn = get_db()
    cursor = conn.cursor()

    token = secrets.token_urlsafe(32)
    token_hash = _hash_token(token)
    expires_at = datetime.utcnow().timestamp() + (days * 24 * 60 * 60)

    # token column gets the hash (not plaintext) to satisfy UNIQUE constraint.
    # Each call generates a unique random token, so token_hash is always unique
    # even for the same user — multi-device login is safe.
    cursor.execute(
        'INSERT INTO sessions (user_id, token, token_hash, expires_at) VALUES (?, ?, ?, ?)',
        (user_id, token_hash, token_hash,
         datetime.utcfromtimestamp(expires_at).strftime('%Y-%m-%d %H:%M:%S'))
    )
    conn.commit()
    conn.close()

    return token


def verify_session(token):
    """Verify a session token and return user.

    1. Look up by token_hash (new sessions).
    2. Fall back to plaintext token column (legacy sessions) and auto-migrate.
    """
    if not token:
        return None

    conn = get_db()
    cursor = conn.cursor()
    token_hash = _hash_token(token)

    # --- Primary: hash-based lookup ---
    cursor.execute('''
        SELECT s.user_id, u.email, u.name
        FROM sessions s
        JOIN users u ON s.user_id = u.id
        WHERE s.token_hash = ? AND s.expires_at > datetime('now')
    ''', (token_hash,))
    row = cursor.fetchone()

    if row:
        conn.close()
        return {'id': row['user_id'], 'email': row['email'], 'name': row['name']}

    # --- Fallback: legacy plaintext token lookup + auto-migrate ---
    # Only match sessions that haven't been migrated yet (token_hash IS NULL)
    cursor.execute('''
        SELECT s.id AS session_id, s.user_id, u.email, u.name
        FROM sessions s
        JOIN users u ON s.user_id = u.id
        WHERE s.token = ? AND (s.token_hash IS NULL OR s.token_hash = '')
              AND s.expires_at > datetime('now')
    ''', (token,))
    row = cursor.fetchone()

    if row:
        # Migrate: write hash, replace plaintext token with hash to keep UNIQUE constraint
        cursor.execute(
            'UPDATE sessions SET token_hash = ?, token = ? WHERE id = ?',
            (token_hash, token_hash, row['session_id'])
        )
        conn.commit()
        conn.close()
        logger.info(f"Session migrated to hashed storage (user {row['user_id']})")
        return {'id': row['user_id'], 'email': row['email'], 'name': row['name']}

    conn.close()
    return None


def delete_session(token):
    """Delete a session (logout) — handles both hashed and legacy tokens."""
    if not token:
        return
    conn = get_db()
    cursor = conn.cursor()
    token_hash = _hash_token(token)
    # Delete by token_hash (new sessions) or plaintext token (legacy sessions)
    cursor.execute('DELETE FROM sessions WHERE token_hash = ? OR token = ?',
                   (token_hash, token))
    conn.commit()
    conn.close()


# =============================================================================
# Dog Functions
# =============================================================================

def create_dog(user_id, name, breed_id, birth_date=None, weight=None, gender=None, notes=None):
    """Create a new dog"""
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(
            'INSERT INTO dogs (user_id, name, breed_id, birth_date, weight, gender, notes) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (user_id, name, breed_id, birth_date, weight, gender, notes)
        )
        conn.commit()
        dog_id = cursor.lastrowid

        return {'id': dog_id, 'name': name, 'breed_id': breed_id}
    except Exception as e:
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()


def get_dogs_by_user(user_id):
    """Get all dogs for a user"""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT d.*,
               (SELECT COUNT(*) FROM analyses WHERE dog_id = d.id) as analysis_count,
               (SELECT overall_score FROM analyses WHERE dog_id = d.id ORDER BY created_at DESC LIMIT 1) as latest_score
        FROM dogs d
        WHERE d.user_id = ?
        ORDER BY d.created_at DESC
    ''', (user_id,))
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_dog_by_id(dog_id, user_id):
    """Get a specific dog (with user verification)"""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM dogs WHERE id = ? AND user_id = ?', (dog_id, user_id))
    row = cursor.fetchone()
    conn.close()

    if row:
        return dict(row)
    return None


def update_dog(dog_id, user_id, name=None, breed_id=None, birth_date=None, weight=None, gender=None, notes=None):
    """Update a dog's information"""
    conn = get_db()
    cursor = conn.cursor()

    updates = []
    values = []

    if name is not None:
        updates.append('name = ?')
        values.append(name)
    if breed_id is not None:
        updates.append('breed_id = ?')
        values.append(breed_id)
    if birth_date is not None:
        updates.append('birth_date = ?')
        values.append(birth_date)
    if weight is not None:
        updates.append('weight = ?')
        values.append(weight)
    if gender is not None:
        updates.append('gender = ?')
        values.append(gender)
    if notes is not None:
        updates.append('notes = ?')
        values.append(notes)
    updates.append("updated_at = CURRENT_TIMESTAMP")

    if updates:
        values.extend([dog_id, user_id])
        cursor.execute(
            f'UPDATE dogs SET {", ".join(updates)} WHERE id = ? AND user_id = ?',
            values
        )
        conn.commit()

    conn.close()
    return get_dog_by_id(dog_id, user_id)


def delete_dog(dog_id, user_id):
    """Delete a dog and its analyses"""
    conn = get_db()
    cursor = conn.cursor()

    # Delete analyses first
    cursor.execute('DELETE FROM analyses WHERE dog_id = ? AND user_id = ?', (dog_id, user_id))
    # Then delete dog
    cursor.execute('DELETE FROM dogs WHERE id = ? AND user_id = ?', (dog_id, user_id))
    conn.commit()
    conn.close()


# =============================================================================
# Analysis Functions
# =============================================================================

def save_analysis(dog_id, user_id, age_years, has_video, results):
    """Save an analysis result"""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO analyses (
            dog_id, user_id, age_years, has_video,
            overall_score, grade,
            structure_score, coat_score, gait_score, temperament_score,
            results_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        dog_id, user_id, age_years, has_video,
        results.get('overall_score'),
        results.get('grade'),
        results.get('scores', {}).get('structure', {}).get('display'),
        results.get('scores', {}).get('coat_photo', {}).get('display'),
        results.get('scores', {}).get('gait', {}).get('display'),
        results.get('scores', {}).get('temperament', {}).get('display'),
        json.dumps(results, ensure_ascii=False)
    ))
    conn.commit()
    analysis_id = cursor.lastrowid
    conn.close()

    return analysis_id


def get_analyses_by_dog(dog_id, user_id, limit=50):
    """Get analysis history for a dog"""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM analyses
        WHERE dog_id = ? AND user_id = ?
        ORDER BY created_at DESC
        LIMIT ?
    ''', (dog_id, user_id, limit))
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_analysis_by_id(analysis_id, user_id):
    """Get a specific analysis"""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT a.*, d.name as dog_name, d.breed_id
        FROM analyses a
        JOIN dogs d ON a.dog_id = d.id
        WHERE a.id = ? AND a.user_id = ?
    ''', (analysis_id, user_id))
    row = cursor.fetchone()
    conn.close()

    if row:
        result = dict(row)
        if result.get('results_json'):
            try:
                result['results'] = json.loads(result['results_json'])
            except (json.JSONDecodeError, TypeError):
                logger.warning(f"Corrupted results_json for analysis {analysis_id}")
                result['results'] = {}
        return result
    return None


def get_recent_analyses_by_user(user_id, limit=10):
    """Get recent analyses for a user across all dogs"""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT a.*, d.name as dog_name, d.breed_id
        FROM analyses a
        JOIN dogs d ON a.dog_id = d.id
        WHERE a.user_id = ?
        ORDER BY a.created_at DESC
        LIMIT ?
    ''', (user_id, limit))
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


# =============================================================================
# Audit Log Functions
# =============================================================================

def save_audit_log(analysis_id, user_id, dog_id, algorithm_version, model_version,
                   weights_hash, input_type, axis_scores, final_score, grade):
    """Save an audit log entry for an analysis."""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO audit_logs (
            analysis_id, user_id, dog_id,
            algorithm_version, model_version, weights_hash,
            input_type, axis_scores_json, final_score, grade
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        analysis_id, user_id, dog_id,
        algorithm_version, model_version, weights_hash,
        input_type, json.dumps(axis_scores, ensure_ascii=False),
        final_score, grade
    ))
    conn.commit()
    audit_id = cursor.lastrowid
    conn.close()

    return audit_id


def get_audit_logs(analysis_id=None, user_id=None, limit=100):
    """Get audit logs with optional filters."""
    conn = get_db()
    cursor = conn.cursor()

    query = 'SELECT * FROM audit_logs WHERE 1=1'
    params = []

    if analysis_id is not None:
        query += ' AND analysis_id = ?'
        params.append(analysis_id)
    if user_id is not None:
        query += ' AND user_id = ?'
        params.append(user_id)

    query += ' ORDER BY created_at DESC LIMIT ?'
    params.append(limit)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_audit_log_by_analysis(analysis_id):
    """Get the audit log for a specific analysis."""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM audit_logs WHERE analysis_id = ?', (analysis_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        result = dict(row)
        if result.get('axis_scores_json'):
            try:
                result['axis_scores'] = json.loads(result['axis_scores_json'])
            except (json.JSONDecodeError, TypeError):
                logger.warning(f"Corrupted axis_scores_json for analysis {analysis_id}")
                result['axis_scores'] = {}
        return result
    return None


# =============================================================================
# Dog Medical Record Functions (カルテ)
# =============================================================================

def create_medical_record(user_id, data):
    """Create a new dog medical record (カルテ)."""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO dog_medical_records (
            user_id, dog_id, dog_name, breed, color, sex, date_of_birth,
            body_length_cm, body_height_cm, body_weight_kg,
            microchip_number, microchip_date, microchip_location, microchip_type,
            owner_name, owner_address, owner_phone,
            purchase_date, purchase_place, keeping_place,
            veterinary_clinic, veterinarian_name, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        user_id, data.get('dog_id'),
        data.get('dog_name', ''), data.get('breed', ''),
        data.get('color', ''), data.get('sex', ''),
        data.get('date_of_birth'),
        data.get('body_length_cm'), data.get('body_height_cm'), data.get('body_weight_kg'),
        data.get('microchip_number'), data.get('microchip_date'),
        data.get('microchip_location', '頸部'), data.get('microchip_type'),
        data.get('owner_name', ''), data.get('owner_address', ''),
        data.get('owner_phone', ''),
        data.get('purchase_date'), data.get('purchase_place'),
        data.get('keeping_place', ''),
        data.get('veterinary_clinic', ''), data.get('veterinarian_name', ''),
        data.get('notes', ''),
    ))

    record_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return record_id


def get_medical_record(record_id, user_id=None):
    """Get a medical record by ID."""
    conn = get_db()
    cursor = conn.cursor()

    if user_id:
        cursor.execute(
            'SELECT * FROM dog_medical_records WHERE id = ? AND user_id = ?',
            (record_id, user_id))
    else:
        cursor.execute(
            'SELECT * FROM dog_medical_records WHERE id = ?',
            (record_id,))

    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def get_medical_record_by_microchip(microchip_number):
    """Get a medical record by microchip number."""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        'SELECT * FROM dog_medical_records WHERE microchip_number = ?',
        (microchip_number,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def get_medical_records_by_user(user_id, limit=50):
    """Get all medical records for a user."""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM dog_medical_records
        WHERE user_id = ?
        ORDER BY created_at DESC LIMIT ?
    ''', (user_id, limit))

    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_medical_vaccination(record_id, vac_data):
    """Add a vaccination record to a medical record (カルテ)."""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO dog_vaccinations (
            medical_record_id, vaccination_type, vaccination_date,
            expiry_date, vaccine_kind, product_name, manufacturer
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        record_id,
        vac_data.get('vaccination_type', '狂犬病'),
        vac_data.get('vaccination_date', ''),
        vac_data.get('expiry_date'),
        vac_data.get('vaccine_kind', ''),
        vac_data.get('product_name', ''),
        vac_data.get('manufacturer', ''),
    ))

    conn.commit()
    conn.close()


def get_medical_vaccinations(record_id):
    """Get vaccination records for a medical record."""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        'SELECT * FROM dog_vaccinations WHERE medical_record_id = ? ORDER BY vaccination_date DESC',
        (record_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


# =============================================================================
# Dog Export Application Functions (MAFF 別記様式第１号)
# =============================================================================

def create_export_application(user_id, data):
    """Create a new dog export application."""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO dog_export_applications (
            user_id, dog_id,
            applicant_name, applicant_address, applicant_phone,
            applicant_company_name, applicant_company_representative,
            animal_name, breed, color, sex, usage_purpose,
            date_of_birth, age_years, destination_country,
            body_length_cm, body_height_cm, body_weight_kg,
            embarkation_date, embarkation_place, vessel_name, flight_number,
            consignor_name, consignor_address,
            consignee_name, consignee_address,
            keeping_place, purchase_date, scheduled_reentry_date,
            identification_method, identification_number,
            identification_date, identification_location,
            microchip_type, microchip_reader_type,
            laboratory_name, laboratory_address,
            remarks, application_date
        ) VALUES (
            ?, ?,
            ?, ?, ?,
            ?, ?,
            ?, ?, ?, ?, ?,
            ?, ?, ?,
            ?, ?, ?,
            ?, ?, ?, ?,
            ?, ?,
            ?, ?,
            ?, ?, ?,
            ?, ?,
            ?, ?,
            ?, ?,
            ?, ?,
            ?, ?
        )
    ''', (
        user_id, data.get('dog_id'),
        data.get('applicant_name', ''), data.get('applicant_address', ''),
        data.get('applicant_phone', ''),
        data.get('applicant_company_name'), data.get('applicant_company_representative'),
        data.get('animal_name', ''), data.get('breed', ''),
        data.get('color', ''), data.get('sex', ''), data.get('usage_purpose', ''),
        data.get('date_of_birth'), data.get('age_years'),
        data.get('destination_country', ''),
        data.get('body_length_cm'), data.get('body_height_cm'), data.get('body_weight_kg'),
        data.get('embarkation_date'), data.get('embarkation_place'),
        data.get('vessel_name'), data.get('flight_number'),
        data.get('consignor_name', ''), data.get('consignor_address', ''),
        data.get('consignee_name', ''), data.get('consignee_address', ''),
        data.get('keeping_place', ''), data.get('purchase_date'),
        data.get('scheduled_reentry_date'),
        data.get('identification_method', 'マイクロチップ'),
        data.get('identification_number', ''),
        data.get('identification_date'), data.get('identification_location'),
        data.get('microchip_type', 'ISO 11784/11785'),
        data.get('microchip_reader_type'),
        data.get('laboratory_name', ''), data.get('laboratory_address', ''),
        data.get('remarks', ''),
        data.get('application_date', datetime.now().strftime('%Y-%m-%d')),
    ))

    app_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return app_id


def add_export_vaccination(application_id, vac_data):
    """Add a vaccination record to an export application."""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO dog_vaccinations (
            application_id, vaccination_type, vaccination_date,
            expiry_date, vaccine_kind, product_name, manufacturer
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        application_id,
        vac_data.get('vaccination_type', '狂犬病'),
        vac_data.get('vaccination_date', ''),
        vac_data.get('expiry_date'),
        vac_data.get('vaccine_kind', ''),
        vac_data.get('product_name', ''),
        vac_data.get('manufacturer', ''),
    ))

    conn.commit()
    conn.close()


def add_export_rabies_test(application_id, test_data):
    """Add a rabies serological test record (supports dual antibody titers)."""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO dog_rabies_tests (
            application_id, blood_sampling_date, antibody_titer_1, antibody_titer_2, unit
        ) VALUES (?, ?, ?, ?, ?)
    ''', (
        application_id,
        test_data.get('blood_sampling_date', ''),
        test_data.get('antibody_titer_1'),
        test_data.get('antibody_titer_2'),
        test_data.get('unit', 'IU/ml'),
    ))

    conn.commit()
    conn.close()


def get_export_application(application_id, user_id=None):
    """Get an export application by ID."""
    conn = get_db()
    cursor = conn.cursor()

    if user_id:
        cursor.execute(
            'SELECT * FROM dog_export_applications WHERE id = ? AND user_id = ?',
            (application_id, user_id))
    else:
        cursor.execute(
            'SELECT * FROM dog_export_applications WHERE id = ?',
            (application_id,))

    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def get_export_vaccinations(application_id):
    """Get vaccination records for an export application."""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        'SELECT * FROM dog_vaccinations WHERE application_id = ? ORDER BY vaccination_date DESC',
        (application_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_export_rabies_tests(application_id):
    """Get rabies test records for an export application."""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        'SELECT * FROM dog_rabies_tests WHERE application_id = ? ORDER BY blood_sampling_date DESC',
        (application_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_export_applications_by_user(user_id, limit=50):
    """Get all export applications for a user."""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM dog_export_applications
        WHERE user_id = ?
        ORDER BY created_at DESC LIMIT ?
    ''', (user_id, limit))

    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def search_export_by_microchip(microchip_number):
    """Search export applications by microchip number."""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        'SELECT * FROM dog_export_applications WHERE identification_number = ?',
        (microchip_number,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def search_export_applications(animal_name=None, destination_country=None,
                               date_from=None, date_to=None, user_id=None, limit=100):
    """Search export applications with multiple filters.

    Args:
        animal_name: Partial match on animal name (LIKE)
        destination_country: Exact match on destination country
        date_from: Application date start (YYYY-MM-DD)
        date_to: Application date end (YYYY-MM-DD)
        user_id: Filter by user (optional)
        limit: Max results (default 100)
    """
    conn = get_db()
    cursor = conn.cursor()

    query = 'SELECT * FROM dog_export_applications WHERE 1=1'
    params = []

    if user_id is not None:
        query += ' AND user_id = ?'
        params.append(user_id)
    if animal_name:
        query += ' AND animal_name LIKE ?'
        params.append(f'%{animal_name}%')
    if destination_country:
        query += ' AND destination_country = ?'
        params.append(destination_country)
    if date_from:
        query += ' AND application_date >= ?'
        params.append(date_from)
    if date_to:
        query += ' AND application_date <= ?'
        params.append(date_to)

    query += ' ORDER BY application_date DESC LIMIT ?'
    params.append(limit)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def create_export_from_medical_record(user_id, medical_record_id, data):
    """Create an export application from a medical record (カルテ → パスポート auto-transfer).

    Auto-populates applicant info from the medical record's owner data.
    Copies existing vaccinations from the medical record to the application.

    Args:
        user_id: Current user ID
        medical_record_id: Source medical record ID
        data: Additional export-specific data (destination_country, embarkation_date, etc.)

    Returns:
        application_id or None if medical record not found
    """
    record = get_medical_record(medical_record_id, user_id)
    if not record:
        return None

    # Auto-fill from medical record
    export_data = {
        'dog_id': record.get('dog_id'),
        'applicant_name': record.get('owner_name', ''),
        'applicant_address': record.get('owner_address', ''),
        'applicant_phone': record.get('owner_phone', ''),
        'animal_name': record.get('dog_name', ''),
        'breed': record.get('breed', ''),
        'color': record.get('color', ''),
        'sex': record.get('sex', ''),
        'date_of_birth': record.get('date_of_birth'),
        'body_length_cm': record.get('body_length_cm'),
        'body_height_cm': record.get('body_height_cm'),
        'body_weight_kg': record.get('body_weight_kg'),
        'identification_number': record.get('microchip_number', ''),
        'identification_date': record.get('microchip_date'),
        'identification_location': record.get('microchip_location', ''),
        'microchip_type': record.get('microchip_type', ''),
        'keeping_place': record.get('keeping_place', ''),
        'purchase_date': record.get('purchase_date'),
        'consignor_name': record.get('owner_name', ''),
        'consignor_address': record.get('owner_address', ''),
    }
    # Merge caller's data (overrides auto-filled values)
    export_data.update(data)

    # Create the export application
    app_id = create_export_application(user_id, export_data)

    # Link to medical record
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE dog_export_applications SET medical_record_id = ? WHERE id = ?',
        (medical_record_id, app_id))

    # Copy vaccinations from medical record to application
    cursor.execute('''
        INSERT INTO dog_vaccinations (
            application_id, medical_record_id, vaccination_type,
            vaccination_date, expiry_date, vaccine_kind, product_name, manufacturer
        )
        SELECT
            ?, medical_record_id, vaccination_type,
            vaccination_date, expiry_date, vaccine_kind, product_name, manufacturer
        FROM dog_vaccinations
        WHERE medical_record_id = ? AND application_id IS NULL
    ''', (app_id, medical_record_id))

    conn.commit()
    conn.close()
    return app_id


def check_export_required_fields(application_id, user_id=None):
    """Check required fields for an export application.

    Returns a list of missing fields: [{'field': 'key', 'label': 'Japanese label'}]
    Empty list means all required fields are present.
    """
    REQUIRED = {
        'applicant_name': '申請者氏名',
        'animal_name': '動物名',
        'identification_number': 'マイクロチップ番号',
        'destination_country': '仕向国',
        'embarkation_date': '搭載予定日',
    }

    app = get_export_application(application_id, user_id)
    if not app:
        return [{'field': 'application', 'label': '申請が見つかりません'}]

    missing = []
    for field, label in REQUIRED.items():
        if not app.get(field):
            missing.append({'field': field, 'label': label})

    # Check rabies vaccination exists
    vaccinations = get_export_vaccinations(application_id)
    has_rabies = any(v.get('vaccination_type') == '狂犬病' for v in vaccinations)
    if not has_rabies:
        missing.append({'field': 'rabies_vaccination', 'label': '狂犬病予防接種'})

    # Check rabies antibody test exists
    tests = get_export_rabies_tests(application_id)
    if not tests:
        missing.append({'field': 'rabies_test', 'label': '狂犬病抗体検査'})

    return missing


def get_export_full_data(application_id, user_id=None):
    """Get complete export application data including medical record, vaccinations, and tests.

    Returns a merged dict with all data needed for PDF generation.
    """
    app = get_export_application(application_id, user_id)
    if not app:
        return None

    # If linked to a medical record, merge that data
    if app.get('medical_record_id'):
        record = get_medical_record(app['medical_record_id'])
        if record:
            # Medical record fields supplement (don't override) application data
            for key in ('dog_name', 'breed', 'color', 'sex', 'date_of_birth',
                        'body_length_cm', 'body_height_cm', 'body_weight_kg',
                        'microchip_number', 'microchip_date', 'microchip_location',
                        'microchip_type', 'owner_name', 'owner_address', 'owner_phone',
                        'purchase_date', 'keeping_place'):
                if not app.get(key) and record.get(key):
                    app[key] = record[key]

    app['vaccinations'] = get_export_vaccinations(application_id)
    app['rabies_tests'] = get_export_rabies_tests(application_id)

    return app


# =============================================================================
# Medical Visit Functions (診察記録)
# =============================================================================

def create_medical_visit(user_id, data):
    """Create a new medical visit record.

    Args:
        user_id: Current user ID
        data: Visit data dict with keys:
            - dog_id: Dog ID
            - visit_date: Visit date (YYYY-MM-DD)
            - chief_complaint: Main complaint
            - health_checks: Dict of {category: [checked_items]} (stored as JSON)
            - mapped_symptoms: List of English symptom IDs (for symptom checker)
            - detailed_memo: Detailed notes
            - body_weight_kg, body_temperature, heart_rate, respiratory_rate: Vitals
            - analysis_result: Symptom analysis result (stored as JSON)

    Returns:
        visit_id

    Raises:
        ValueError: If dog does not belong to user
    """
    conn = get_db()
    cursor = conn.cursor()

    # Verify dog ownership
    dog_id = data.get('dog_id')
    if dog_id:
        cursor.execute('SELECT id FROM dogs WHERE id = ? AND user_id = ?', (dog_id, user_id))
        if not cursor.fetchone():
            conn.close()
            raise ValueError(f"Dog {dog_id} does not belong to user {user_id}")

    health_checks = data.get('health_checks')
    if isinstance(health_checks, dict):
        health_checks = json.dumps(health_checks, ensure_ascii=False)

    mapped_symptoms = data.get('mapped_symptoms')
    if isinstance(mapped_symptoms, list):
        mapped_symptoms = json.dumps(mapped_symptoms, ensure_ascii=False)

    analysis_result = data.get('analysis_result')
    if isinstance(analysis_result, dict):
        analysis_result = json.dumps(analysis_result, ensure_ascii=False)

    cursor.execute('''
        INSERT INTO medical_visits (
            user_id, dog_id, medical_record_id,
            visit_date, visit_time, chief_complaint,
            health_checks_json, mapped_symptoms_json, detailed_memo,
            body_weight_kg, body_temperature, heart_rate, respiratory_rate,
            diagnosis, treatment, prescription, next_visit_date,
            analysis_result_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        user_id, data.get('dog_id'), data.get('medical_record_id'),
        data.get('visit_date', ''), data.get('visit_time'),
        data.get('chief_complaint', ''),
        health_checks, mapped_symptoms, data.get('detailed_memo', ''),
        data.get('body_weight_kg'), data.get('body_temperature'),
        data.get('heart_rate'), data.get('respiratory_rate'),
        data.get('diagnosis'), data.get('treatment'),
        data.get('prescription'), data.get('next_visit_date'),
        analysis_result,
    ))

    visit_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return visit_id


def get_medical_visit(visit_id, user_id=None):
    """Get a medical visit by ID."""
    conn = get_db()
    cursor = conn.cursor()

    if user_id:
        cursor.execute(
            'SELECT * FROM medical_visits WHERE id = ? AND user_id = ?',
            (visit_id, user_id))
    else:
        cursor.execute(
            'SELECT * FROM medical_visits WHERE id = ?',
            (visit_id,))

    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    result = dict(row)
    for json_field, target, default in [
        ('health_checks_json', 'health_checks', {}),
        ('mapped_symptoms_json', 'mapped_symptoms', []),
        ('analysis_result_json', 'analysis_result', {}),
    ]:
        if result.get(json_field):
            try:
                result[target] = json.loads(result[json_field])
            except (json.JSONDecodeError, TypeError):
                logger.warning(f"Corrupted {json_field} in medical visit")
                result[target] = default
    return result


def get_medical_visits_by_dog(dog_id, user_id=None, limit=50):
    """Get visit history for a dog."""
    conn = get_db()
    cursor = conn.cursor()

    if user_id:
        cursor.execute('''
            SELECT * FROM medical_visits
            WHERE dog_id = ? AND user_id = ?
            ORDER BY visit_date DESC LIMIT ?
        ''', (dog_id, user_id, limit))
    else:
        cursor.execute('''
            SELECT * FROM medical_visits
            WHERE dog_id = ?
            ORDER BY visit_date DESC LIMIT ?
        ''', (dog_id, limit))

    rows = cursor.fetchall()
    conn.close()

    results = []
    for row in rows:
        r = dict(row)
        if r.get('health_checks_json'):
            r['health_checks'] = json.loads(r['health_checks_json'])
        if r.get('mapped_symptoms_json'):
            r['mapped_symptoms'] = json.loads(r['mapped_symptoms_json'])
        results.append(r)
    return results


# =============================================================================
# Genetic Test Functions (遺伝子検査)
# =============================================================================

def save_genetic_test(user_id, data):
    """Save a genetic test result.

    Args:
        user_id: Current user ID
        data: Dict with keys:
            - dog_id: Dog ID
            - medical_record_id: Linked medical record (optional)
            - test_company: Testing lab name
            - test_date: Test date
            - registration_number: Registration/microchip number
            - health_tests: List of gene test results
            - color_tests: List of color locus results
            - notes: Free text notes

    Returns:
        genetic_test_id
    """
    conn = get_db()
    cursor = conn.cursor()

    health_tests = data.get('health_tests', [])
    color_tests = data.get('color_tests', [])

    clear_count = sum(1 for t in health_tests if t.get('result') == 'clear')
    carrier_count = sum(1 for t in health_tests if t.get('result') == 'carrier')
    affected_count = sum(1 for t in health_tests if t.get('result') == 'affected')

    if affected_count > 0:
        overall_risk = 'high'
    elif carrier_count > 0:
        overall_risk = 'medium'
    elif health_tests:
        overall_risk = 'low'
    else:
        overall_risk = 'unknown'

    cursor.execute('''
        INSERT INTO dog_genetic_tests (
            user_id, dog_id, medical_record_id,
            test_company, test_date, registration_number,
            results_json, color_results_json,
            overall_risk, clear_count, carrier_count, affected_count,
            notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        user_id, data.get('dog_id'), data.get('medical_record_id'),
        data.get('test_company', ''), data.get('test_date'),
        data.get('registration_number'),
        json.dumps(health_tests, ensure_ascii=False),
        json.dumps(color_tests, ensure_ascii=False),
        overall_risk, clear_count, carrier_count, affected_count,
        data.get('notes', ''),
    ))

    test_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return test_id


def get_genetic_test(test_id, user_id=None):
    """Get a genetic test result by ID."""
    conn = get_db()
    cursor = conn.cursor()

    if user_id:
        cursor.execute(
            'SELECT * FROM dog_genetic_tests WHERE id = ? AND user_id = ?',
            (test_id, user_id))
    else:
        cursor.execute(
            'SELECT * FROM dog_genetic_tests WHERE id = ?',
            (test_id,))

    row = cursor.fetchone()
    conn.close()

    if not row:
        return None
    result = dict(row)
    for json_field, target, default in [
        ('results_json', 'health_tests', {}),
        ('color_results_json', 'color_tests', {}),
    ]:
        if result.get(json_field):
            try:
                result[target] = json.loads(result[json_field])
            except (json.JSONDecodeError, TypeError):
                logger.warning(f"Corrupted {json_field} in genetic test")
                result[target] = default
    return result


def get_genetic_tests_by_dog(dog_id, user_id=None, limit=50):
    """Get genetic test history for a dog."""
    conn = get_db()
    cursor = conn.cursor()

    if user_id:
        cursor.execute('''
            SELECT * FROM dog_genetic_tests
            WHERE dog_id = ? AND user_id = ?
            ORDER BY created_at DESC LIMIT ?
        ''', (dog_id, user_id, limit))
    else:
        cursor.execute('''
            SELECT * FROM dog_genetic_tests
            WHERE dog_id = ?
            ORDER BY created_at DESC LIMIT ?
        ''', (dog_id, limit))

    rows = cursor.fetchall()
    conn.close()

    results = []
    for row in rows:
        r = dict(row)
        if r.get('results_json'):
            r['health_tests'] = json.loads(r['results_json'])
        if r.get('color_results_json'):
            r['color_tests'] = json.loads(r['color_results_json'])
        results.append(r)
    return results


def get_genetic_tests_by_user(user_id, limit=50):
    """Get all genetic tests for a user."""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT gt.*, d.name as dog_name, d.breed_id
        FROM dog_genetic_tests gt
        LEFT JOIN dogs d ON gt.dog_id = d.id
        WHERE gt.user_id = ?
        ORDER BY gt.created_at DESC LIMIT ?
    ''', (user_id, limit))

    rows = cursor.fetchall()
    conn.close()

    results = []
    for row in rows:
        r = dict(row)
        if r.get('results_json'):
            r['health_tests'] = json.loads(r['results_json'])
        if r.get('color_results_json'):
            r['color_tests'] = json.loads(r['color_results_json'])
        results.append(r)
    return results


def seed_admin_user():
    """Create or update admin user from environment variables.

    Reads ADMIN_BOOTSTRAP_EMAIL, ADMIN_PASSWORD, and optionally ADMIN_NAME from env.
    Runs on every startup so the admin account persists even when the DB
    is recreated (e.g. Render ephemeral filesystem).
    Always updates the password to match the current env var.
    """
    admin_email = os.environ.get('ADMIN_BOOTSTRAP_EMAIL', '').strip().lower()
    admin_password = os.environ.get('ADMIN_PASSWORD', '').strip()
    admin_name = os.environ.get('ADMIN_NAME', '').strip() or 'Admin'

    if not admin_email or not admin_password:
        logger.info("No ADMIN_BOOTSTRAP_EMAIL/ADMIN_PASSWORD env vars configured - skipping admin seed")
        return

    logger.info(f"Seeding admin user: {admin_email} (password length: {len(admin_password)})")

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users WHERE email = ?', (admin_email,))
    existing = cursor.fetchone()

    password_hash = generate_password_hash(admin_password)
    security_answer_hash = generate_password_hash(admin_email)

    if existing:
        # Update password to match current env var
        cursor.execute(
            'UPDATE users SET password_hash = ?, name = ? WHERE email = ?',
            (password_hash, admin_name, admin_email)
        )
        conn.commit()
        conn.close()
        logger.info(f"Admin user updated: {admin_email}")
        return

    try:
        cursor.execute(
            'INSERT INTO users (email, password_hash, name, security_question, security_answer_hash) VALUES (?, ?, ?, ?, ?)',
            (admin_email, password_hash, admin_name, 'Admin Account', security_answer_hash)
        )
        conn.commit()
        logger.info(f"Admin user created: {admin_email}")
    except Exception as e:
        # sqlite3.IntegrityError for SQLite, psycopg2.errors.UniqueViolation for PG
        if 'UNIQUE' in str(e).upper() or 'unique' in str(e).lower() or 'duplicate' in str(e).lower():
            logger.warning(f"Admin user creation failed (already exists): {admin_email}")
        else:
            logger.error(f"Admin user creation failed: {e}")
    finally:
        conn.close()


# Initialize database on import
init_db()
seed_admin_user()
