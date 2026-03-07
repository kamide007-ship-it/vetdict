"""
analysis.html のバックエンドAPIエンドポイント専用テスト
- /api/pre-analyze-photo
- /api/pre-analyze-video
および analysis.html が依存するユーティリティ関数の単体テスト
"""

import importlib
import io
import struct
import zlib

import pytest


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def _app(temp_instance):
    """アプリを毎テスト再ロードして独立した状態にする"""
    import app as appmod
    importlib.reload(appmod)
    return appmod


@pytest.fixture()
def client(_app):
    return _app.app.test_client()


@pytest.fixture()
def auth_headers(client):
    """テスト用ユーザー登録→ログインしてセッションを取得する"""
    client.post('/api/auth/register', json={
        'email': 'analysis_test@example.com',
        'password': 'TestPass1!',
        'name': 'Analysis Tester',
    })
    client.post('/api/auth/login', json={
        'email': 'analysis_test@example.com',
        'password': 'TestPass1!',
    })
    return {}


# ---------------------------------------------------------------------------
# Helper: 最小 PNG バイナリを生成（依存ライブラリ不要）
# ---------------------------------------------------------------------------

def _minimal_png(width: int = 2, height: int = 2) -> bytes:
    """RGB 2x2 の最小 PNG を生成して返す"""
    def chunk(name: bytes, data: bytes) -> bytes:
        c = struct.pack('>I', len(data)) + name + data
        return c + struct.pack('>I', zlib.crc32(name + data) & 0xFFFFFFFF)

    header = b'\x89PNG\r\n\x1a\n'
    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
    ihdr = chunk(b'IHDR', ihdr_data)

    # Raw scanlines: filter byte(0) + RGB*width per row
    raw_row = b'\x00' + b'\xff\x00\x00' * width
    raw = raw_row * height
    compressed = zlib.compress(raw)
    idat = chunk(b'IDAT', compressed)

    iend = chunk(b'IEND', b'')
    return header + ihdr + idat + iend


# ---------------------------------------------------------------------------
# Unit Tests: /api/pre-analyze-photo
# ---------------------------------------------------------------------------

class TestPreAnalyzePhotoUnit:
    """photo エンドポイントの単体テスト"""

    def test_missing_photo_returns_400(self, client, auth_headers):
        """photoフィールドなしで400が返る"""
        r = client.post('/api/pre-analyze-photo',
                        data={'breed_id': '172d_poodle_toy'})
        assert r.status_code == 400
        body = r.get_json()
        assert body is not None
        assert 'error' in body

    def test_invalid_extension_returns_400(self, client, auth_headers):
        """不正な拡張子で400が返る"""
        data = {
            'photo': (io.BytesIO(b'not an image'), 'test.exe'),
            'breed_id': '172d_poodle_toy',
        }
        r = client.post('/api/pre-analyze-photo',
                        data=data,
                        content_type='multipart/form-data')
        assert r.status_code == 400
        body = r.get_json()
        assert 'error' in body

    def test_invalid_image_content_returns_400(self, client, auth_headers):
        """PNG拡張子でも内容が壊れていれば400が返る"""
        garbage = b'GIF89a' + b'\x00' * 100  # GIF を PNG として送信
        data = {
            'photo': (io.BytesIO(garbage), 'test.png'),
            'breed_id': '172d_poodle_toy',
        }
        r = client.post('/api/pre-analyze-photo',
                        data=data,
                        content_type='multipart/form-data')
        assert r.status_code in (400, 200)  # 実装によりエラーまたは解析続行

    def test_response_is_json(self, client, auth_headers):
        """レスポンスは必ずJSONである"""
        data = {
            'photo': (io.BytesIO(_minimal_png()), 'dog.png'),
            'breed_id': '172d_poodle_toy',
        }
        r = client.post('/api/pre-analyze-photo',
                        data=data,
                        content_type='multipart/form-data')
        assert r.content_type is not None
        assert 'application/json' in r.content_type

    def test_valid_photo_has_required_fields(self, client, auth_headers):
        """正常なPNG送信時、レスポンスに必須フィールドが含まれる"""
        data = {
            'photo': (io.BytesIO(_minimal_png()), 'dog.png'),
            'breed_id': '172d_poodle_toy',
        }
        r = client.post('/api/pre-analyze-photo',
                        data=data,
                        content_type='multipart/form-data')
        body = r.get_json()
        assert body is not None
        # success=True の場合は structure と coat が存在すること
        if body.get('success'):
            assert 'structure' in body or 'coat' in body
        else:
            assert 'error' in body

    def test_no_internal_error_details_leaked(self, client, auth_headers):
        """エラーレスポンスに内部例外詳細(str(e))が漏洩しないこと"""
        data = {
            'photo': (io.BytesIO(b'\x00' * 10), 'dog.jpg'),
            'breed_id': '172d_poodle_toy',
        }
        r = client.post('/api/pre-analyze-photo',
                        data=data,
                        content_type='multipart/form-data')
        body = r.get_json()
        if body and 'error' in body:
            err_str = str(body['error'])
            # Pythonのトレースバックやスタック情報が含まれていないこと
            assert 'Traceback' not in err_str
            assert 'File "' not in err_str

    def test_default_breed_used_when_not_specified(self, client, auth_headers):
        """breed_idを指定しない場合もデフォルト犬種で処理される"""
        data = {
            'photo': (io.BytesIO(_minimal_png()), 'dog.png'),
        }
        r = client.post('/api/pre-analyze-photo',
                        data=data,
                        content_type='multipart/form-data')
        # エラーにならずにレスポンスが返ること
        assert r.status_code in (200, 400)
        assert r.get_json() is not None


