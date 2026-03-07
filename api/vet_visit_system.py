"""
vet_visit_system.py
動物病院受診用診察資料生成システム - 体調チェックボックス完全版

【充実した体調チェック項目】
10カテゴリ、60項目以上のチェックボックスで犬の状態を詳細に記録。

【使い方】
# 1. システム初期化
from vet_visit_system import VetVisitSystem

vet = VetVisitSystem("clinic.db")
vet.create_tables()

# 2. 診察記録作成（チェックボックス形式）
health_checks = {
    '全般状態': ['元気がない', 'ぐったりしている'],
    '消化器症状': ['嘔吐', '下痢', '血便'],
    '食欲・飲水': ['食欲なし', '多飲']
}

visit_data = {
    'medical_record_id': 1,
    'visit_date': '2024-02-08',
    'chief_complaint': '嘔吐・下痢',
    'health_checks': health_checks,
    'detailed_memo': '詳細な症状...',
    'body_weight_kg': 10.2,
    'body_temperature': 39.5
}

visit_id = vet.add_visit(visit_data)

# 3. プレビュー & PDF生成
html = vet.generate_html_preview(visit_id)
vet.generate_pdf(visit_id, 'report.pdf')
"""

import json
import logging
import sqlite3
from datetime import datetime
from typing import Dict, Tuple

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


