"""fixora init コマンドのテスト。"""
import os
import stat

from synapse_fixora.init import (
    CONFIG_FILENAME,
    run_init,
)


def test_init_creates_hook_and_config(tmp_path):
    """git リポジトリに hook と設定ファイルが生成される。"""
    # .git ディレクトリを作成（模擬リポジトリ）
    git_dir = tmp_path / ".git"
    git_dir.mkdir()

    result = run_init(str(tmp_path))

    assert result["status"] == "ok"

    # .fixora.yaml が生成されたか
    config_path = tmp_path / CONFIG_FILENAME
    assert config_path.exists()
    content = config_path.read_text(encoding="utf-8")
    assert "mode: DRY_RUN" in content
    assert "verify_profile: light" in content

    # pre-commit hook が生成されたか
    hook_path = tmp_path / ".git" / "hooks" / "pre-commit"
    assert hook_path.exists()
    hook_content = hook_path.read_text(encoding="utf-8")
    assert "Fixora auto-remediation hook" in hook_content
    assert "fixora gate" in hook_content

    # 実行権限が付いているか
    st = os.stat(hook_path)
    assert st.st_mode & stat.S_IEXEC


def test_init_not_git_repo(tmp_path):
    """git リポジトリでないディレクトリではエラーを返す。"""
    result = run_init(str(tmp_path))
    assert result["status"] == "error"
    assert "Git リポジトリではありません" in result["message"]


def test_init_custom_mode_and_hook(tmp_path):
    """カスタムのモードとフック種類を指定できる。"""
    git_dir = tmp_path / ".git"
    git_dir.mkdir()

    result = run_init(str(tmp_path), mode="AUTO_SAFE", verify_profile="strict", hook="pre-push")

    assert result["status"] == "ok"

    # pre-push hook が生成されたか
    hook_path = tmp_path / ".git" / "hooks" / "pre-push"
    assert hook_path.exists()
    hook_content = hook_path.read_text(encoding="utf-8")
    assert "fixora gate" in hook_content

    # 設定ファイルの内容確認（モード等は .fixora.yaml に記録される）
    config_path = tmp_path / CONFIG_FILENAME
    content = config_path.read_text(encoding="utf-8")
    assert "mode: AUTO_SAFE" in content
    assert "hook: pre-push" in content


def test_init_preserves_existing_hook(tmp_path):
    """既存の hook がある場合は追記する（上書きしない）。"""
    git_dir = tmp_path / ".git"
    hooks_dir = git_dir / "hooks"
    hooks_dir.mkdir(parents=True)

    existing_hook = hooks_dir / "pre-commit"
    existing_content = "#!/bin/sh\necho 'existing hook'\n"
    existing_hook.write_text(existing_content, encoding="utf-8")

    result = run_init(str(tmp_path))

    assert result["status"] == "ok"

    hook_content = existing_hook.read_text(encoding="utf-8")
    # 既存の内容が保持されている
    assert "existing hook" in hook_content
    # Fixora セクションが追記されている
    assert "Fixora auto-remediation hook (appended by fixora init)" in hook_content


def test_init_skip_if_already_installed(tmp_path):
    """既に Fixora hook がインストール済みの場合はスキップする。"""
    git_dir = tmp_path / ".git"
    hooks_dir = git_dir / "hooks"
    hooks_dir.mkdir(parents=True)

    # 初回 init
    run_init(str(tmp_path))

    hook_path = hooks_dir / "pre-commit"
    first_content = hook_path.read_text(encoding="utf-8")

    # 二回目 init
    result = run_init(str(tmp_path))

    assert result["status"] == "ok"

    # フックの内容が変わっていない（二重追記されていない）
    second_content = hook_path.read_text(encoding="utf-8")
    assert first_content == second_content