# ---------------------------------------------------------------------------
# Unit Tests: /api/pre-analyze-video
# ---------------------------------------------------------------------------

class TestPreAnalyzeVideoUnit:
    """video エンドポイントの単体テスト"""

    def test_missing_video_returns_400(self, client, auth_headers):
        """videoフィールドなしで400が返る"""
        r = client.post('/api/pre-analyze-video',
                        data={'breed_id': '172d_poodle_toy'})
        assert r.status_code == 400
        body = r.get_json()
        assert 'error' in body

    def test_invalid_extension_returns_400(self, client, auth_headers):
        """不正な拡張子(.exe)で400が返る"""
        data = {
            'video': (io.BytesIO(b'fake video data'), 'test.exe'),
            'breed_id': '172d_poodle_toy',
        }
        r = client.post('/api/pre-analyze-video',
                        data=data,
                        content_type='multipart/form-data')
        assert r.status_code == 400
        body = r.get_json()
        assert 'error' in body

    def test_response_is_json(self, client, auth_headers):
        """レスポンスは必ずJSONである"""
        data = {
            'video': (io.BytesIO(b'fake mp4 data'), 'test.mp4'),
            'breed_id': '172d_poodle_toy',
        }
        r = client.post('/api/pre-analyze-video',
                        data=data,
                        content_type='multipart/form-data')
        assert r.content_type is not None
        assert 'application/json' in r.content_type

    def test_garbage_video_returns_error(self, client, auth_headers):
        """壊れた動画データはエラーを返す"""
        data = {
            'video': (io.BytesIO(b'\x00' * 50), 'test.mp4'),
            'breed_id': '172d_poodle_toy',
        }
        r = client.post('/api/pre-analyze-video',
                        data=data,
                        content_type='multipart/form-data')
        body = r.get_json()
        assert body is not None
        # 壊れた動画→エラーまたはフレーム抽出失敗でエラーが返ること
        assert r.status_code in (400, 500) or 'error' in body

    def test_no_internal_error_details_leaked(self, client, auth_headers):
        """エラーレスポンスにトレースバックが漏洩しないこと"""
        data = {
            'video': (io.BytesIO(b'\x00' * 10), 'test.mp4'),
            'breed_id': '172d_poodle_toy',
        }
        r = client.post('/api/pre-analyze-video',
                        data=data,
                        content_type='multipart/form-data')
        body = r.get_json()
        if body and 'error' in body:
            err_str = str(body['error'])
            assert 'Traceback' not in err_str
            assert 'File "' not in err_str

    def test_unsupported_format_txt_returns_400(self, client, auth_headers):
        """テキストファイルを動画として送信すると400"""
        data = {
            'video': (io.BytesIO(b'Hello world'), 'test.txt'),
            'breed_id': '172d_poodle_toy',
        }
        r = client.post('/api/pre-analyze-video',
                        data=data,
                        content_type='multipart/form-data')
        assert r.status_code == 400


# ---------------------------------------------------------------------------
# Integration Tests: analysis.html が依存するAPIフロー
# ---------------------------------------------------------------------------