class VetVisitSystem:
    """動物病院受診用診察資料生成システム（充実版）"""

    # 充実した体調チェック項目マスタ（10カテゴリ）
    HEALTH_CHECK_ITEMS = {
        '全般状態': [
            '元気がない',
            'ぐったりしている',
            '普段通り',
            '興奮している',
            '落ち着きがない'
        ],

        '食欲・飲水': [
            '食欲なし',
            '食欲低下',
            '食欲旺盛',
            '食欲普通',
            '水を飲まない',
            '多飲（水をよく飲む）',
            '飲水普通'
        ],

        '消化器症状': [
            '嘔吐',
            '吐き気（よだれが多い）',
            '下痢',
            '軟便',
            '便秘',
            '血便',
            '黒色便',
            '腹痛（触ると痛がる）',
            '腹部膨満（お腹が張っている）',
            'ゲップ・しゃっくり'
        ],

        '呼吸器症状': [
            '咳',
            'くしゃみ',
            '鼻水',
            '鼻血',
            '鼻づまり',
            '呼吸困難',
            '喘鳴（ゼーゼー音）',
            '開口呼吸',
            '呼吸が速い',
            '呼吸が遅い'
        ],

        '泌尿器症状': [
            '頻尿',
            '排尿困難',
            '血尿',
            '尿量減少',
            '尿が出ない',
            '尿漏れ',
            '尿の色が濃い',
            '尿の臭いが強い'
        ],

        '皮膚症状': [
            'かゆみ（掻く・舐める）',
            '脱毛',
            '発疹',
            '腫れ',
            'ただれ',
            'フケ',
            '赤み',
            '膿',
            '湿疹',
            '乾燥'
        ],

        '眼・耳・鼻症状': [
            '目やに',
            '充血',
            '涙が多い',
            '目が開かない',
            '目の腫れ',
            '耳を痒がる',
            '耳垂れ',
            '耳の臭い',
            '頭を振る',
            '耳が赤い'
        ],

        '運動器症状': [
            'びっこ（片足を引く）',
            '足を引きずる',
            '歩行困難',
            '立てない',
            '震え',
            'ふらつき',
            '関節の腫れ',
            '関節の痛み',
            '階段を嫌がる'
        ],

        '神経症状': [
            'けいれん',
            '意識障害',
            '麻痺',
            '旋回運動',
            '首を傾ける',
            '眼振（目が揺れる）',
            '失禁',
            '反応が鈍い'
        ],

        'その他': [
            '発熱（体が熱い）',
            '出血',
            '腫瘤（しこり）',
            '痛がる',
            '異物誤飲の疑い',
            '発作',
            '異常行動',
            '鳴き声の異常',
            '体重減少',
            '体重増加'
        ]
    }

    # 異常を示すキーワード（赤文字表示用）
    ABNORMAL_KEYWORDS = [
        '嘔吐', '下痢', '血便', '血尿', '出血', 'けいれん',
        '呼吸困難', '意識障害', '麻痺', '発熱', '異物誤飲',
        'ぐったり', '立てない', '開口呼吸', '尿が出ない',
        '腹痛', '痛がる', '黒色便', '鼻血'
    ]

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
        """データベーステーブル作成"""
        self.connect()
        cursor = self.conn.cursor()

        # カルテテーブル
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS dog_medical_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dog_name TEXT NOT NULL,
            breed TEXT,
            color TEXT,
            sex TEXT,
            date_of_birth DATE,
            body_weight_kg REAL,
            microchip_number TEXT UNIQUE,
            owner_name TEXT NOT NULL,
            owner_address TEXT,
            owner_phone TEXT,
            veterinary_clinic TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # 診察記録テーブル
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS medical_visits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            medical_record_id INTEGER NOT NULL,
            visit_date DATE NOT NULL,
            visit_time TIME,
            chief_complaint TEXT NOT NULL,
            health_checks TEXT,
            detailed_memo TEXT,
            body_weight_kg REAL,
            body_temperature REAL,
            heart_rate INTEGER,
            respiratory_rate INTEGER,
            diagnosis TEXT,
            treatment TEXT,
            prescription TEXT,
            next_visit_date DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (medical_record_id) REFERENCES dog_medical_records(id) ON DELETE CASCADE
        )
        """)

        # ワクチンテーブル
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS dog_vaccinations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            medical_record_id INTEGER NOT NULL,
            vaccination_type TEXT NOT NULL,
            vaccination_date DATE NOT NULL,
            expiry_date DATE,
            product_name TEXT,
            manufacturer TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (medical_record_id) REFERENCES dog_medical_records(id) ON DELETE CASCADE
        )
        """)

        self.conn.commit()
        self.close()

    def add_visit(self, data: Dict) -> int:
        """
        診察記録を追加

        Args:
            data: 診察記録データ
                - medical_record_id: カルテID
                - visit_date: 来院日
                - chief_complaint: 主訴
                - health_checks: 体調チェック（辞書形式）
                  例: {'全般状態': ['元気がない'], '消化器症状': ['嘔吐', '下痢']}
                - detailed_memo: 詳細メモ
                - body_weight_kg: 体重
                - body_temperature: 体温

        Returns:
            診察記録ID

        使用例:
            health_checks = {
                '全般状態': ['元気がない', 'ぐったりしている'],
                '消化器症状': ['嘔吐', '下痢'],
                '食欲・飲水': ['食欲なし']
            }

            visit_data = {
                'medical_record_id': 1,
                'visit_date': '2024-02-08',
                'chief_complaint': '嘔吐・下痢',
                'health_checks': health_checks,
                'detailed_memo': '昨夜から嘔吐3回...',
                'body_weight_kg': 10.2,
                'body_temperature': 39.5
            }

            visit_id = vet.add_visit(visit_data)
        """
        self.connect()
        cursor = self.conn.cursor()

        # health_checksをJSON文字列に変換
        if 'health_checks' in data and isinstance(data['health_checks'], dict):
            data['health_checks'] = json.dumps(data['health_checks'], ensure_ascii=False)

        cursor.execute("""
        INSERT INTO medical_visits (
            medical_record_id, visit_date, visit_time, chief_complaint,
            health_checks, detailed_memo,
            body_weight_kg, body_temperature, heart_rate, respiratory_rate,
            diagnosis, treatment, prescription, next_visit_date
        ) VALUES (
            :medical_record_id, :visit_date, :visit_time, :chief_complaint,
            :health_checks, :detailed_memo,
            :body_weight_kg, :body_temperature, :heart_rate, :respiratory_rate,
            :diagnosis, :treatment, :prescription, :next_visit_date
        )
        """, data)

        visit_id = cursor.lastrowid
        self.conn.commit()
        self.close()

        return visit_id

    def get_visit_full_data(self, visit_id: int) -> Dict:
        """診察記録の完全データを取得"""
        self.connect()
        cursor = self.conn.cursor()

        cursor.execute("""
        SELECT
            v.*,
            m.dog_name, m.breed, m.color, m.sex, m.date_of_birth,
            m.microchip_number, m.owner_name, m.owner_address, m.owner_phone,
            m.veterinary_clinic
        FROM medical_visits v
        JOIN dog_medical_records m ON v.medical_record_id = m.id
        WHERE v.id = ?
        """, (visit_id,))

        row = cursor.fetchone()
        if not row:
            self.close()
            raise ValueError(f"診察記録ID {visit_id} が見つかりません")

        data = dict(row)

        # health_checks JSON → 辞書
        if data.get('health_checks'):
            data['health_checks'] = json.loads(data['health_checks'])
        else:
            data['health_checks'] = {}

        # 年齢計算
        if data.get('date_of_birth'):
            birth_date = datetime.strptime(data['date_of_birth'], '%Y-%m-%d')
            today = datetime.now()
            age_years = (today - birth_date).days // 365
            data['age_years'] = age_years

        # ワクチン履歴
        cursor.execute("""
        SELECT * FROM dog_vaccinations
        WHERE medical_record_id = ?
        ORDER BY vaccination_date DESC
        """, (data['medical_record_id'],))

        data['vaccinations'] = [dict(v) for v in cursor.fetchall()]

        # 過去の診察記録
        cursor.execute("""
        SELECT * FROM medical_visits
        WHERE medical_record_id = ? AND id != ?
        ORDER BY visit_date DESC
        LIMIT 5
        """, (data['medical_record_id'], visit_id))

        past_visits = []
        for v in cursor.fetchall():
            visit_dict = dict(v)
            if visit_dict.get('health_checks'):
                visit_dict['health_checks'] = json.loads(visit_dict['health_checks'])
            past_visits.append(visit_dict)

        data['past_visits'] = past_visits

        self.close()

        return data

    def _is_abnormal(self, item: str) -> bool:
        """項目が異常を示すかチェック"""
        return any(keyword in item for keyword in self.ABNORMAL_KEYWORDS)

    def generate_html_preview(self, visit_id: int) -> str:
        """
        HTMLプレビュー生成

        使用例:
            html = vet.generate_html_preview(1)
            with open('preview.html', 'w', encoding='utf-8') as f:
                f.write(html)
        """
        data = self.get_visit_full_data(visit_id)
        health_checks = data.get('health_checks', {})

        # チェック項目数カウント
        total_checks = sum(len(items) for items in health_checks.values())
        abnormal_count = sum(
            1 for items in health_checks.values()
            for item in items
            if self._is_abnormal(item)
        )

        html = f"""
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>動物病院受診用資料 - {data.get('dog_name', '')}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}

        body {{
            font-family: 'Hiragino Kaku Gothic Pro', 'Meiryo', sans-serif;
            background: #f5f7fa;
            padding: 20px;
            line-height: 1.6;
        }}

        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }}

        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 30px;
        }}

        .header h1 {{
            font-size: 28px;
            margin-bottom: 10px;
        }}

        .header .subtitle {{
            font-size: 14px;
            opacity: 0.9;
        }}

        .stats {{
            display: flex;
            gap: 20px;
            margin-top: 20px;
        }}

        .stat-card {{
            background: rgba(255,255,255,0.2);
            padding: 15px;
            border-radius: 8px;
            flex: 1;
        }}

        .stat-label {{
            font-size: 12px;
            opacity: 0.9;
        }}

        .stat-value {{
            font-size: 24px;
            font-weight: bold;
            margin-top: 5px;
        }}

        .content {{
            padding: 30px;
        }}

        .section {{
            margin-bottom: 30px;
        }}

        .section-title {{
            font-size: 18px;
            font-weight: bold;
            color: #667eea;
            padding-bottom: 10px;
            border-bottom: 2px solid #e9ecef;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
        }}

        .info-card {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            border-left: 3px solid #667eea;
        }}

        .info-label {{
            font-size: 12px;
            color: #6c757d;
            margin-bottom: 5px;
        }}

        .info-value {{
            font-size: 16px;
            font-weight: 600;
            color: #212529;
        }}

        .health-check-category {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 15px;
        }}

        .category-name {{
            font-size: 16px;
            font-weight: bold;
            color: #495057;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .check-items {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }}

        .check-item {{
            background: white;
            padding: 8px 16px;
            border-radius: 20px;
            border: 2px solid #dee2e6;
            font-size: 14px;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }}

        .check-item.abnormal {{
            border-color: #dc3545;
            background: #fff5f5;
            color: #dc3545;
            font-weight: bold;
        }}

        .check-item::before {{
            content: '\\2713';
            font-weight: bold;
        }}

        .check-item.abnormal::before {{
            content: '\\26A0';
        }}

        .memo-box {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
            white-space: pre-wrap;
            min-height: 100px;
            font-size: 14px;
            line-height: 1.8;
        }}

        .vitals-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
        }}

        .vital-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
        }}

        .vital-label {{
            font-size: 12px;
            opacity: 0.9;
            margin-bottom: 10px;
        }}

        .vital-value {{
            font-size: 32px;
            font-weight: bold;
        }}

        .vital-unit {{
            font-size: 14px;
            opacity: 0.9;
            margin-left: 5px;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }}

        th {{
            background: #667eea;
            color: white;
            padding: 12px;
            text-align: left;
            font-size: 14px;
        }}

        td {{
            padding: 12px;
            border-bottom: 1px solid #e9ecef;
            font-size: 13px;
        }}

        tr:hover {{
            background: #f8f9fa;
        }}

        .alert-box {{
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }}

        .print-btn {{
            background: #667eea;
            color: white;
            border: none;
            padding: 15px 40px;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 10px;
            transition: all 0.3s;
        }}

        .print-btn:hover {{
            background: #5568d3;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }}

        @media print {{
            body {{ background: white; padding: 0; }}
            .container {{ box-shadow: none; }}
            .no-print {{ display: none; }}
            .print-btn {{ display: none; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>&#x1F3E5; 動物病院受診用資料</h1>
            <div class="subtitle">Medical Record for Veterinary Visit</div>
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-label">チェック項目数</div>
                    <div class="stat-value">{total_checks}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">異常項目数</div>
                    <div class="stat-value" style="color: #ff6b6b;">{abnormal_count}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">作成日時</div>
                    <div class="stat-value" style="font-size: 16px;">{datetime.now().strftime('%Y/%m/%d %H:%M')}</div>
                </div>
            </div>
        </div>

        <div class="content">
            <!-- 基本情報 -->
            <div class="section">
                <div class="section-title">
                    <span>&#x1F415;</span> 基本情報 / Basic Information
                </div>
                <div class="info-grid">
                    <div class="info-card">
                        <div class="info-label">犬の名前</div>
                        <div class="info-value">{data.get('dog_name', '未登録')}</div>
                    </div>
                    <div class="info-card">
                        <div class="info-label">品種</div>
                        <div class="info-value">{data.get('breed', '未登録')}</div>
                    </div>
                    <div class="info-card">
                        <div class="info-label">性別</div>
                        <div class="info-value">{data.get('sex', '未登録')}</div>
                    </div>
                    <div class="info-card">
                        <div class="info-label">年齢</div>
                        <div class="info-value">{data.get('age_years', '?')}歳</div>
                    </div>
                    <div class="info-card">
                        <div class="info-label">マイクロチップ</div>
                        <div class="info-value" style="font-size: 13px;">{data.get('microchip_number', '未登録')}</div>
                    </div>
                    <div class="info-card">
                        <div class="info-label">飼い主</div>
                        <div class="info-value">{data.get('owner_name', '未登録')}</div>
                    </div>
                </div>
            </div>

            <!-- 来院情報 -->
            <div class="section">
                <div class="section-title">
                    <span>&#x1F4C5;</span> 来院情報 / Visit Information
                </div>
                <div class="info-grid">
                    <div class="info-card">
                        <div class="info-label">来院日</div>
                        <div class="info-value">{data.get('visit_date', '未登録')}</div>
                    </div>
                    <div class="info-card">
                        <div class="info-label">主訴</div>
                        <div class="info-value">{data.get('chief_complaint', '未登録')}</div>
                    </div>
                </div>
            </div>

            <!-- バイタルサイン -->
            <div class="section">
                <div class="section-title">
                    <span>&#x1F493;</span> バイタルサイン / Vital Signs
                </div>
                <div class="vitals-grid">
                    <div class="vital-card">
                        <div class="vital-label">体重</div>
                        <div class="vital-value">{data.get('body_weight_kg', '-')}<span class="vital-unit">kg</span></div>
                    </div>
                    <div class="vital-card">
                        <div class="vital-label">体温</div>
                        <div class="vital-value">{data.get('body_temperature', '-')}<span class="vital-unit">&#xB0;C</span></div>
                    </div>
                    <div class="vital-card">
                        <div class="vital-label">心拍数</div>
                        <div class="vital-value">{data.get('heart_rate', '-')}<span class="vital-unit">bpm</span></div>
                    </div>
                </div>
            </div>
"""

        # 体調チェック
        if health_checks:
            html += """
            <div class="section">
                <div class="section-title">
                    <span>&#x2705;</span> 体調チェック / Health Check
                </div>
"""

            if abnormal_count > 0:
                html += f"""
                <div class="alert-box">
                    <strong>&#x26A0;&#xFE0F; 注意:</strong> {abnormal_count}件の異常項目が検出されました。
                </div>
"""

            icons = {
                '全般状態': '&#x1F321;&#xFE0F;',
                '食欲・飲水': '&#x1F356;',
                '消化器症状': '&#x1FAC3;',
                '呼吸器症状': '&#x1FAC1;',
                '泌尿器症状': '&#x1F4A7;',
                '皮膚症状': '&#x1FA79;',
                '眼・耳・鼻症状': '&#x1F441;&#xFE0F;',
                '運動器症状': '&#x1F9B4;',
                '神経症状': '&#x1F9E0;',
                'その他': '&#x1F4CC;'
            }

            for category, items in health_checks.items():
                if items:
                    icon = icons.get(category, '&#x1F4CB;')

                    html += f"""
                <div class="health-check-category">
                    <div class="category-name">
                        <span>{icon}</span> {category}
                    </div>
                    <div class="check-items">
"""

                    for item in items:
                        is_abnormal = self._is_abnormal(item)
                        abnormal_class = ' abnormal' if is_abnormal else ''

                        html += f"""
                        <div class="check-item{abnormal_class}">{item}</div>
"""

                    html += """
                    </div>
                </div>
"""

            html += """
            </div>
"""

        # 詳細メモ
        html += f"""
            <div class="section">
                <div class="section-title">
                    <span>&#x1F4DD;</span> 詳細メモ / Detailed Notes
                </div>
                <div class="memo-box">{data.get('detailed_memo', '記載なし')}</div>
            </div>
"""

        # ワクチン履歴
        html += """
            <div class="section">
                <div class="section-title">
                    <span>&#x1F489;</span> ワクチン接種履歴 / Vaccination History
                </div>
"""

        if data.get('vaccinations'):
            html += """
                <table>
                    <thead>
                        <tr>
                            <th>接種日</th>
                            <th>ワクチン種類</th>
                            <th>製品名</th>
                            <th>有効期限</th>
                        </tr>
                    </thead>
                    <tbody>
"""
            for vac in data['vaccinations']:
                html += f"""
                        <tr>
                            <td>{vac.get('vaccination_date', '-')}</td>
                            <td>{vac.get('vaccination_type', '-')}</td>
                            <td>{vac.get('product_name', '-')}</td>
                            <td>{vac.get('expiry_date', '-')}</td>
                        </tr>
"""
            html += """
                    </tbody>
                </table>
"""
        else:
            html += '<div class="alert-box">ワクチン接種履歴がありません</div>'

        html += """
            </div>

            <div class="no-print" style="text-align: center; margin-top: 40px;">
                <button class="print-btn" onclick="window.print()">
                    <span>&#x1F5A8;&#xFE0F;</span> 印刷 / Print
                </button>
            </div>
        </div>
    </div>
</body>
</html>
"""

        return html

    def generate_pdf(self, visit_id: int, output_path: str) -> Tuple[bool, str]:
        """PDF生成"""
        try:
            data = self.get_visit_full_data(visit_id)
            self._create_pdf(data, output_path)
            return True, f"PDF生成完了: {output_path}"
        except Exception as e:
            logging.getLogger(__name__).error(f"PDF generation failed: {e}", exc_info=True)
            return False, "PDF生成中にエラーが発生しました"

    def _create_pdf(self, data: Dict, output_path: str):
        """PDF実体生成"""
        # フォント登録
        try:
            pdfmetrics.registerFont(TTFont('JPFont', '/usr/share/fonts/opentype/ipaexfont-gothic/ipaexg.ttf'))
            jp_font = 'JPFont'
        except Exception as e:
            logging.getLogger(__name__).warning(f"Japanese font not available, falling back to Helvetica: {e}")
            jp_font = 'Helvetica'

        c = canvas.Canvas(output_path, pagesize=A4)
        width, height = A4
        margin = 20 * mm

        # ヘッダー
        c.setFillColor(colors.HexColor('#667eea'))
        c.rect(0, height - 60*mm, width, 60*mm, fill=True, stroke=False)

        c.setFillColor(colors.white)
        c.setFont(jp_font, 20)
        c.drawString(margin, height - 35*mm, "動物病院受診用資料")

        c.setFont('Helvetica', 14)
        c.drawString(margin, height - 45*mm, "Medical Record for Veterinary Visit")

        c.setFont(jp_font, 10)
        c.drawString(margin, height - 55*mm, f"作成日: {datetime.now().strftime('%Y年%m月%d日')}")

        # 基本情報
        y = height - 75*mm
        c.setFillColor(colors.black)

        c.setFillColor(colors.HexColor('#667eea'))
        c.rect(margin, y - 8*mm, width - 2*margin, 8*mm, fill=True, stroke=False)
        c.setFillColor(colors.white)
        c.setFont(jp_font, 12)
        c.drawString(margin + 3*mm, y - 6*mm, "基本情報")

        y -= 15*mm
        c.setFillColor(colors.black)
        c.setFont(jp_font, 10)

        col1_x = margin
        col2_x = width / 2

        c.drawString(col1_x, y, f"犬の名前: {data.get('dog_name', '未登録')}")
        c.drawString(col2_x, y, f"品種: {data.get('breed', '未登録')}")
        y -= 5*mm
        c.drawString(col1_x, y, f"性別: {data.get('sex', '未登録')}")
        c.drawString(col2_x, y, f"年齢: {data.get('age_years', '?')}歳")
        y -= 5*mm
        c.drawString(col1_x, y, f"マイクロチップ: {data.get('microchip_number', '未登録')}")

        # 来院情報
        y -= 15*mm
        c.setFillColor(colors.HexColor('#667eea'))
        c.rect(margin, y - 8*mm, width - 2*margin, 8*mm, fill=True, stroke=False)
        c.setFillColor(colors.white)
        c.setFont(jp_font, 12)
        c.drawString(margin + 3*mm, y - 6*mm, "来院情報")

        y -= 15*mm
        c.setFillColor(colors.black)
        c.setFont(jp_font, 10)
        c.drawString(col1_x, y, f"来院日: {data.get('visit_date', '未登録')}")
        c.drawString(col2_x, y, f"主訴: {data.get('chief_complaint', '未登録')}")

        # バイタルサイン
        y -= 15*mm
        c.setFillColor(colors.HexColor('#667eea'))
        c.rect(margin, y - 8*mm, width - 2*margin, 8*mm, fill=True, stroke=False)
        c.setFillColor(colors.white)
        c.setFont(jp_font, 12)
        c.drawString(margin + 3*mm, y - 6*mm, "バイタルサイン")

        y -= 15*mm
        c.setFillColor(colors.black)
        c.setFont(jp_font, 10)
        c.drawString(col1_x, y, f"体重: {data.get('body_weight_kg', '-')} kg")
        c.drawString(col2_x, y, f"体温: {data.get('body_temperature', '-')} °C")

        # 体調チェック
        y -= 15*mm
        c.setFillColor(colors.HexColor('#667eea'))
        c.rect(margin, y - 8*mm, width - 2*margin, 8*mm, fill=True, stroke=False)
        c.setFillColor(colors.white)
        c.setFont(jp_font, 12)
        c.drawString(margin + 3*mm, y - 6*mm, "体調チェック")

        y -= 12*mm
        c.setFont(jp_font, 9)

        health_checks = data.get('health_checks', {})
        for category, items in health_checks.items():
            if items:
                if y < 40*mm:
                    c.showPage()
                    y = height - margin
                    c.setFont(jp_font, 9)

                c.setFillColor(colors.black)
                c.drawString(margin, y, f"【{category}】")
                y -= 5*mm

                for item in items:
                    if y < 40*mm:
                        c.showPage()
                        y = height - margin
                        c.setFont(jp_font, 9)

                    # 異常項目は赤文字
                    if self._is_abnormal(item):
                        c.setFillColor(colors.HexColor('#dc3545'))
                    else:
                        c.setFillColor(colors.black)

                    c.drawString(margin + 5*mm, y, f"• {item}")
                    y -= 5*mm

                y -= 3*mm

        # 詳細メモ
        y -= 10*mm
        if y < 60*mm:
            c.showPage()
            y = height - margin

        c.setFillColor(colors.HexColor('#667eea'))
        c.rect(margin, y - 8*mm, width - 2*margin, 8*mm, fill=True, stroke=False)
        c.setFillColor(colors.white)
        c.setFont(jp_font, 12)
        c.drawString(margin + 3*mm, y - 6*mm, "詳細メモ")

        y -= 15*mm
        c.setFillColor(colors.black)
        c.setFont(jp_font, 9)

        memo = data.get('detailed_memo', '記載なし')
        for line in memo.split('\n'):
            if y < 40*mm:
                c.showPage()
                y = height - margin
                c.setFont(jp_font, 9)
            c.drawString(margin, y, line)
            y -= 5*mm

        c.save()


