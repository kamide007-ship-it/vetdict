"""fixora gate コマンドのテスト。"""

from synapse_fixora.gate import load_config, _count_issues, _print_summary, run_gate
from synapse_fixora.init import CONFIG_FILENAME


def test_load_config_defaults(tmp_path):
    """設定ファイルが無い場合にデフォルト値を返す。"""
    config = load_config(str(tmp_path))
    assert config["mode"] == "DRY_RUN"
    assert config["verify_profile"] == "light"
    assert config["block"] == "true"


def test_load_config_reads_yaml(tmp_path):
    """`.fixora.yaml` から値を正しく読み込む。"""
    config_path = tmp_path / CONFIG_FILENAME
    config_path.write_text(
        "mode: AUTO_SAFE\nverify_profile: strict\nblock: false\n",
        encoding="utf-8",
    )
    config = load_config(str(tmp_path))
    assert config["mode"] == "AUTO_SAFE"
    assert config["verify_profile"] == "strict"
    assert config["block"] == "false"


def test_load_config_ignores_comments(tmp_path):
    """コメント行と空行を無視する。"""
    config_path = tmp_path / CONFIG_FILENAME
    config_path.write_text(
        "# This is a comment\n\nmode: DRY_RUN\n# another comment\n",
        encoding="utf-8",
    )
    config = load_config(str(tmp_path))
    assert config["mode"] == "DRY_RUN"


def test_count_issues_empty():
    """空のレポートでは全件数0。"""
    v, c, i, f = _count_issues({})
    assert (v, c, i, f) == (0, 0, 0, 0)


def test_count_issues_with_data():
    """レポートから正しく件数を抽出する。"""
    report = {
        "analysis": {
            "layer_violations": [{"from": "a", "to": "b"}],
            "cycles": [["a", "b", "a"], ["c", "d", "c"]],
        },
        "debug": {"issue_count": 5, "fixed_count": 3},
    }
    v, c, i, f = _count_issues(report)
    assert v == 1
    assert c == 2
    assert i == 5
    assert f == 3


def test_print_summary_no_issues(capsys):
    """問題0件で OK メッセージを出す。"""
    _print_summary(0, 0, 0, 0)
    out = capsys.readouterr().out
    assert "✅" in out


def test_print_summary_with_issues(capsys):
    """問題がある場合に件数を表示する。"""
    _print_summary(2, 1, 3, 0)
    out = capsys.readouterr().out
    assert "レイヤー違反 2件" in out
    assert "循環依存 1件" in out
    assert "静的問題 3件" in out


def test_print_summary_with_fixes(capsys):
    """自動修正件数が表示される。"""
    _print_summary(0, 0, 5, 4)
    out = capsys.readouterr().out
    assert "自動修正: 4件" in out


def test_run_gate_clean_repo(tmp_path):
    """問題のないリポジトリで exit 0 を返す。"""
    (tmp_path / ".git").mkdir()
    # .fixora.yaml を作成
    config_path = tmp_path / CONFIG_FILENAME
    config_path.write_text("mode: DRY_RUN\nverify_profile: light\nblock: true\n", encoding="utf-8")
    exit_code = run_gate(str(tmp_path))
    assert exit_code == 0


def test_run_gate_block_false_returns_zero(tmp_path):
    """block: false の場合は問題があっても exit 0 を返す。"""
    (tmp_path / ".git").mkdir()
    config_path = tmp_path / CONFIG_FILENAME
    config_path.write_text("mode: DRY_RUN\nverify_profile: light\nblock: false\n", encoding="utf-8")

    # レイヤー違反を作るファイルを用意 (domain → routes)
    domain_dir = tmp_path / "domain"
    routes_dir = tmp_path / "routes"
    domain_dir.mkdir()
    routes_dir.mkdir()
    (domain_dir / "__init__.py").write_text("")
    (routes_dir / "__init__.py").write_text("")
    (domain_dir / "model.py").write_text("from routes import handler\n")
    (routes_dir / "handler.py").write_text("x = 1\n")

    exit_code = run_gate(str(tmp_path))
    # block: false なので問題があっても 0
    assert exit_code == 0
