#!/usr/bin/env python3
"""
Generic Analysis Platform - Main Application
config.py を編集するだけで任意のドメインに対応可能
"""

import base64
import json
import logging
import os
import re
import sys
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from functools import wraps

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import (
    AI_PROMPT_PRIMARY,
    AI_PROMPT_SECONDARY,
    AI_PROMPT_VIDEO,
    CATEGORIES,
    DEFAULT_CATEGORY,
    GRADE_THRESHOLDS,
    PHOTO_AXES_PRIMARY,
    PHOTO_AXES_SECONDARY,
    PLATFORM_NAME,
    PLATFORM_VERSION,
    WEIGHTS_PHOTO_ONLY,
    WEIGHTS_WITH_VIDEO,
)

# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------
from api.database import (
    create_reset_token,
    create_session,
    create_user,
    delete_session,
    get_user_by_email,
    update_user_password,
    verify_reset_token,
    verify_security_answer,
    verify_session,
    verify_user,
)

# ---------------------------------------------------------------------------
# Local analysis
# ---------------------------------------------------------------------------
from api.local_analysis import analyze_primary_local, analyze_secondary_local, analyze_video_local

# ---------------------------------------------------------------------------
# Vision API setup
# ---------------------------------------------------------------------------
ANTHROPIC_AVAILABLE = False
OPENAI_AVAILABLE = False

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    pass

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    pass

ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

claude_client = None
openai_client = None
VISION_ENABLED = False
VISION_PROVIDER = "none"

if ANTHROPIC_AVAILABLE and ANTHROPIC_API_KEY:
    claude_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY, timeout=30.0, max_retries=2)
    VISION_ENABLED = True
    VISION_PROVIDER = "claude"
elif OPENAI_AVAILABLE and OPENAI_API_KEY:
    openai_client = OpenAI(api_key=OPENAI_API_KEY, timeout=30.0, max_retries=2)
    VISION_ENABLED = True
    VISION_PROVIDER = "openai"

# ---------------------------------------------------------------------------
# Flask App
# ---------------------------------------------------------------------------
app = Flask(__name__, static_folder='../static')
CORS(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, 'uploads')
os.makedirs(UPLOAD_DIR, exist_ok=True)

logger.info(f"{PLATFORM_NAME} v{PLATFORM_VERSION}")
logger.info(f"Vision: {'Enabled' if VISION_ENABLED else 'Disabled'} (Provider: {VISION_PROVIDER})")

# ---------------------------------------------------------------------------
# JSON response parsing (optimized)
# ---------------------------------------------------------------------------
_JSON_BLOCK_RE = re.compile(r'```(?:json)?\s*\n?(.*?)\n?\s*```', re.DOTALL)
_BARE_JSON_RE = re.compile(r'\A\s*[\[{]')


def parse_json_response(content):
    if _BARE_JSON_RE.match(content):
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            pass
    m = _JSON_BLOCK_RE.search(content)
    if m:
        return json.loads(m.group(1))
    try:
        return json.loads(content.strip())
    except json.JSONDecodeError as e:
        logger.error(f"JSON parse failed: {e}; preview: {content[:200]!r}")
        raise


# ---------------------------------------------------------------------------
# Vision API call
# ---------------------------------------------------------------------------
def call_vision_api(prompt, image_base64, max_tokens=500):
    if VISION_PROVIDER == "claude":
        response = claude_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": [
                {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": image_base64}},
                {"type": "text", "text": prompt}
            ]}]
        )
        return response.content[0].text
    elif VISION_PROVIDER == "openai":
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}", "detail": "low"}}
            ]}],
            max_tokens=max_tokens, temperature=0.3
        )
        return response.choices[0].message.content
    raise Exception("No vision provider available")


# ---------------------------------------------------------------------------
# Analysis functions (config-driven)
# ---------------------------------------------------------------------------
def _build_axes_description(axes_list):
    return "\n".join(f"{i+1}. {a['name']}（{a['description']}）" for i, a in enumerate(axes_list))


def _build_axes_json_template(axes_list):
    parts = ['"score": 85.0']
    for a in axes_list:
        parts.append(f'"{a["key"]}": 85')
    parts.append('"comments": "具体的な評価コメント"')
    return "{{\n    " + ",\n    ".join(parts) + "\n}}"


