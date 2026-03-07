# 📚 ShowDog 症状チェック API リファレンス

## 概要

ShowDog の症状チェック API は、犬の症状を入力して、AI が関連疾患の参考情報を提案するシステムです。

このドキュメントでは、**強化版 API** の詳細を説明します。

---

## 🔐 認証

すべての API エンドポイントは、`Authorization` ヘッダーで認証トークンを必要とします。

```javascript
const headers = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${authToken}`
};
```

---

## 📋 エンドポイント一覧

### 1. 症状チェック チャット（強化版）

**エンドポイント:** `POST /api/diagnostic-chat/chat`

**説明:** ユーザーの自然言語入力から症状を抽出し、関連疾患の参考情報とケアガイドを返します。

#### リクエスト

```json
{
    "message": "咳が続いているし、呼吸が苦しい気がします",
    "breed_id": "122_labrador_retriever",
    "age_years": 3.5,
    "previous_symptoms": ["fever"]
}
```

| パラメータ | 型 | 必須 | 説明 |
|-----------|----|----|------|
| `message` | string | ✅ | ユーザーの症状説明 |
| `breed_id` | string | ❌ | 犬種 ID（精度向上のため） |
| `age_years` | number | ❌ | 犬の年齢（年単位） |
| `previous_symptoms` | array | ❌ | 前回の会話で抽出された症状 |

#### レスポンス

```json
{
    "user_message": "咳が続いているし、呼吸が苦しい気がします",
    "extracted_symptoms": ["coughing", "labored_breathing"],
    "accumulated_symptoms": ["coughing", "labored_breathing", "fever"],
    "symptom_details": [
        {
            "id": "coughing",
            "name_ja": "咳",
            "name_en": "Coughing",
            "category": "respiratory"
        },
        {
            "id": "labored_breathing",
            "name_ja": "呼吸困難",
            "name_en": "Labored Breathing",
            "category": "respiratory"
        }
    ],
    "disease_candidates": [
        {
            "disease_id": "brachycephalic_airway_syndrome",
            "name_ja": "短頭種気道症候群",
            "name_en": "Brachycephalic Airway Syndrome",
            "severity": "high",
            "similarity_score": 0.85,
            "confidence_level": "85%",
            "matched_symptoms": ["labored_breathing", "coughing"],
            "unmatched_user_symptoms": ["fever"],
            "additional_disease_symptoms": ["reverse_sneezing", "sleep_apnea"],
            "description": "短頭種犬に見られる気道閉塞症候群...",
            "recommended_tests": ["X-ray (chest and neck)", "Laryngoscopy"],
            "reasoning": {
                "why_this_condition_ja": "患者犬の症状セット（2/3）が短頭種気道症候群と高く一致しており、類似度は85%です。",
                "why_this_condition_en": "The dog's symptom profile (2/3) shows strong alignment with Brachycephalic Airway Syndrome, with a similarity score of 85%.",
                "confidence_factors": [
                    {
                        "factor": "symptom_match",
                        "percentage": 85,
                        "weight": "High"
                    },
                    {
                        "factor": "breed_predisposition",
                        "percentage": 60,
                        "weight": "Medium"
                    },
                    {
                        "factor": "age_relevance",
                        "percentage": 40,
                        "weight": "Low"
                    }
                ]
            },
            "treatment_recommendations": {
                "primary_care_plan_ja": "こちらは参考情報です。具体的なケアについては獣医師にご相談ください。",
                "primary_care_plan_en": "Veterinary evaluation is essential. Depending on severity, medical management or surgery may be recommended.",
                "supplements": [
                    {
                        "name_ja": "オメガ3脂肪酸",
                        "name_en": "Omega-3 Fatty Acids",
                        "dosage": "500mg",
                        "frequency": "Daily",
                        "reason_ja": "気道炎症の軽減",
                        "reason_en": "Airway inflammation reduction",
                        "reference": "https://www.caninevet.jp/"
                    }
                ],
                "diagnostic_tests": [
                    {
                        "test_id": "xray",
                        "test_name_ja": "X線検査",
                        "test_name_en": "X-Ray",
                        "priority": 1,
                        "description_ja": "気道狭窄評価",
                        "description_en": "Airway obstruction assessment"
                    }
                ],
                "follow_up_schedule_ja": "2週間後に獣医師の再診を推奨",
                "follow_up_schedule_en": "Follow-up recommended in 2 weeks"
            }
        }
    ],
    "total_candidates": 8,
    "breed_context": "122_labrador_retriever",
    "age_context": 3.5,
    "analysis_steps": [
        {
            "step_id": "symptom_extraction",
            "step_name_ja": "症状抽出",
            "step_name_en": "Symptom Extraction",
            "status": "completed",
            "completion_percentage": 100
        },
        {
            "step_id": "disease_matching",
            "step_name_ja": "疾患マッチング",
            "step_name_en": "Disease Matching",
            "status": "completed",
            "completion_percentage": 100
        },
        {
            "step_id": "reasoning_generation",
            "step_name_ja": "判定根拠生成",
            "step_name_en": "Reasoning Generation",
            "status": "completed",
            "completion_percentage": 100
        }
    ],
    "recommendations": {
        "next_step": "This is reference information only. Please consult a veterinarian for professional evaluation.",
        "next_step_ja": "こちらは参考情報です。正確な評価のため、獣医師の診察を受けてください。",
        "navigation": {
            "dashboard": "/dashboard.html",
            "health_check": "/health-check.html",
            "dog_detail": null,
            "breeds": "/breeds.html"
        }
    }
}
```

#### 重要なフィールド

| フィールド | 説明 |
|-----------|------|
| `confidence_level` | 判定の信頼度（パーセンテージ） |
| `reasoning` | 判定根拠の詳細説明 |
| `confidence_factors` | 信頼度を構成するファクター |
| `treatment_recommendations` | ケアガイド情報（サプリメント、検査、スケジュール） |
| `analysis_steps` | UI 進捗表示用のメタデータ |

---

### 2. 類症鑑別比較

**エンドポイント:** `POST /api/diagnostic-chat/differential-analysis`

**説明:** 2つの疾患を比較し、症状の違いや検査による区別方法を説明します。

#### リクエスト

```json
{
    "disease_id_1": "brachycephalic_airway_syndrome",
    "disease_id_2": "congestive_heart_failure",
    "symptoms": ["labored_breathing", "coughing"],
    "breed_id": "122_labrador_retriever",
    "age_years": 3.5
}
```

| パラメータ | 型 | 必須 | 説明 |
|-----------|----|----|------|
| `disease_id_1` | string | ✅ | 比較対象の疾患 ID 1 |
| `disease_id_2` | string | ✅ | 比較対象の疾患 ID 2 |
| `symptoms` | array | ✅ | ユーザーが報告した症状 |
| `breed_id` | string | ❌ | 犬種 ID |
| `age_years` | number | ❌ | 犬の年齢 |

#### レスポンス

```json
{
    "disease_1": {
        "id": "brachycephalic_airway_syndrome",
        "name_ja": "短頭種気道症候群",
        "name_en": "Brachycephalic Airway Syndrome",
        "severity": "high",
        "description": "..."
    },
    "disease_2": {
        "id": "congestive_heart_failure",
        "name_ja": "心不全",
        "name_en": "Congestive Heart Failure",
        "severity": "emergency",
        "description": "..."
    },
    "symptom_analysis": {
        "shared_symptoms": ["labored_breathing"],
        "unique_to_disease_1": ["reverse_sneezing", "sleep_apnea"],
        "unique_to_disease_2": ["syncope", "edema"],
        "user_symptom_overlap_1": 2,
        "user_symptom_overlap_2": 1
    },
    "differential_reasoning_ja": "短頭種気道症候群と心不全は類似した症状を呈することがありますが、固有の症状と検査結果により区別されます。",
    "differential_reasoning_en": "Both Brachycephalic Airway Syndrome and Congestive Heart Failure can present with similar symptoms, but differ in specific findings and test results.",
    "recommended_diagnostic_tests": [
        "X-ray (chest and neck)",
        "Laryngoscopy",
        "Echocardiography",
        "ECG"
    ]
}
```

---

### 3. ケアガイド取得

**エンドポイント:** `POST /api/diagnostic-chat/treatment-plan`

**説明:** 特定の疾患に対する参考ケアガイド情報を取得します。

#### リクエスト

```json
{
    "disease_id": "brachycephalic_airway_syndrome",
    "breed_id": "122_labrador_retriever",
    "age_years": 3.5
}
```

| パラメータ | 型 | 必須 | 説明 |
|-----------|----|----|------|
| `disease_id` | string | ✅ | 疾患 ID |
| `breed_id` | string | ❌ | 犬種 ID（個別化計画用） |
| `age_years` | number | ❌ | 犬の年齢 |

#### レスポンス

```json
{
    "disease_id": "brachycephalic_airway_syndrome",
    "disease_name_ja": "短頭種気道症候群",
    "disease_name_en": "Brachycephalic Airway Syndrome",
    "severity": "high",
    "primary_care_plan_ja": "獣医師による診療評価が必須です...",
    "primary_care_plan_en": "Veterinary evaluation is essential...",
    "supplements": [
        {
            "name_ja": "オメガ3脂肪酸",
            "name_en": "Omega-3 Fatty Acids",
            "dosage": "500mg",
            "frequency": "Daily",
            "reason_ja": "気道炎症の軽減",
            "reason_en": "Airway inflammation reduction",
            "reference": "https://www.caninevet.jp/"
        }
    ],
    "diagnostic_tests": [
        {
            "test_id": "xray",
            "test_name_ja": "X線検査",
            "test_name_en": "X-Ray",
            "priority": 1,
            "description_ja": "気道狭窄評価",
            "description_en": "Airway obstruction assessment"
        }
    ],
    "follow_up_visits": [
        {
            "visit_number": 1,
            "days_after_diagnosis": 14,
            "focus_areas_ja": ["呼吸状態評価", "投薬レビュー"],
            "focus_areas_en": ["Respiratory Assessment", "Medication Review"]
        },
        {
            "visit_number": 2,
            "days_after_diagnosis": 60,
            "focus_areas_ja": ["症状改善確認", "ケアプラン調整"],
            "focus_areas_en": ["Symptom Improvement Check", "Care Plan Adjustment"]
        }
    ],
    "follow_up_schedule_ja": "初診より2週間後の再診を推奨",
    "follow_up_schedule_en": "Follow-up recommended in 2 weeks"
}
```

---

### 4. 症状サジェスチョン

**エンドポイント:** `GET /api/diagnostic-chat/symptom-suggestions`

**説明:** オートコンプリート用の症状リストを取得します。

#### リクエストパラメータ

| パラメータ | 型 | 説明 |
|-----------|----|----|------|
| `category` | string | カテゴリでフィルタ（respiratory, digestive など） |
| `search` | string | テキスト検索（部分一致） |

#### 例

```
GET /api/diagnostic-chat/symptom-suggestions?search=cough&category=respiratory
```

#### レスポンス

```json
{
    "total": 2,
    "symptoms": [
        {
            "id": "coughing",
            "name_ja": "咳",
            "name_en": "Coughing",
            "category": "respiratory"
        },
        {
            "id": "chronic_cough",
            "name_ja": "慢性的な咳",
            "name_en": "Chronic Cough",
            "category": "respiratory"
        }
    ]
}
```

---

### 5. 症状カテゴリ

**エンドポイント:** `GET /api/diagnostic-chat/categories`

**説明:** すべての症状カテゴリと症状を取得します。

#### レスポンス

```json
{
    "total_categories": 10,
    "categories": [
        {
            "id": "respiratory",
            "symptoms": [
                {
                    "id": "coughing",
                    "name_ja": "咳",
                    "name_en": "Coughing"
                },
                {
                    "id": "labored_breathing",
                    "name_ja": "呼吸困難",
                    "name_en": "Labored Breathing"
                }
            ]
        },
        {
            "id": "digestive",
            "symptoms": [...]
        }
    ]
}
```

---

## 🔍 API レスポンスコード

| コード | 説明 |
|--------|------|
| `200` | 成功 |
| `400` | リクエスト形式エラー |
| `401` | 認証エラー |
| `404` | リソースが見つからない |
| `500` | サーバーエラー |

---

## 💡 使用例

### JavaScript/TypeScript

```javascript
// 1. 症状チェック
async function getDiagnosis(message) {
    const response = await fetch('/api/diagnostic-chat/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${authToken}`
        },
        body: JSON.stringify({
            message: message,
            breed_id: 'labrador_retriever',
            age_years: 3.5
        })
    });

    const data = await response.json();

    // UI コンポーネントに渡す
    const renderer = new DiseaseCardRenderer('diseaseCardsContainer');
    renderer.renderCards(data.disease_candidates);

    return data;
}