# 使用例
def example_workflow():
    """完全なワークフロー例"""

    print("=== 動物病院受診用診察資料システム（充実版） ===\n")

    vet = VetVisitSystem("vet_clinic_full.db")
    vet.create_tables()
    print("✓ システム初期化完了\n")

    # サンプルカルテ登録
    conn = sqlite3.connect("vet_clinic_full.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR IGNORE INTO dog_medical_records (
        id, dog_name, breed, color, sex, date_of_birth,
        body_weight_kg, microchip_number,
        owner_name, owner_phone
    ) VALUES (1, 'ポチ', '柴犬', '赤', 'オス', '2022-05-15',
              10.5, '392143000012345',
              '山田太郎', '03-1234-5678')
    """)

    cursor.execute("""
    INSERT OR IGNORE INTO dog_vaccinations (
        medical_record_id, vaccination_type, vaccination_date,
        product_name
    ) VALUES (1, '狂犬病', '2024-04-01', 'ラビエスワクチン')
    """)

    conn.commit()
    conn.close()
    print("✓ カルテ登録完了\n")

    # 診察記録作成（充実したチェックボックス）
    print("✓ 診察記録作成（充実したチェックボックス）\n")

    health_checks = {
        '全般状態': ['元気がない', 'ぐったりしている'],
        '食欲・飲水': ['食欲なし', '多飲（水をよく飲む）'],
        '消化器症状': ['嘔吐', '下痢', '腹痛（触ると痛がる）'],
        '呼吸器症状': ['普段通り'],
        '皮膚症状': ['かゆみ（掻く・舐める）']
    }

    visit_data = {
        'medical_record_id': 1,
        'visit_date': '2024-02-08',
        'visit_time': '14:30',
        'chief_complaint': '嘔吐・下痢・食欲不振',
        'health_checks': health_checks,
        'detailed_memo': '''昨夜22時頃から嘔吐が始まり、今朝までに3回嘔吐。
嘔吐物は未消化のフード。
今朝6時頃から下痢も始まる（水様便、1日5回）。
朝食・昼食ともに食べず。水は普段より多く飲む。
ぐったりとして元気がなく、散歩に行きたがらない。
お腹を触ると痛がる様子。''',
        'body_weight_kg': 10.2,
        'body_temperature': 39.5,
        'heart_rate': 110,
        'respiratory_rate': 28,
        'diagnosis': None,
        'treatment': None,
        'prescription': None,
        'next_visit_date': None
    }

    visit_id = vet.add_visit(visit_data)
    print(f"✓ 診察記録ID {visit_id} を作成")
    print(f"  チェック項目数: {sum(len(items) for items in health_checks.values())}件\n")

    # HTMLプレビュー生成
    print("✓ HTMLプレビュー生成中...")
    html = vet.generate_html_preview(visit_id)

    with open('vet_visit_preview.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print("✅ HTMLプレビュー生成完了: vet_visit_preview.html\n")

    # PDF生成
    print("✓ PDF生成中...")
    success, message = vet.generate_pdf(visit_id, 'vet_visit_report.pdf')

    if success:
        print(f"✅ {message}\n")
    else:
        print(f"❌ {message}\n")

    print("=== 完了 ===")
    print("\n生成されたファイル:")
    print("  📄 vet_visit_preview.html - ブラウザで確認可能")
    print("  📄 vet_visit_report.pdf - 動物病院提出用")
    print("\n体調チェック項目（10カテゴリ）:")
    for i, (cat, items) in enumerate(vet.HEALTH_CHECK_ITEMS.items(), 1):
        print(f"  {i}. {cat}: {len(items)}項目")


if __name__ == "__main__":
    example_workflow()
