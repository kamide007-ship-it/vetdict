"""
dog_export_db.py
犬の輸出検査申請書データベース統合モジュール

【概要】
狂犬病予防法及び家畜伝染病予防法に基づく犬の輸出検査申請書のデータを
SQLiteデータベースで管理するためのモジュールです。

【主な機能】
1. 申請メイン情報の管理
2. 予防接種履歴の管理（複数回対応）
3. 狂犬病抗体検査履歴の管理
4. マイクロチップ番号による個体識別
5. 申請データの検索・取得

【使い方】

■ステップ1: 既存DBに統合する場合
-----------------------------------------
from dog_export_db import DogExportDB

# 既存のデータベースファイルを指定
db = DogExportDB("your_existing_database.db")

# テーブルを作成（既存テーブルには影響なし）
db.create_tables()


■ステップ2: 新規申請を追加
-----------------------------------------
# 申請データを辞書形式で準備
application_data = {
    'applicant_name': '山田太郎',
    'applicant_address': '東京都渋谷区...',
    'applicant_phone': '03-1234-5678',
    'animal_name': 'ポチ',
    'breed': '柴犬',
    'color': '赤',
    'sex': 'オス',
    'date_of_birth': '2022-05-15',
    'identification_number': '392143000012345',  # マイクロチップ番号
    'destination_country': 'アメリカ合衆国',
    # ... その他のフィールド（必要に応じて）
}

# データベースに追加
app_id = db.add_application(application_data)
print(f"申請ID {app_id} を追加しました")


■ステップ3: 予防接種履歴を追加
-----------------------------------------
# 狂犬病予防接種
rabies_vaccine = {
    'vaccination_type': '狂犬病',
    'vaccination_date': '2024-10-01',
    'expiry_date': '2025-10-01',
    'vaccine_kind': '不活化ワクチン',
    'product_name': 'ラビエスワクチン',
    'manufacturer': 'XYZ製薬'
}
db.add_vaccination(app_id, rabies_vaccine)

# その他の予防接種
other_vaccine = {
    'vaccination_type': 'その他',
    'vaccination_date': '2024-09-15',
    'expiry_date': '2025-09-15',
    'vaccine_kind': '混合ワクチン',
    'product_name': '5種混合ワクチン',
    'manufacturer': 'ABC動物薬品'
}
db.add_vaccination(app_id, other_vaccine)


■ステップ4: 狂犬病抗体検査を追加
-----------------------------------------
rabies_test = {
    'blood_sampling_date': '2024-10-15',
    'antibody_titer_1': 0.8,
    'antibody_titer_2': 0.9,
    'unit': 'IU/ml'
}
db.add_rabies_test(app_id, rabies_test)


■ステップ5: データを取得
-----------------------------------------
# IDで取得
application = db.get_application_by_id(app_id)
print(application['animal_name'])

# マイクロチップ番号で取得
app_by_chip = db.get_application_by_microchip('392143000012345')
if app_by_chip:
    print(f"{app_by_chip['animal_name']} を発見")

# 予防接種履歴を取得
vaccinations = db.get_vaccinations(app_id)
for vac in vaccinations:
    print(f"{vac['vaccination_type']}: {vac['vaccination_date']}")

# 抗体検査履歴を取得
tests = db.get_rabies_tests(app_id)
for test in tests:
    print(f"採血日: {test['blood_sampling_date']}, 抗体価: {test['antibody_titer_1']}")


■ステップ6: 申請を検索
-----------------------------------------
# 動物名で検索（部分一致）
results = db.search_applications(animal_name='ポチ')

# 仕向国で検索
results = db.search_applications(destination_country='アメリカ合衆国')

# 期間で検索
results = db.search_applications(
    date_from='2024-01-01',
    date_to='2024-12-31'
)

# 複合検索
results = db.search_applications(
    animal_name='柴',
    destination_country='アメリカ合衆国',
    date_from='2024-01-01'
)

for app in results:
    print(f"{app['animal_name']} - {app['destination_country']}")


■ShowDog AIとの連携例
-----------------------------------------
# ShowDogの既存DBに統合
showdog_db = DogExportDB("showdog_production.db")
showdog_db.create_tables()

# AI評価結果と輸出検査を紐付け
# マイクロチップ番号で個体を特定
export_app = showdog_db.get_application_by_microchip('392143000012345')
if export_app:
    # ShowDogの評価データと連携
    print(f"輸出申請あり: {export_app['destination_country']}向け")
    # B2B監査ログに記録可能


■FastAPI連携例
-----------------------------------------
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
db = DogExportDB("dog_export.db")
db.create_tables()

class ApplicationCreate(BaseModel):
    applicant_name: str
    animal_name: str
    identification_number: str
    # ... その他のフィールド

@app.post("/applications/")
def create_application(data: ApplicationCreate):
    app_id = db.add_application(data.dict())
    return {"application_id": app_id}

@app.get("/applications/{microchip}")
def get_by_microchip(microchip: str):
    app = db.get_application_by_microchip(microchip)
    if not app:
        raise HTTPException(status_code=404, detail="申請が見つかりません")
    return app


【データベーススキーマ】
-------------------------
1. dog_export_applications (申請メイン)
   - 申請者情報（氏名、住所、電話番号、法人情報）
   - 動物基本情報（名前、品種、毛色、性別、生年月日など）
   - 体格情報（体長、体高、体重）
   - 輸送情報（搭載日、搭載地、便名など）
   - 個体識別情報（マイクロチップ番号、識別方法など）

2. dog_vaccinations (予防接種履歴)
   - 予防接種タイプ（狂犬病/その他）
   - 接種日、有効期限
   - ワクチン情報（種類、製品名、製造会社）

3. dog_rabies_tests (狂犬病抗体検査)
   - 採血日
   - 抗体価（2つまで記録可能）
   - 検査単位（デフォルト: IU/ml）

【注意事項】
-------------------------
- identification_number（マイクロチップ番号）はUNIQUE制約あり
- 予防接種と抗体検査は申請に紐づく（外部キー制約）
- 申請削除時は関連する予防接種・検査も自動削除（CASCADE）
"""