// 2. 類症鑑別比較
async function compareDiseases(diseaseId1, diseaseId2, symptoms) {
    const response = await fetch('/api/diagnostic-chat/differential-analysis', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${authToken}`
        },
        body: JSON.stringify({
            disease_id_1: diseaseId1,
            disease_id_2: diseaseId2,
            symptoms: symptoms
        })
    });

    return await response.json();
}

// 3. ケアガイド取得
async function getTreatmentPlan(diseaseId, breedId, ageYears) {
    const response = await fetch('/api/diagnostic-chat/treatment-plan', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${authToken}`
        },
        body: JSON.stringify({
            disease_id: diseaseId,
            breed_id: breedId,
            age_years: ageYears
        })
    });

    const plan = await response.json();

    // UI に表示
    const planner = new TreatmentPlanDisplay(plan);
    planner.render('treatmentContainer');

    return plan;
}
```

### Python

```python
import requests

# API クライアント
class ShowDogAPI:
    def __init__(self, base_url, auth_token):
        self.base_url = base_url
        self.auth_token = auth_token
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {auth_token}'
        }

    def chat(self, message, breed_id=None, age_years=None):
        url = f'{self.base_url}/api/diagnostic-chat/chat'
        data = {
            'message': message,
            'breed_id': breed_id,
            'age_years': age_years
        }
        response = requests.post(url, json=data, headers=self.headers)
        return response.json()

    def differential_analysis(self, disease_id_1, disease_id_2, symptoms):
        url = f'{self.base_url}/api/diagnostic-chat/differential-analysis'
        data = {
            'disease_id_1': disease_id_1,
            'disease_id_2': disease_id_2,
            'symptoms': symptoms
        }
        response = requests.post(url, json=data, headers=self.headers)
        return response.json()

    def treatment_plan(self, disease_id, breed_id=None, age_years=None):
        url = f'{self.base_url}/api/diagnostic-chat/treatment-plan'
        data = {
            'disease_id': disease_id,
            'breed_id': breed_id,
            'age_years': age_years
        }
        response = requests.post(url, json=data, headers=self.headers)
        return response.json()