def analyze_photo_primary(image_base64, category_name, category_data):
    if not VISION_ENABLED:
        result = analyze_primary_local(image_base64, category_name, category_data)
        if result:
            return result
        return {'score': 80.0, 'comments': 'Vision API未設定（モック）'}

    try:
        prompt = AI_PROMPT_PRIMARY.format(
            platform_name=PLATFORM_NAME,
            category_name=category_name,
            standard=category_data.get('ideal_standard', '標準基準'),
            axes_description=_build_axes_description(PHOTO_AXES_PRIMARY['axes']),
            axes_json=_build_axes_json_template(PHOTO_AXES_PRIMARY['axes']),
        )
        return parse_json_response(call_vision_api(prompt, image_base64, 500))
    except Exception as e:
        logger.error(f"Primary analysis error: {e}")
        result = analyze_primary_local(image_base64, category_name, category_data)
        return result or {'score': 78.0, 'comments': '解析中にエラーが発生しました', 'error': 'analysis_failed'}


def analyze_photo_secondary(image_base64, category_name, category_data):
    if not VISION_ENABLED:
        result = analyze_secondary_local(image_base64, category_name, category_data)
        if result:
            return result
        return {'score': 80.0, 'comments': 'Vision API未設定（モック）'}

    try:
        prompt = AI_PROMPT_SECONDARY.format(
            platform_name=PLATFORM_NAME,
            category_name=category_name,
            standard=category_data.get('ideal_standard', '標準基準'),
            axes_description=_build_axes_description(PHOTO_AXES_SECONDARY['axes']),
            axes_json=_build_axes_json_template(PHOTO_AXES_SECONDARY['axes']),
        )
        return parse_json_response(call_vision_api(prompt, image_base64, 400))
    except Exception as e:
        logger.error(f"Secondary analysis error: {e}")
        result = analyze_secondary_local(image_base64, category_name, category_data)
        return result or {'score': 78.0, 'comments': '解析中にエラーが発生しました', 'error': 'analysis_failed'}


def analyze_video_frames(video_frames, category_name, category_data):
    if not VISION_ENABLED or not video_frames:
        if video_frames:
            result = analyze_video_local(video_frames, category_name, category_data)
            if result:
                return result
        return {
            'motion': {'score': 80.0, 'comments': '動画未提供またはVision API未設定'},
            'behavior': {'score': 80.0, 'comments': '動画未提供またはVision API未設定'},
            'surface_motion': {'score': 80.0, 'comments': '動画未提供またはVision API未設定'},
        }

    try:
        # Use first 3 frames with vision API
        if VISION_PROVIDER == "claude":
            parts = []
            for frame in video_frames[:3]:
                parts.append({"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": frame}})
            prompt = AI_PROMPT_VIDEO.format(
                platform_name=PLATFORM_NAME,
                category_name=category_name,
                standard=category_data.get('ideal_standard', '標準基準'),
                axes_description="動作・振る舞い・表面動態",
                axes_json='{ "motion": {...}, "behavior": {...}, "surface_motion": {...} }',
            )
            parts.append({"type": "text", "text": prompt})
            response = claude_client.messages.create(
                model="claude-sonnet-4-20250514", max_tokens=600,
                messages=[{"role": "user", "content": parts}]
            )
            return parse_json_response(response.content[0].text)
        elif VISION_PROVIDER == "openai":
            parts = [{"type": "text", "text": AI_PROMPT_VIDEO.format(
                platform_name=PLATFORM_NAME,
                category_name=category_name,
                standard=category_data.get('ideal_standard', '標準基準'),
                axes_description="動作・振る舞い・表面動態",
                axes_json='{ "motion": {...}, "behavior": {...}, "surface_motion": {...} }',
            )}]
            for frame in video_frames[:3]:
                parts.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{frame}", "detail": "low"}})
            response = openai_client.chat.completions.create(
                model="gpt-4o", messages=[{"role": "user", "content": parts}],
                max_tokens=600, temperature=0.3
            )
            return parse_json_response(response.choices[0].message.content)
    except Exception as e:
        logger.error(f"Video analysis error: {e}")
        result = analyze_video_local(video_frames, category_name, category_data)
        return result or {
            'motion': {'score': 78.0, 'comments': f'エラー: {e}'},
            'behavior': {'score': 78.0, 'comments': f'エラー: {e}'},
            'surface_motion': {'score': 78.0, 'comments': f'エラー: {e}'},
        }


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------
def calculate_grade(score):
    for threshold, en, ja in GRADE_THRESHOLDS:
        if score >= threshold:
            return f"{en} ({ja})"
    return "Ungraded"


