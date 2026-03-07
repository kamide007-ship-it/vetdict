"""
dog_export_system.py
犬のカルテ管理 + 国際パスポート統合システム

【システム概要】
犬の医療記録（カルテ）と国際輸出検査申請書（パスポート）を統合管理。
カルテ情報が自動的にパスポートに反映され、不足項目を検出してPDF出力します。

【主な機能】
1. カルテ管理（犬の基本情報・予防接種記録）
2. 国際パスポート申請（カルテとの自動連携）
3. 必須項目チェック（不足項目をリスト化）
4. PDF生成（公式フォーム形式）

【ワークフロー】
犬登録（カルテ） → 国際パスポート作成（カルテデータ自動転送）
→ 不足項目チェック → クライアントが追加入力 → PDF出力

【使い方】
# 1. カルテ登録
from dog_export_system import DogMedicalRecord

medical_db = DogMedicalRecord("dog_clinic.db")
medical_db.create_tables()

record_data = {
    'dog_name': 'ポチ',
    'breed': '柴犬',
    'microchip_number': '392143000012345',
    'owner_name': '山田太郎',
    # ...
}
record_id = medical_db.add_record(record_data)

# 2. 国際パスポート作成（カルテから自動転送）
from dog_export_system import DogExportPassport

passport_db = DogExportPassport("dog_clinic.db")
application_id = passport_db.create_from_medical_record(
    medical_record_id=record_id,
    destination_country='アメリカ合衆国',
    embarkation_date='2024-12-20'
)

# 3. 必須項目チェック
missing = passport_db.check_required_fields(application_id)
if missing:
    print("不足項目:", missing)

# 4. PDF生成
passport_db.generate_pdf(application_id, "passport.pdf")
"""

import logging
import sqlite3

logger = logging.getLogger(__name__)
from typing import Dict, List, Optional, Tuple

from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