# 使用例
api = ShowDogAPI('http://localhost:5000', auth_token)
diagnosis = api.chat('咳が続いている')
print(diagnosis['disease_candidates'])
```

---

## 📊 エラー処理

```javascript
async function getDiagnosis(message) {
    try {
        const response = await fetch('/api/diagnostic-chat/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify({ message })
        });

        if (!response.ok) {
            const error = await response.json();
            console.error('API Error:', error);
            throw new Error(error.error || 'Unknown error');
        }

        return await response.json();
    } catch (error) {
        console.error('Request failed:', error);
        // UI にエラーメッセージを表示
        showError(error.message);
    }
}
```

---

## 🔄 データフロー

```
ユーザー入力
    ↓
/api/diagnostic-chat/chat
    ↓
症状抽出 → 疾患マッチング → 推論生成 → ケアガイド情報生成
    ↓
JSON レスポンス返却
    ↓
DiseaseCardRenderer で表示
    ↓
ユーザーがカード展開
    ↓
TreatmentPlanDisplay でケアガイド表示
```

---

## 📝 API 仕様変更履歴

### v2.0（現在）
- ✅ `reasoning` フィールド追加
- ✅ `confidence_factors` 追加
- ✅ `treatment_recommendations` 追加
- ✅ `analysis_steps` 追加
- ✅ `/differential-analysis` エンドポイント新規
- ✅ `/treatment-plan` エンドポイント新規

### v1.0
- 基本的な症状チェック機能のみ

---

## 🔗 関連リソース

- [テストガイド](./TEST_GUIDE.md)
- [コンポーネント使用ガイド](./COMPONENTS.md)
- [実装詳細](./IMPLEMENTATION.md)

---

**API リファレンス - 2026年2月17日 版**