import sqlite3
from typing import Dict, List, Optional


class DogExportDB:
    """犬の輸出検査申請書データベース管理クラス"""

    def __init__(self, db_path: str = "dog_export.db"):
        """
        初期化

        Args:
            db_path: データベースファイルのパス（既存DBのパスを指定）
        """
        self.db_path = db_path
        self.conn = None

    def connect(self):
        """データベース接続"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row  # 列名でアクセス可能に

    def close(self):
        """データベース接続を閉じる"""
        if self.conn:
            self.conn.close()

    def create_tables(self):
        """
        テーブル作成（既存DBに新規テーブルを追加）
        既にテーブルが存在する場合はスキップ
        """
        self.connect()
        cursor = self.conn.cursor()

        # 1. 申請メイン情報テーブル
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS dog_export_applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            -- 申請者情報
            applicant_name TEXT NOT NULL,
            applicant_address TEXT,
            applicant_phone TEXT,
            applicant_company_name TEXT,
            applicant_company_representative TEXT,

            -- 動物基本情報
            animal_species TEXT DEFAULT '犬',
            animal_quantity INTEGER DEFAULT 1,
            animal_name TEXT NOT NULL,
            breed TEXT,
            color TEXT,
            sex TEXT CHECK(sex IN ('オス', 'メス', '不明')),
            usage_purpose TEXT,
            date_of_birth DATE,
            age_years INTEGER,
            destination_country TEXT,

            -- 体格情報
            body_length_cm REAL,
            body_height_cm REAL,
            body_weight_kg REAL,

            -- 輸送情報
            embarkation_date DATE,
            embarkation_place TEXT,
            vessel_name TEXT,
            flight_number TEXT,

            -- 関係者情報
            consignor_name TEXT,
            consignor_address TEXT,
            consignee_name TEXT,
            consignee_address TEXT,
            keeping_place TEXT,

            -- 購入・帰国情報
            purchase_date DATE,
            scheduled_reentry_date DATE,

            -- 個体識別情報
            identification_method TEXT,
            identification_number TEXT UNIQUE,
            identification_date DATE,
            identification_location TEXT,
            microchip_type TEXT,
            microchip_reader_type TEXT,

            -- 検査機関情報
            laboratory_name TEXT,
            laboratory_address TEXT,

            -- メタ情報
            remarks TEXT,
            application_date DATE DEFAULT CURRENT_DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # 2. 予防接種履歴テーブル（1頭の犬に複数回の接種が可能）
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS dog_vaccinations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            application_id INTEGER NOT NULL,

            vaccination_type TEXT NOT NULL CHECK(vaccination_type IN ('狂犬病', 'その他')),
            vaccination_date DATE NOT NULL,
            expiry_date DATE,
            vaccine_kind TEXT,
            product_name TEXT,
            manufacturer TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (application_id) REFERENCES dog_export_applications(id) ON DELETE CASCADE
        )
        """)

        # 3. 狂犬病抗体検査履歴テーブル
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS dog_rabies_tests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            application_id INTEGER NOT NULL,

            blood_sampling_date DATE NOT NULL,
            antibody_titer_1 REAL,
            antibody_titer_2 REAL,
            unit TEXT DEFAULT 'IU/ml',

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (application_id) REFERENCES dog_export_applications(id) ON DELETE CASCADE
        )
        """)

        # インデックス作成（検索高速化）
        cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_identification_number
        ON dog_export_applications(identification_number)
        """)

        cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_animal_name
        ON dog_export_applications(animal_name)
        """)

        cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_application_date
        ON dog_export_applications(application_date)
        """)

        self.conn.commit()
        self.close()

    def add_application(self, data: Dict) -> int:
        """
        新規申請を追加

        Args:
            data: 申請データ（辞書形式）

        Returns:
            追加された申請のID

        使用例:
            application_data = {
                'applicant_name': '山田太郎',
                'animal_name': 'ポチ',
                'identification_number': '392143000012345',
                # ... その他のフィールド
            }
            app_id = db.add_application(application_data)
        """
        self.connect()
        cursor = self.conn.cursor()

        # メインテーブルに挿入
        cursor.execute("""
        INSERT INTO dog_export_applications (
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
            :applicant_name, :applicant_address, :applicant_phone,
            :applicant_company_name, :applicant_company_representative,
            :animal_name, :breed, :color, :sex, :usage_purpose,
            :date_of_birth, :age_years, :destination_country,
            :body_length_cm, :body_height_cm, :body_weight_kg,
            :embarkation_date, :embarkation_place, :vessel_name, :flight_number,
            :consignor_name, :consignor_address,
            :consignee_name, :consignee_address,
            :keeping_place, :purchase_date, :scheduled_reentry_date,
            :identification_method, :identification_number,
            :identification_date, :identification_location,
            :microchip_type, :microchip_reader_type,
            :laboratory_name, :laboratory_address,
            :remarks, :application_date
        )
        """, data)

        application_id = cursor.lastrowid
        self.conn.commit()
        self.close()

        return application_id

    def add_vaccination(self, application_id: int, vaccination_data: Dict):
        """
        予防接種履歴を追加

        Args:
            application_id: 申請ID
            vaccination_data: 予防接種データ

        使用例:
            vaccine = {
                'vaccination_type': '狂犬病',
                'vaccination_date': '2024-10-01',
                'expiry_date': '2025-10-01',
                'vaccine_kind': '不活化ワクチン',
                'product_name': 'ラビエスワクチン',
                'manufacturer': 'XYZ製薬'
            }
            db.add_vaccination(app_id, vaccine)
        """
        self.connect()
        cursor = self.conn.cursor()

        vaccination_data['application_id'] = application_id

        cursor.execute("""
        INSERT INTO dog_vaccinations (
            application_id, vaccination_type, vaccination_date,
            expiry_date, vaccine_kind, product_name, manufacturer
        ) VALUES (
            :application_id, :vaccination_type, :vaccination_date,
            :expiry_date, :vaccine_kind, :product_name, :manufacturer
        )
        """, vaccination_data)

        self.conn.commit()
        self.close()

    def add_rabies_test(self, application_id: int, test_data: Dict):
        """
        狂犬病抗体検査履歴を追加

        Args:
            application_id: 申請ID
            test_data: 検査データ

        使用例:
            test = {
                'blood_sampling_date': '2024-10-15',
                'antibody_titer_1': 0.8,
                'antibody_titer_2': 0.9,
                'unit': 'IU/ml'
            }
            db.add_rabies_test(app_id, test)
        """
        self.connect()
        cursor = self.conn.cursor()

        test_data['application_id'] = application_id

        cursor.execute("""
        INSERT INTO dog_rabies_tests (
            application_id, blood_sampling_date,
            antibody_titer_1, antibody_titer_2, unit
        ) VALUES (
            :application_id, :blood_sampling_date,
            :antibody_titer_1, :antibody_titer_2, :unit
        )
        """, test_data)

        self.conn.commit()
        self.close()

    def get_application_by_id(self, application_id: int) -> Optional[Dict]:
        """
        IDで申請を取得

        Args:
            application_id: 申請ID

        Returns:
            申請データ（辞書形式）または None

        使用例:
            app = db.get_application_by_id(1)
            if app:
                print(app['animal_name'])
        """
        self.connect()
        cursor = self.conn.cursor()

        cursor.execute("""
        SELECT * FROM dog_export_applications WHERE id = ?
        """, (application_id,))

        row = cursor.fetchone()
        self.close()

        if row:
            return dict(row)
        return None

    def get_application_by_microchip(self, microchip_number: str) -> Optional[Dict]:
        """
        マイクロチップ番号で申請を取得

        Args:
            microchip_number: マイクロチップ番号

        Returns:
            申請データ（辞書形式）または None

        使用例:
            app = db.get_application_by_microchip('392143000012345')
            if app:
                print(f"{app['animal_name']} を発見")
        """
        self.connect()
        cursor = self.conn.cursor()

        cursor.execute("""
        SELECT * FROM dog_export_applications
        WHERE identification_number = ?
        """, (microchip_number,))

        row = cursor.fetchone()
        self.close()

        if row:
            return dict(row)
        return None

    def get_vaccinations(self, application_id: int) -> List[Dict]:
        """
        申請IDに紐づく予防接種履歴を取得

        Args:
            application_id: 申請ID

        Returns:
            予防接種履歴のリスト（新しい順）

        使用例:
            vaccinations = db.get_vaccinations(app_id)
            for vac in vaccinations:
                print(f"{vac['vaccination_type']}: {vac['vaccination_date']}")
        """
        self.connect()
        cursor = self.conn.cursor()

        cursor.execute("""
        SELECT * FROM dog_vaccinations
        WHERE application_id = ?
        ORDER BY vaccination_date DESC
        """, (application_id,))

        rows = cursor.fetchall()
        self.close()

        return [dict(row) for row in rows]

    def get_rabies_tests(self, application_id: int) -> List[Dict]:
        """
        申請IDに紐づく狂犬病抗体検査履歴を取得

        Args:
            application_id: 申請ID

        Returns:
            検査履歴のリスト（新しい順）

        使用例:
            tests = db.get_rabies_tests(app_id)
            for test in tests:
                print(f"採血日: {test['blood_sampling_date']}")
                print(f"抗体価: {test['antibody_titer_1']} {test['unit']}")
        """
        self.connect()
        cursor = self.conn.cursor()

        cursor.execute("""
        SELECT * FROM dog_rabies_tests
        WHERE application_id = ?
        ORDER BY blood_sampling_date DESC
        """, (application_id,))

        rows = cursor.fetchall()
        self.close()

        return [dict(row) for row in rows]

    def search_applications(self,
                          animal_name: Optional[str] = None,
                          destination_country: Optional[str] = None,
                          date_from: Optional[str] = None,
                          date_to: Optional[str] = None) -> List[Dict]:
        """
        申請を検索

        Args:
            animal_name: 動物名（部分一致）
            destination_country: 仕向国（完全一致）
            date_from: 申請日（開始）YYYY-MM-DD形式
            date_to: 申請日（終了）YYYY-MM-DD形式

        Returns:
            検索結果のリスト（新しい順）

        使用例:
            # 動物名で検索
            results = db.search_applications(animal_name='ポチ')

            # 仕向国で検索
            results = db.search_applications(destination_country='アメリカ合衆国')

            # 期間指定検索
            results = db.search_applications(
                date_from='2024-01-01',
                date_to='2024-12-31'
            )

            # 複合検索
            results = db.search_applications(
                animal_name='柴',
                destination_country='アメリカ合衆国',
                date_from='2024-01-01'
            )
        """
        self.connect()
        cursor = self.conn.cursor()

        query = "SELECT * FROM dog_export_applications WHERE 1=1"
        params = []

        if animal_name:
            query += " AND animal_name LIKE ?"
            params.append(f"%{animal_name}%")

        if destination_country:
            query += " AND destination_country = ?"
            params.append(destination_country)

        if date_from:
            query += " AND application_date >= ?"
            params.append(date_from)

        if date_to:
            query += " AND application_date <= ?"
            params.append(date_to)

        query += " ORDER BY application_date DESC"

        cursor.execute(query, params)
        rows = cursor.fetchall()
        self.close()

        return [dict(row) for row in rows]