def calculate_overall(primary_result, secondary_result, video_result, has_video):
    weights = WEIGHTS_WITH_VIDEO if has_video else WEIGHTS_PHOTO_ONLY
    p = primary_result.get('score', 80)
    s = secondary_result.get('score', 80)

    if has_video:
        m = video_result.get('motion', {}).get('score', 80)
        b = video_result.get('behavior', {}).get('score', 80)
        overall = (p * weights['primary'] + s * weights['secondary']
                   + m * weights['motion'] + b * weights['behavior'])
    else:
        overall = p * weights['primary'] + s * weights['secondary']

    return round(overall, 1)


# ---------------------------------------------------------------------------
# Auth decorators
# ---------------------------------------------------------------------------
def _get_token():
    auth = request.headers.get('Authorization', '')
    if auth.startswith('Bearer '):
        return auth[7:]
    return request.cookies.get('session_token')


def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = _get_token()
        if not token:
            return jsonify({'error': 'Authentication required'}), 401
        user = verify_session(token)
        if not user:
            return jsonify({'error': 'Invalid or expired session'}), 401
        request.current_user = user
        return f(*args, **kwargs)
    return decorated


def optional_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = _get_token()
        request.current_user = verify_session(token) if token else None
        return f(*args, **kwargs)
    return decorated


# ---------------------------------------------------------------------------
# Static files
# ---------------------------------------------------------------------------
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/<path:filename>')
def serve_static(filename):
    try:
        return send_from_directory(app.static_folder, filename)
    except Exception as err:
        # Log the error but return 404 instead of 500
        logging.debug(f'Static file not found: {filename}')
        return jsonify({'error': 'Not found'}), 404


# ---------------------------------------------------------------------------
# Global Error Handlers
# ---------------------------------------------------------------------------
@app.errorhandler(404)
def handle_404(error):
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def handle_500(error):
    logging.error(f'Internal Server Error: {error}')
    return jsonify({'error': 'Internal server error'}), 500


# ---------------------------------------------------------------------------
# Auth Endpoints
# ---------------------------------------------------------------------------
@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    name = data.get('name', '').strip()
    sq = data.get('security_question', '').strip()
    sa = data.get('security_answer', '').strip()

    if not email or '@' not in email:
        return jsonify({'error': 'Valid email is required'}), 400
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400
    if not sq or not sa:
        return jsonify({'error': '合言葉を入力してください'}), 400

    user = create_user(email, password, name or None, sq, sa)
    if not user:
        return jsonify({'error': 'Email already registered'}), 409

    token = create_session(user['id'])
    resp = jsonify({'success': True, 'user': user, 'token': token})
    resp.set_cookie('session_token', token, httponly=True, samesite='Lax', max_age=30*86400)
    return resp


@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    user = verify_user(data.get('email', '').strip().lower(), data.get('password', ''))
    if not user:
        return jsonify({'error': 'Invalid email or password'}), 401
    token = create_session(user['id'])
    resp = jsonify({'success': True, 'user': user, 'token': token})
    resp.set_cookie('session_token', token, httponly=True, samesite='Lax', max_age=30*86400)
    return resp


@app.route('/api/auth/logout', methods=['POST'])
def logout():
    token = _get_token()
    if token:
        delete_session(token)
    resp = jsonify({'success': True})
    resp.delete_cookie('session_token')
    return resp


@app.route('/api/auth/me', methods=['GET'])
def auth_me():
    token = _get_token()
    if not token:
        return jsonify({'error': 'Not authenticated'}), 401
    user = verify_session(token)
    if not user:
        return jsonify({'error': 'Session expired'}), 401
    return jsonify({'success': True, 'user': user})


@app.route('/api/auth/security-question', methods=['POST'])
def get_security_question():
    email = request.get_json().get('email', '').strip().lower()
    user = get_user_by_email(email)
    if not user or not user.get('security_question'):
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'success': True, 'security_question': user['security_question']})


@app.route('/api/auth/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email', '').strip().lower()
    sa = data.get('security_answer', '').strip()
    if not email or not sa:
        return jsonify({'error': '入力してください'}), 400

    verified = verify_security_answer(email, sa)
    if not verified:
        return jsonify({'error': 'メールアドレスまたは合言葉が正しくありません'}), 401

    token = create_reset_token(verified['id'])
    # SMTP省略 - インラインリセット
    return jsonify({'success': True, 'reset_token': token,
                    'message': 'このままパスワードをリセットできます。'})