class DogMedicalRecord:
    """犬のカルテ管理クラス"""

    def __init__(self, db_path: str = "dog_clinic.db"):
        self.db_path = db_path
        self.conn = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row

    def close(self):
        if self.conn:
            self.conn.close()

    def create_tables(self):
        """カルテ用テーブルを作成"""
        self.connect()
        cursor = self.conn.cursor()

        # カルテメインテーブル
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS dog_medical_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            -- 犬の基本情報
            dog_name TEXT NOT NULL,
            breed TEXT,
            color TEXT,
            sex TEXT CHECK(sex IN ('オス', 'メス', '不明')),
            date_of_birth DATE,

            -- 体格情報
            body_length_cm REAL,
            body_height_cm REAL,
            body_weight_kg REAL,

            -- 個体識別
            microchip_number TEXT UNIQUE,
            microchip_date DATE,
            microchip_location TEXT DEFAULT '頸部',
            microchip_type TEXT,

            -- 飼い主情報
            owner_name TEXT NOT NULL,
            owner_address TEXT,
            owner_phone TEXT,

            -- 購入・飼養情報
            purchase_date DATE,
            purchase_place TEXT,
            keeping_place TEXT,

            -- 獣医情報
            veterinary_clinic TEXT,
            veterinarian_name TEXT,

            -- メタ情報
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # 国際パスポート申請テーブル
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS dog_export_applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            medical_record_id INTEGER NOT NULL,

            -- 申請者情報（飼い主と異なる場合）
            applicant_name TEXT,
            applicant_address TEXT,
            applicant_phone TEXT,
            applicant_company_name TEXT,

            -- 輸出情報
            destination_country TEXT NOT NULL,
            usage_purpose TEXT DEFAULT 'ペット',
            embarkation_date DATE,
            embarkation_place TEXT,
            vessel_name TEXT,
            flight_number TEXT,

            -- 荷送人・荷受人
            consignor_name TEXT,
            consignor_address TEXT,
            consignee_name TEXT,
            consignee_address TEXT,

            -- 帰国予定
            scheduled_reentry_date DATE,

            -- 検査機関
            laboratory_name TEXT,
            laboratory_address TEXT,

            -- ステータス
            status TEXT DEFAULT '作成中' CHECK(status IN ('作成中', '申請済み', '承認済み', '却下')),
            application_date DATE DEFAULT CURRENT_DATE,

            -- メタ情報
            remarks TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (medical_record_id) REFERENCES dog_medical_records(id) ON DELETE CASCADE
        )
        """)

        # 予防接種履歴テーブル（カルテと申請の両方に紐付け可能）
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS dog_vaccinations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            medical_record_id INTEGER,
            application_id INTEGER,

            vaccination_type TEXT NOT NULL CHECK(vaccination_type IN ('狂犬病', 'その他')),
            vaccination_date DATE NOT NULL,
            expiry_date DATE,
            vaccine_kind TEXT,
            product_name TEXT,
            manufacturer TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (medical_record_id) REFERENCES dog_medical_records(id) ON DELETE CASCADE,
            FOREIGN KEY (application_id) REFERENCES dog_export_applications(id) ON DELETE CASCADE
        )
        """)

        # 狂犬病抗体検査
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS dog_rabies_tests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            medical_record_id INTEGER,
            application_id INTEGER,

            blood_sampling_date DATE NOT NULL,
            antibody_titer_1 REAL,
            antibody_titer_2 REAL,
            unit TEXT DEFAULT 'IU/ml',

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (medical_record_id) REFERENCES dog_medical_records(id) ON DELETE CASCADE,
            FOREIGN KEY (application_id) REFERENCES dog_export_applications(id) ON DELETE CASCADE
        )
        """)

        # インデックス
        cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_microchip
        ON dog_medical_records(microchip_number)
        """)

        cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_medical_record
        ON dog_export_applications(medical_record_id)
        """)

        self.conn.commit()
        self.close()

    def add_record(self, data: Dict) -> int:
        """
        新規カルテを登録

        Args:
            data: カルテデータ（辞書形式）

        Returns:
            作成されたカルテID

        使用例:
            record_data = {
                'dog_name': 'ポチ',
                'breed': '柴犬',
                'color': '赤',
                'sex': 'オス',
                'date_of_birth': '2022-05-15',
                'microchip_number': '392143000012345',
                'owner_name': '山田太郎',
                'owner_address': '東京都渋谷区...',
                'owner_phone': '03-1234-5678'
            }
            record_id = medical_db.add_record(record_data)
        """
        self.connect()
        cursor = self.conn.cursor()

        cursor.execute("""
        INSERT INTO dog_medical_records (
            dog_name, breed, color, sex, date_of_birth,
            body_length_cm, body_height_cm, body_weight_kg,
            microchip_number, microchip_date, microchip_location, microchip_type,
            owner_name, owner_address, owner_phone,
            purchase_date, purchase_place, keeping_place,
            veterinary_clinic, veterinarian_name, notes
        ) VALUES (
            :dog_name, :breed, :color, :sex, :date_of_birth,
            :body_length_cm, :body_height_cm, :body_weight_kg,
            :microchip_number, :microchip_date, :microchip_location, :microchip_type,
            :owner_name, :owner_address, :owner_phone,
            :purchase_date, :purchase_place, :keeping_place,
            :veterinary_clinic, :veterinarian_name, :notes
        )
        """, data)

        record_id = cursor.lastrowid
        self.conn.commit()
        self.close()

        return record_id

    def get_record(self, record_id: int) -> Optional[Dict]:
        """カルテを取得"""
        self.connect()
        cursor = self.conn.cursor()

        cursor.execute("SELECT * FROM dog_medical_records WHERE id = ?", (record_id,))
        row = cursor.fetchone()
        self.close()

        return dict(row) if row else None

    def add_vaccination(self, record_id: int, vaccine_data: Dict):
        """カルテに予防接種を追加"""
        self.connect()
        cursor = self.conn.cursor()

        vaccine_data['medical_record_id'] = record_id
        vaccine_data['application_id'] = None

        cursor.execute("""
        INSERT INTO dog_vaccinations (
            medical_record_id, application_id, vaccination_type,
            vaccination_date, expiry_date, vaccine_kind, product_name, manufacturer
        ) VALUES (
            :medical_record_id, :application_id, :vaccination_type,
            :vaccination_date, :expiry_date, :vaccine_kind, :product_name, :manufacturer
        )
        """, vaccine_data)

        self.conn.commit()
        self.close()


class DogExportPassport:
    """国際パスポート（輸出検査申請）管理クラス"""

    # 必須項目の定義
    REQUIRED_FIELDS = {
        'applicant_name': '申請者氏名',
        'dog_name': '動物名',
        'microchip_number': 'マイクロチップ番号',
        'destination_country': '仕向国',
        'embarkation_date': '搭載予定日',
    }

    def __init__(self, db_path: str = "dog_clinic.db"):
        self.db_path = db_path
        self.conn = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row

    def close(self):
        if self.conn:
            self.conn.close()

    def create_from_medical_record(self,
                                   medical_record_id: int,
                                   destination_country: str,
                                   embarkation_date: Optional[str] = None,
                                   **additional_data) -> int:
        """
        カルテから国際パスポート申請を作成（データ自動転送）

        Args:
            medical_record_id: カルテID
            destination_country: 仕向国（必須）
            embarkation_date: 搭載予定日
            **additional_data: 追加データ

        Returns:
            作成された申請ID

        使用例:
            app_id = passport_db.create_from_medical_record(
                medical_record_id=1,
                destination_country='アメリカ合衆国',
                embarkation_date='2024-12-20',
                flight_number='NH001'
            )
        """
        self.connect()
        cursor = self.conn.cursor()

        # カルテ情報を取得
        cursor.execute("SELECT * FROM dog_medical_records WHERE id = ?", (medical_record_id,))
        record = cursor.fetchone()

        if not record:
            self.close()
            raise ValueError(f"カルテID {medical_record_id} が見つかりません")

        record_dict = dict(record)

        # 申請データを作成（カルテ情報を自動転送）
        application_data = {
            'medical_record_id': medical_record_id,
            'applicant_name': record_dict.get('owner_name'),
            'applicant_address': record_dict.get('owner_address'),
            'applicant_phone': record_dict.get('owner_phone'),
            'destination_country': destination_country,
            'embarkation_date': embarkation_date,
            'consignor_name': record_dict.get('owner_name'),
            'consignor_address': record_dict.get('owner_address'),
        }

        # 追加データをマージ
        application_data.update(additional_data)

        cursor.execute("""
        INSERT INTO dog_export_applications (
            medical_record_id, applicant_name, applicant_address, applicant_phone,
            applicant_company_name, destination_country, usage_purpose,
            embarkation_date, embarkation_place, vessel_name, flight_number,
            consignor_name, consignor_address, consignee_name, consignee_address,
            scheduled_reentry_date, laboratory_name, laboratory_address, remarks
        ) VALUES (
            :medical_record_id, :applicant_name, :applicant_address, :applicant_phone,
            :applicant_company_name, :destination_country, :usage_purpose,
            :embarkation_date, :embarkation_place, :vessel_name, :flight_number,
            :consignor_name, :consignor_address, :consignee_name, :consignee_address,
            :scheduled_reentry_date, :laboratory_name, :laboratory_address, :remarks
        )
        """, application_data)

        application_id = cursor.lastrowid

        # カルテの予防接種を申請にもコピー
        cursor.execute("""
        INSERT INTO dog_vaccinations (
            medical_record_id, application_id, vaccination_type,
            vaccination_date, expiry_date, vaccine_kind, product_name, manufacturer
        )
        SELECT
            medical_record_id, ? as application_id, vaccination_type,
            vaccination_date, expiry_date, vaccine_kind, product_name, manufacturer
        FROM dog_vaccinations
        WHERE medical_record_id = ? AND application_id IS NULL
        """, (application_id, medical_record_id))

        self.conn.commit()
        self.close()

        return application_id

    def check_required_fields(self, application_id: int) -> List[Dict[str, str]]:
        """
        必須項目チェック（不足項目をリスト化）

        Args:
            application_id: 申請ID

        Returns:
            不足項目のリスト [{'field': 'フィールド名', 'label': '日本語ラベル'}]

        使用例:
            missing = passport_db.check_required_fields(1)
            if missing:
                print("以下の項目が不足しています:")
                for item in missing:
                    print(f"  - {item['label']}")
        """
        self.connect()
        cursor = self.conn.cursor()

        # 申請とカルテを結合して取得
        cursor.execute("""
        SELECT
            a.*,
            m.dog_name,
            m.microchip_number
        FROM dog_export_applications a
        JOIN dog_medical_records m ON a.medical_record_id = m.id
        WHERE a.id = ?
        """, (application_id,))

        row = cursor.fetchone()

        if not row:
            self.close()
            raise ValueError(f"申請ID {application_id} が見つかりません")

        data = dict(row)
        missing_fields = []

        # 基本必須項目チェック
        for field, label in self.REQUIRED_FIELDS.items():
            if not data.get(field):
                missing_fields.append({'field': field, 'label': label})

        # 狂犬病予防接種チェック
        cursor.execute("""
        SELECT COUNT(*) as count FROM dog_vaccinations
        WHERE application_id = ? AND vaccination_type = '狂犬病'
        """, (application_id,))

        rabies_count = cursor.fetchone()['count']
        if rabies_count == 0:
            missing_fields.append({'field': 'rabies_vaccination', 'label': '狂犬病予防接種'})

        # 狂犬病抗体検査チェック
        cursor.execute("""
        SELECT COUNT(*) as count FROM dog_rabies_tests
        WHERE application_id = ?
        """, (application_id,))

        test_count = cursor.fetchone()['count']
        if test_count == 0:
            missing_fields.append({'field': 'rabies_test', 'label': '狂犬病抗体検査'})

        self.close()

        return missing_fields

    def get_full_data(self, application_id: int) -> Dict:
        """
        申請の完全データを取得（カルテ・予防接種・検査を含む）

        Args:
            application_id: 申請ID

        Returns:
            完全データ（辞書形式）
        """
        self.connect()
        cursor = self.conn.cursor()

        # 申請 + カルテ
        cursor.execute("""
        SELECT
            a.*,
            m.dog_name, m.breed, m.color, m.sex, m.date_of_birth,
            m.body_length_cm, m.body_height_cm, m.body_weight_kg,
            m.microchip_number, m.microchip_date, m.microchip_location, m.microchip_type,
            m.owner_name, m.owner_address, m.owner_phone,
            m.purchase_date, m.purchase_place, m.keeping_place
        FROM dog_export_applications a
        JOIN dog_medical_records m ON a.medical_record_id = m.id
        WHERE a.id = ?
        """, (application_id,))

        row = cursor.fetchone()
        if not row:
            self.close()
            raise ValueError(f"申請ID {application_id} が見つかりません")

        data = dict(row)

        # 予防接種
        cursor.execute("""
        SELECT * FROM dog_vaccinations
        WHERE application_id = ?
        ORDER BY vaccination_date DESC
        """, (application_id,))

        data['vaccinations'] = [dict(v) for v in cursor.fetchall()]

        # 抗体検査
        cursor.execute("""
        SELECT * FROM dog_rabies_tests
        WHERE application_id = ?
        ORDER BY blood_sampling_date DESC
        """, (application_id,))

        data['rabies_tests'] = [dict(t) for t in cursor.fetchall()]

        self.close()

        return data

    def generate_pdf(self, application_id: int, output_path: str, strict_validation: bool = False) -> Tuple[bool, str]:
        """
        国際パスポートPDFを生成

        Args:
            application_id: 申請ID
            output_path: 出力ファイルパス
            strict_validation: True=必須項目チェック（デフォルト: False=未記入でも出力可能）

        Returns:
            (成功/失敗, メッセージ)

        使用例:
            # 厳密なチェック（必須項目がないと出力不可）
            success, message = passport_db.generate_pdf(1, "passport.pdf", strict_validation=True)

            # 緩いチェック（未記入でも出力可能）
            success, message = passport_db.generate_pdf(1, "passport.pdf", strict_validation=False)

            if success:
                print("PDF生成成功")
            else:
                print(f"エラー: {message}")
        """
        # 必須項目チェック（strict_validation=Trueの場合のみ）
        if strict_validation:
            missing = self.check_required_fields(application_id)
            if missing:
                missing_labels = [m['label'] for m in missing]
                return False, f"以下の項目が不足しています: {', '.join(missing_labels)}"

        # データ取得
        try:
            data = self.get_full_data(application_id)
        except ValueError as e:
            logger.error(f"Data retrieval failed for application {application_id}: {e}")
            return False, "申請データの取得に失敗しました"

        # PDF生成
        try:
            self._create_pdf(data, output_path)
            return True, f"PDF生成完了: {output_path}"
        except Exception as e:
            logger.error(f"PDF generation failed: {e}", exc_info=True)
            return False, "PDF生成中にエラーが発生しました"

    def _create_pdf(self, data: Dict, output_path: str):
        """
        PDF実体生成（内部メソッド）

        ReportLabを使用してA4サイズのPDFを作成
        """
        # フォント登録（日本語対応）
        try:
            pdfmetrics.registerFont(TTFont('IPAexGothic', '/usr/share/fonts/opentype/ipaexfont-gothic/ipaexg.ttf'))
            font_name = 'IPAexGothic'
        except Exception as e:
            logging.getLogger(__name__).warning(f"Japanese font not available, falling back to Helvetica: {e}")
            font_name = 'Helvetica'

        c = canvas.Canvas(output_path, pagesize=A4)
        width, height = A4

        # タイトル
        c.setFont(font_name, 16)
        c.drawString(50, height - 50, "APPLICATION FOR EXPORT INSPECTION OF DOG")
        c.setFont(font_name, 12)
        c.drawString(50, height - 70, "狂犬病予防法及び家畜伝染病予防法に基づく犬の輸出検査申請書")

        # 申請日
        c.setFont(font_name, 10)
        c.drawString(400, height - 100, f"申請日: {data.get('application_date', '')}")

        # 申請者情報
        y = height - 130
        c.drawString(50, y, f"申請者氏名: {data.get('applicant_name', '')}")
        y -= 20
        c.drawString(50, y, f"住所: {data.get('applicant_address', '')}")
        y -= 20
        c.drawString(50, y, f"電話番号: {data.get('applicant_phone', '')}")

        # 動物情報
        y -= 40
        c.setFont(font_name, 12)
        c.drawString(50, y, "【動物情報】")
        c.setFont(font_name, 10)
        y -= 20
        c.drawString(50, y, f"名称: {data.get('dog_name', '')}")
        c.drawString(250, y, f"品種: {data.get('breed', '')}")
        c.drawString(400, y, f"毛色: {data.get('color', '')}")
        y -= 20
        c.drawString(50, y, f"性別: {data.get('sex', '')}")
        c.drawString(150, y, f"生年月日: {data.get('date_of_birth', '')}")
        c.drawString(350, y, f"仕向国: {data.get('destination_country', '')}")

        # 体格
        y -= 20
        c.drawString(50, y, f"体長: {data.get('body_length_cm', '')} cm")
        c.drawString(200, y, f"体高: {data.get('body_height_cm', '')} cm")
        c.drawString(350, y, f"体重: {data.get('body_weight_kg', '')} kg")

        # マイクロチップ
        y -= 30
        c.setFont(font_name, 12)
        c.drawString(50, y, "【個体識別】")
        c.setFont(font_name, 10)
        y -= 20
        c.drawString(50, y, f"マイクロチップ番号: {data.get('microchip_number', '')}")
        y -= 20
        c.drawString(50, y, f"識別日: {data.get('microchip_date', '')}")
        c.drawString(250, y, f"部位: {data.get('microchip_location', '')}")

        # 輸送情報
        y -= 30
        c.setFont(font_name, 12)
        c.drawString(50, y, "【輸送情報】")
        c.setFont(font_name, 10)
        y -= 20
        c.drawString(50, y, f"搭載日: {data.get('embarkation_date', '')}")
        c.drawString(250, y, f"搭載地: {data.get('embarkation_place', '')}")
        y -= 20
        c.drawString(50, y, f"便名: {data.get('flight_number', '')}")

        # 予防接種
        y -= 30
        c.setFont(font_name, 12)
        c.drawString(50, y, "【予防接種履歴】")
        c.setFont(font_name, 10)

        for vac in data.get('vaccinations', []):
            y -= 20
            if y < 100:
                c.showPage()
                y = height - 50
                c.setFont(font_name, 10)

            vac_text = f"{vac['vaccination_type']}: {vac['vaccination_date']} - {vac['product_name']}"
            c.drawString(50, y, vac_text)

        # 抗体検査
        y -= 30
        c.setFont(font_name, 12)
        c.drawString(50, y, "【狂犬病抗体検査】")
        c.setFont(font_name, 10)

        for test in data.get('rabies_tests', []):
            y -= 20
            if y < 100:
                c.showPage()
                y = height - 50
                c.setFont(font_name, 10)

            test_text = f"採血日: {test['blood_sampling_date']}, 抗体価: {test['antibody_titer_1']} {test['unit']}"
            c.drawString(50, y, test_text)

        # 備考
        if data.get('remarks'):
            y -= 30
            c.setFont(font_name, 12)
            c.drawString(50, y, "【備考】")
            c.setFont(font_name, 10)
            y -= 20
            c.drawString(50, y, data['remarks'])

        c.save()


# ========================================
# 使用例
# ========================================

def example_complete_workflow():
    """完全なワークフロー例"""

    print("=== 犬のカルテ + 国際パスポート統合システム ===\n")

    # 1. カルテ登録
    print("[1] 犬のカルテを登録")
    medical_db = DogMedicalRecord("dog_clinic_example.db")
    medical_db.create_tables()

    record_data = {
        'dog_name': 'ポチ',
        'breed': '柴犬',
        'color': '赤',
        'sex': 'オス',
        'date_of_birth': '2022-05-15',
        'body_length_cm': 45.0,
        'body_height_cm': 40.0,
        'body_weight_kg': 10.5,
        'microchip_number': '392143000012345',
        'microchip_date': '2022-06-01',
        'microchip_location': '頸部',
        'microchip_type': 'ISO 11784/11785準拠',
        'owner_name': '山田太郎',
        'owner_address': '東京都渋谷区神宮前1-2-3',
        'owner_phone': '03-1234-5678',
        'purchase_date': '2022-06-01',
        'purchase_place': 'ABCブリーダー',
        'keeping_place': '自宅',
        'veterinary_clinic': 'XYZ動物病院',
        'veterinarian_name': None,
        'notes': '特になし'
    }

    record_id = medical_db.add_record(record_data)
    print(f"✓ カルテID {record_id} を登録しました\n")

    # カルテに予防接種を追加
    print("[2] カルテに予防接種を追加")
    rabies_vaccine = {
        'vaccination_type': '狂犬病',
        'vaccination_date': '2024-10-01',
        'expiry_date': '2025-10-01',
        'vaccine_kind': '不活化ワクチン',
        'product_name': 'ラビエスワクチン',
        'manufacturer': 'XYZ製薬'
    }
    medical_db.add_vaccination(record_id, rabies_vaccine)
    print("✓ 狂犬病ワクチンを記録\n")

    # 2. 国際パスポート作成（カルテから自動転送）
    print("[3] カルテから国際パスポートを作成")
    passport_db = DogExportPassport("dog_clinic_example.db")

    app_id = passport_db.create_from_medical_record(
        medical_record_id=record_id,
        destination_country='アメリカ合衆国',
        embarkation_date='2024-12-20',
        embarkation_place='成田国際空港',
        flight_number='NH001',
        consignee_name='John Smith',
        consignee_address='123 Main St, New York, NY, USA',
        laboratory_name='指定検査機関ABC'
    )
    print(f"✓ 国際パスポートID {app_id} を作成\n")

    # 3. 必須項目チェック
    print("[4] 必須項目をチェック")
    missing = passport_db.check_required_fields(app_id)

    if missing:
        print("⚠️  以下の項目が不足しています（赤文字で通知）:")
        for item in missing:
            print(f"  🔴 {item['label']}")
        print()
    else:
        print("✓ すべての必須項目が入力されています\n")

    # 4. 不足項目を追加（狂犬病抗体検査）
    if missing:
        print("[5] 不足項目を追加")

        # 抗体検査を追加
        conn = sqlite3.connect("dog_clinic_example.db")
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO dog_rabies_tests (
            medical_record_id, application_id, blood_sampling_date,
            antibody_titer_1, unit
        ) VALUES (?, ?, ?, ?, ?)
        """, (record_id, app_id, '2024-10-15', 0.8, 'IU/ml'))
        conn.commit()
        conn.close()

        print("✓ 狂犬病抗体検査を追加\n")

        # 再チェック
        missing = passport_db.check_required_fields(app_id)
        if not missing:
            print("✓ すべての必須項目が揃いました！\n")

    # 5. PDF生成（厳密なチェックなし：未記入でも出力可能）
    print("[6] PDF生成")
    success, message = passport_db.generate_pdf(app_id, "dog_export_passport.pdf", strict_validation=False)

    if success:
        print(f"✅ {message}")
    else:
        print(f"❌ {message}")

    print("\n=== 完了 ===")