# ========================================
# 使用例（実行可能なサンプルコード）
# ========================================

def example_usage():
    """
    実際の使用例
    このスクリプトを実行するとサンプルデータが作成されます
    """

    print("=== 犬の輸出検査申請書データベース 使用例 ===\n")

    # 1. データベース初期化
    print("[1] データベース初期化")
    db = DogExportDB("dog_export_example.db")  # ← 既存DBのパスに変更
    db.create_tables()
    print("✓ テーブルを作成しました\n")

    # 2. サンプル申請データを作成
    print("[2] 新規申請を追加")
    application_data = {
        'applicant_name': '山田太郎',
        'applicant_address': '東京都渋谷区神宮前1-2-3',
        'applicant_phone': '03-1234-5678',
        'applicant_company_name': None,
        'applicant_company_representative': None,
        'animal_name': 'ポチ',
        'breed': '柴犬',
        'color': '赤',
        'sex': 'オス',
        'usage_purpose': 'ペット',
        'date_of_birth': '2022-05-15',
        'age_years': 2,
        'destination_country': 'アメリカ合衆国',
        'body_length_cm': 45.0,
        'body_height_cm': 40.0,
        'body_weight_kg': 10.5,
        'embarkation_date': '2024-12-20',
        'embarkation_place': '成田国際空港',
        'vessel_name': None,
        'flight_number': 'NH001',
        'consignor_name': '山田太郎',
        'consignor_address': '東京都渋谷区神宮前1-2-3',
        'consignee_name': 'John Smith',
        'consignee_address': '123 Main St, New York, NY 10001, USA',
        'keeping_place': '自宅',
        'purchase_date': '2022-06-01',
        'scheduled_reentry_date': None,
        'identification_method': 'マイクロチップ',
        'identification_number': '392143000012345',
        'identification_date': '2022-06-01',
        'identification_location': '頸部',
        'microchip_type': 'ISO 11784/11785準拠',
        'microchip_reader_type': 'ユニバーサルリーダー',
        'laboratory_name': '指定検査機関ABC',
        'laboratory_address': '東京都港区赤坂1-2-3',
        'remarks': '特になし',
        'application_date': '2024-11-01'
    }

    app_id = db.add_application(application_data)
    print(f"✓ 申請ID {app_id} を追加しました")
    print(f"  犬の名前: {application_data['animal_name']}")
    print(f"  マイクロチップ: {application_data['identification_number']}\n")

    # 3. 狂犬病予防接種を追加
    print("[3] 狂犬病予防接種を追加")
    rabies_vaccine = {
        'vaccination_type': '狂犬病',
        'vaccination_date': '2024-10-01',
        'expiry_date': '2025-10-01',
        'vaccine_kind': '不活化ワクチン',
        'product_name': 'ラビエスワクチン',
        'manufacturer': 'XYZ製薬'
    }
    db.add_vaccination(app_id, rabies_vaccine)
    print("✓ 狂犬病ワクチン接種記録を追加しました")
    print(f"  接種日: {rabies_vaccine['vaccination_date']}\n")

    # 4. その他の予防接種を追加
    print("[4] その他の予防接種を追加")
    other_vaccine = {
        'vaccination_type': 'その他',
        'vaccination_date': '2024-09-15',
        'expiry_date': '2025-09-15',
        'vaccine_kind': '混合ワクチン',
        'product_name': '5種混合ワクチン',
        'manufacturer': 'ABC動物薬品'
    }
    db.add_vaccination(app_id, other_vaccine)
    print("✓ 混合ワクチン接種記録を追加しました\n")

    # 5. 狂犬病抗体検査を追加
    print("[5] 狂犬病抗体検査結果を追加")
    rabies_test = {
        'blood_sampling_date': '2024-10-15',
        'antibody_titer_1': 0.8,
        'antibody_titer_2': 0.9,
        'unit': 'IU/ml'
    }
    db.add_rabies_test(app_id, rabies_test)
    print("✓ 抗体検査結果を追加しました")
    print(f"  採血日: {rabies_test['blood_sampling_date']}")
    print(f"  抗体価: {rabies_test['antibody_titer_1']} {rabies_test['unit']}\n")

    # 6. データ取得の例
    print("[6] データを取得")

    # IDで取得
    application = db.get_application_by_id(app_id)
    print(f"✓ 申請データ取得: {application['animal_name']} ({application['breed']})")

    # 予防接種履歴
    vaccinations = db.get_vaccinations(app_id)
    print(f"✓ 予防接種履歴: {len(vaccinations)}件")
    for vac in vaccinations:
        print(f"  - {vac['vaccination_type']}: {vac['vaccination_date']}")

    # 抗体検査履歴
    tests = db.get_rabies_tests(app_id)
    print(f"✓ 抗体検査履歴: {len(tests)}件")
    for test in tests:
        print(f"  - 採血日: {test['blood_sampling_date']}, 抗体価: {test['antibody_titer_1']}\n")

    # 7. マイクロチップで検索
    print("[7] マイクロチップ番号で検索")
    app_by_chip = db.get_application_by_microchip('392143000012345')
    if app_by_chip:
        print(f"✓ マイクロチップ検索成功: {app_by_chip['animal_name']} を発見")
        print(f"  仕向国: {app_by_chip['destination_country']}\n")

    # 8. 検索の例
    print("[8] 申請を検索")
    results = db.search_applications(animal_name='ポチ')
    print(f"✓ 「ポチ」の検索結果: {len(results)}件")

    results = db.search_applications(destination_country='アメリカ合衆国')
    print(f"✓ 「アメリカ合衆国」向け: {len(results)}件\n")

    print("=== 完了 ===")
    print(f"データベースファイル: {db.db_path}")


if __name__ == "__main__":
    # このスクリプトを実行するとサンプルデータが作成されます
    example_usage()