@app.route('/api/auth/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    token = data.get('token', '').strip()
    new_pw = data.get('new_password', '')
    if len(new_pw) < 6:
        return jsonify({'error': 'パスワードは6文字以上'}), 400
    user_id = verify_reset_token(token)
    if not user_id:
        return jsonify({'error': 'トークンが無効または期限切れ'}), 401
    update_user_password(user_id, new_pw)
    return jsonify({'success': True, 'message': 'パスワードをリセットしました。'})


# ---------------------------------------------------------------------------
# Categories
# ---------------------------------------------------------------------------
@app.route('/api/categories', methods=['GET'])
def get_categories():
    cats = [{'id': k, 'name': v['name'], 'name_en': v.get('name_en', k)}
            for k, v in CATEGORIES.items()]
    return jsonify({'categories': cats, 'count': len(cats)})


# ---------------------------------------------------------------------------
# Comprehensive Analysis Endpoint
# ---------------------------------------------------------------------------
@app.route('/api/analyze', methods=['POST'])
@optional_auth
def analyze():
    category_id = request.form.get('category_id', DEFAULT_CATEGORY)
    category_data = CATEGORIES.get(category_id, CATEGORIES[DEFAULT_CATEGORY])
    category_name = category_data['name']

    if 'photo' not in request.files:
        return jsonify({'error': '写真が必要です'}), 400

    # Read photo once
    photo_bytes = request.files['photo'].read()
    photo_base64 = base64.b64encode(photo_bytes).decode('utf-8')
    del photo_bytes

    # Video frames
    video_frames = []
    has_video = 'video' in request.files and request.files['video'].filename
    if has_video:
        vpath = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}.mp4")
        request.files['video'].save(vpath)
        video_frames = _extract_frames(vpath, 3)

    # Parallel analysis
    start = time.time()
    with ThreadPoolExecutor(max_workers=3) as ex:
        f_primary = ex.submit(analyze_photo_primary, photo_base64, category_name, category_data)
        f_secondary = ex.submit(analyze_photo_secondary, photo_base64, category_name, category_data)
        f_video = ex.submit(analyze_video_frames, video_frames, category_name, category_data) if video_frames else None

        primary_result = f_primary.result(timeout=45)
        secondary_result = f_secondary.result(timeout=45)
        video_result = f_video.result(timeout=45) if f_video else {}

    overall = calculate_overall(primary_result, secondary_result, video_result, has_video)
    grade = calculate_grade(overall)
    elapsed = round(time.time() - start, 2)

    result = {
        'overall_score': overall,
        'grade': grade,
        'category': {'id': category_id, 'name': category_name},
        'scores': {
            'primary': primary_result,
            'secondary': secondary_result,
        },
        'has_video': has_video,
        'analysis_time': elapsed,
        'vision_provider': VISION_PROVIDER,
        'version': PLATFORM_VERSION,
    }
    if has_video:
        result['scores']['motion'] = video_result.get('motion', {})
        result['scores']['behavior'] = video_result.get('behavior', {})
        result['scores']['surface_motion'] = video_result.get('surface_motion', {})

    return jsonify(result)


def _extract_frames(video_path, num_frames=3, max_dim=512):
    frames = []
    try:
        import cv2
        cap = cv2.VideoCapture(video_path)
        total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if total <= 0:
            return frames
        indices = [int(i * total / num_frames) for i in range(num_frames)]
        for idx in indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
            ret, frame = cap.read()
            if ret:
                h, w = frame.shape[:2]
                if max(h, w) > max_dim:
                    s = max_dim / max(h, w)
                    frame = cv2.resize(frame, (int(w * s), int(h * s)), interpolation=cv2.INTER_AREA)
                _, buf = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
                frames.append(base64.b64encode(buf).decode('utf-8'))
        cap.release()
    except Exception as e:
        logger.error(f"Frame extraction error: {e}")
    return frames


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'ok',
        'platform': PLATFORM_NAME,
        'version': PLATFORM_VERSION,
        'vision_enabled': VISION_ENABLED,
        'provider': VISION_PROVIDER,
    })


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.getenv('FLASK_DEBUG', '0') == '1')