def example_lenient_pdf_workflow():
    """未記入フィールドがあってもPDF出力する例"""

    print("=== 犬のカルテ + 国際パスポート統合システム （緩いバリデーション） ===\n")

    # 1. 最小限の情報でカルテ登録
    print("[1] 最小限の情報でカルテを登録")
    medical_db = DogMedicalRecord("dog_clinic_lenient.db")
    medical_db.create_tables()

    record_data = {
        'dog_name': 'ポチ',  # 必須
        'breed': '',  # 未記入
        'color': '',  # 未記入
        'sex': '',  # 未記入
        'date_of_birth': '',  # 未記入
        'body_length_cm': None,
        'body_height_cm': None,
        'body_weight_kg': None,
        'microchip_number': '392143000012345',  # 必須
        'microchip_date': '',  # 未記入
        'microchip_location': '',  # 未記入
        'microchip_type': '',  # 未記入
        'owner_name': '山田太郎',  # 必須
        'owner_address': '',  # 未記入
        'owner_phone': '',  # 未記入
        'purchase_date': '',  # 未記入
        'purchase_place': '',  # 未記入
        'keeping_place': '',  # 未記入
        'veterinary_clinic': '',  # 未記入
        'veterinarian_name': None,
        'notes': '最小限の情報でPDF出力をテスト'
    }

    record_id = medical_db.add_record(record_data)
    print(f"✓ カルテID {record_id} を登録しました（未記入フィールド多数）\n")

    # 2. 国際パスポート作成（最小限のデータ）
    print("[2] 国際パスポートを作成（未記入フィールド可能）")
    passport_db = DogExportPassport("dog_clinic_lenient.db")

    app_id = passport_db.create_from_medical_record(
        medical_record_id=record_id,
        destination_country='アメリカ合衆国',
        # embarkation_date は未記入のままにする
    )
    print(f"✓ 国際パスポートID {app_id} を作成\n")

    # 3. 必須項目チェック（情報提供用）
    print("[3] 必須項目をチェック（情報提供のみ）")
    missing = passport_db.check_required_fields(app_id)

    if missing:
        print("⚠️  以下の項目が不足しています:")
        for item in missing:
            print(f"  - {item['label']}")
        print()

    # 4. PDF生成（未記入でも出力可能）
    print("[4] PDF生成（strict_validation=False）")
    success, message = passport_db.generate_pdf(app_id, "dog_export_passport_lenient.pdf", strict_validation=False)

    if success:
        print(f"✅ {message}")
        print("   → 未記入フィールドのPDF出力が成功しました\n")
    else:
        print(f"❌ {message}\n")

    print("=== 完了 ===")


if __name__ == "__main__":
    example_complete_workflow()