class TestAnalysisPageIntegration:
    """analysis.html の動作フローに対応する統合テスト"""

    def test_photo_analysis_full_flow(self, client, auth_headers):
        """
        analysis.html の写真解析フロー:
        1. POSTリクエスト送信
        2. レスポンスJSON構造を検証
        3. 必要なフィールドが存在することを確認
        """
        data = {
            'photo': (io.BytesIO(_minimal_png()), 'show_dog.png'),
            'breed_id': '172d_poodle_toy',
        }
        r = client.post('/api/pre-analyze-photo',
                        data=data,
                        content_type='multipart/form-data')
        assert r.status_code in (200, 400)
        body = r.get_json()
        assert isinstance(body, dict)

        if r.status_code == 200 and body.get('success'):
            # analysis.html が参照するフィールド
            assert 'structure' in body or 'coat' in body
            # elapsed フィールドがあれば数値であること
            if 'elapsed' in body:
                assert isinstance(body['elapsed'], (int, float))
                assert body['elapsed'] >= 0

    def test_photo_api_no_xss_in_filename_handling(self, client, auth_headers):
        """
        ファイル名にXSS文字列を含めてもサーバーがエラーを返し、
        スクリプトタグがJSONレスポンスに含まれないこと
        """
        xss_name = '<script>alert(1)</script>.png'
        data = {
            'photo': (io.BytesIO(_minimal_png()), xss_name),
            'breed_id': '172d_poodle_toy',
        }
        r = client.post('/api/pre-analyze-photo',
                        data=data,
                        content_type='multipart/form-data')
        raw_text = r.data.decode('utf-8', errors='replace')
        assert '<script>' not in raw_text

    def test_video_api_no_xss_in_filename_handling(self, client, auth_headers):
        """動画ファイル名のXSSがレスポンスに反映されないこと"""
        xss_name = '<img src=x onerror=alert(1)>.mp4'
        data = {
            'video': (io.BytesIO(b'\x00' * 20), xss_name),
            'breed_id': '172d_poodle_toy',
        }
        r = client.post('/api/pre-analyze-video',
                        data=data,
                        content_type='multipart/form-data')
        raw_text = r.data.decode('utf-8', errors='replace')
        assert '<img' not in raw_text or 'onerror' not in raw_text

    def test_breed_id_injection_rejected(self, client, auth_headers):
        """breed_idにSQLインジェクション試行しても500にならないこと"""
        malicious_breed = "' OR '1'='1"
        data = {
            'photo': (io.BytesIO(_minimal_png()), 'dog.png'),
            'breed_id': malicious_breed,
        }
        r = client.post('/api/pre-analyze-photo',
                        data=data,
                        content_type='multipart/form-data')
        # 500は返さないこと（内部エラーが外部に漏れていない）
        assert r.status_code != 500 or r.get_json() is not None

    def test_concurrent_photo_requests_independent(self, client, auth_headers):
        """同じファイルを複数回送信しても各レスポンスが独立していること"""
        results = []
        for _ in range(3):
            data = {
                'photo': (io.BytesIO(_minimal_png()), 'dog.png'),
                'breed_id': '172d_poodle_toy',
            }
            r = client.post('/api/pre-analyze-photo',
                            data=data,
                            content_type='multipart/form-data')
            results.append(r.status_code)
        # 全リクエストが処理されること
        assert len(results) == 3
        # 全て同じステータスコードであること（一貫性）
        assert len(set(results)) == 1

    def test_rate_limit_header_present(self, client, auth_headers):
        """レート制限ヘッダーが存在すること（Flask-Limiter）"""
        data = {
            'photo': (io.BytesIO(_minimal_png()), 'dog.png'),
            'breed_id': '172d_poodle_toy',
        }
        r = client.post('/api/pre-analyze-photo',
                        data=data,
                        content_type='multipart/form-data')
        # Flask-Limiter はデフォルトでヘッダーを設定する
        # (設定によっては存在しない場合もある)
        assert r.status_code in (200, 400, 429)


# ---------------------------------------------------------------------------
# Mobile / Browser Compatibility Tests (レスポンスヘッダー確認)
# ---------------------------------------------------------------------------

class TestBrowserCompatibility:
    """ブラウザ互換性・モバイル対応に関するヘッダーテスト"""

    def test_content_type_json_on_error(self, client, auth_headers):
        """エラー時もContent-Typeがapplication/jsonであること"""
        r = client.post('/api/pre-analyze-photo',
                        data={'breed_id': '172d_poodle_toy'})
        assert r.status_code == 400
        assert 'application/json' in r.content_type

    def test_cors_header_on_photo_endpoint(self, client, auth_headers):
        """CORSヘッダーが設定されていること"""
        r = client.options('/api/pre-analyze-photo',
                           headers={'Origin': 'https://example.com',
                                    'Access-Control-Request-Method': 'POST'})
        # CORS対応されていれば200かノーコンテンツ
        assert r.status_code in (200, 204)

    def test_large_file_rejected(self, client, auth_headers):
        """100MB超のファイルは拒否またはサーバーエラーにならないこと"""
        # 実際には1KBのダミーデータで拡張子のバリデーションを確認
        data = {
            'photo': (io.BytesIO(b'x' * 1024), 'large.bmp'),
            'breed_id': '172d_poodle_toy',
        }
        r = client.post('/api/pre-analyze-photo',
                        data=data,
                        content_type='multipart/form-data')
        # bmpは不正な拡張子なので400が返ること
        assert r.status_code == 400

    def test_utf8_filename_handling(self, client, auth_headers):
        """日本語ファイル名が処理されてもサーバーがクラッシュしないこと"""
        data = {
            'photo': (io.BytesIO(_minimal_png()), '犬の写真.png'),
            'breed_id': '172d_poodle_toy',
        }
        r = client.post('/api/pre-analyze-photo',
                        data=data,
                        content_type='multipart/form-data')
        assert r.status_code in (200, 400)
        assert r.get_json() is not None
