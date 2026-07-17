"""画像アップロード共通モジュール。

Catbox を第一候補としてアップロードし、失敗時は自動でリトライする。
それでも失敗する場合、ImgBB の API キーが設定されていれば ImgBB に
フォールバックする。

ImgBB フォールバックを使うには、以下のいずれかで API キーを設定する:
  - 環境変数 IMGBB_API_KEY にキーを設定する
  - このフォルダに imgbb_key.txt を置き、中にキーだけを書く
(ImgBB の無料 API キーは https://api.imgbb.com/ から取得できます)

Catbox が一時的に不調でも ImgBB を設定しておけば投稿が止まりません。
"""

import os
import time
import requests

CATBOX_API_URL = 'https://catbox.moe/user/api.php'
IMGBB_API_URL = 'https://api.imgbb.com/1/upload'

MAX_RETRIES = 4
REQUEST_TIMEOUT = 90

_USER_AGENT = (
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
    'AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/150.0.0.0 Safari/537.36'
)


def _get_imgbb_key():
    key = os.environ.get('IMGBB_API_KEY', '').strip()
    if key:
        return key
    if os.path.exists('imgbb_key.txt'):
        with open('imgbb_key.txt', 'r', encoding='utf-8') as f:
            return f.read().strip()
    return ''


def _upload_catbox(file_path):
    """Returns (url, error_message). url is None on failure."""
    with open(file_path, 'rb') as f:
        files = {
            'fileToUpload': (
                os.path.basename(file_path),
                f,
                'application/octet-stream'
            )
        }
        data = {'reqtype': 'fileupload'}
        headers = {'User-Agent': _USER_AGENT}
        response = requests.post(
            CATBOX_API_URL, data=data, files=files,
            headers=headers, timeout=REQUEST_TIMEOUT
        )

    if response.status_code != 200:
        return None, f"HTTP {response.status_code}"

    url = (response.text or '').strip()
    if url.startswith('https://'):
        return url, None
    # 200 だが本文が空 or 想定外 → Catbox 側のレート制限/障害の可能性が高い
    return None, f"empty or invalid body: {url!r}"


def _upload_imgbb(file_path, api_key):
    """Returns (url, error_message). url is None on failure."""
    with open(file_path, 'rb') as f:
        response = requests.post(
            IMGBB_API_URL,
            params={'key': api_key},
            files={'image': f},
            timeout=REQUEST_TIMEOUT
        )
    if response.status_code != 200:
        return None, f"HTTP {response.status_code}: {response.text[:300]}"
    try:
        payload = response.json()
        url = payload['data']['url']
        if url and url.startswith('http'):
            return url, None
        return None, f"unexpected JSON: {payload}"
    except Exception as e:
        return None, f"parse error: {type(e).__name__}: {e}"


def upload_image(file_path):
    """画像をアップロードして URL を返す。失敗時は None。

    Catbox を優先し、指数バックオフでリトライ。全滅したら ImgBB に
    フォールバック(キーが設定されている場合のみ)。
    """
    if not os.path.exists(file_path):
        print(f"Image not found: {file_path}")
        return None

    # --- Catbox（リトライ付き） ---
    for attempt in range(1, MAX_RETRIES + 1):
        print(f"Uploading {file_path} to Catbox (attempt {attempt}/{MAX_RETRIES})...")
        try:
            url, err = _upload_catbox(file_path)
        except requests.Timeout:
            url, err = None, "timeout"
        except requests.RequestException as e:
            url, err = None, f"{type(e).__name__}: {e}"
        except OSError as e:
            print(f"Image file error: {type(e).__name__}: {e}")
            return None

        if url:
            print(f"Success (Catbox): {url}")
            return url

        if attempt < MAX_RETRIES:
            wait = 2 ** attempt  # 2, 4, 8 秒
            print(f"  Catbox failed: {err}. Retrying in {wait}s...")
            time.sleep(wait)
        else:
            print(f"  Catbox failed: {err}. (Catbox が混雑/制限中の可能性)")

    # --- ImgBB フォールバック ---
    imgbb_key = _get_imgbb_key()
    if imgbb_key:
        print("Falling back to ImgBB...")
        for attempt in range(1, MAX_RETRIES + 1):
            print(f"Uploading {file_path} to ImgBB (attempt {attempt}/{MAX_RETRIES})...")
            try:
                url, err = _upload_imgbb(file_path, imgbb_key)
            except requests.Timeout:
                url, err = None, "timeout"
            except requests.RequestException as e:
                url, err = None, f"{type(e).__name__}: {e}"
            if url:
                print(f"Success (ImgBB): {url}")
                return url
            if attempt < MAX_RETRIES:
                wait = 2 ** attempt
                print(f"  ImgBB failed: {err}. Retrying in {wait}s...")
                time.sleep(wait)
            else:
                print(f"  ImgBB failed: {err}.")
    else:
        print("  ImgBB フォールバックは未設定です。")
        print("  (imgbb_key.txt を置くか、環境変数 IMGBB_API_KEY を設定すると有効になります)")

    print(f"All upload attempts failed for {file_path}. しばらく時間をおいて再実行してください。")
    return None
