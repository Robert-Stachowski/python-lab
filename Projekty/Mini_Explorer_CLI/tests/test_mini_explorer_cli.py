import sys
import pytest
from mini_explorer_cli import main


def test_count_files(tmp_path, monkeypatch, capsys):
    (tmp_path / "a.txt").write_text("hello")
    (tmp_path / "b.txt").write_text("world :) ")
    (tmp_path / "c.py").write_text("code")


    monkeypatch.setattr(sys, "argv", ["prog", str(tmp_path), "--count"])
    result = main()

    captured = capsys.readouterr()
    assert result == 0
    assert captured.out.strip() == "3"


def test_list_files(tmp_path, monkeypatch, capsys):
    (tmp_path / "a.txt").write_text("hello")
    (tmp_path / "b.py").write_text("code")

    monkeypatch.setattr(sys, "argv", ["prog", str(tmp_path), "--list"])
    result = main()

    captured = capsys.readouterr()
    assert result == 0
    names = captured.out.strip().split("\n")
    assert "a.txt" in names
    assert "b.py" in names


def test_ext_filter(tmp_path, monkeypatch, capsys):
    (tmp_path / "a.txt").write_text("hello")
    (tmp_path / "b.txt").write_text("world :D ")
    (tmp_path / "c.py").write_text("craft code :) ")

    monkeypatch.setattr(sys, "argv", ["prog", str(tmp_path), "--ext", ".txt"])
    result = main()

    captured = capsys.readouterr()
    assert result == 0
    names = captured.out.strip().split("\n")
    assert "a.txt" in  names
    assert "b.txt" in names
    assert "c.py" not in names


def test_info_file(tmp_path, monkeypatch, capsys):
    f = tmp_path / "test.py"
    f.write_text("hello")

    monkeypatch.setattr(sys, "argv", ["prog", str(f), "--info"])
    result = main()

    captured = capsys.readouterr()
    assert result == 0
    assert "test.py" in captured.out
    assert ".py" in captured.out
    assert "Czy plik? True" in captured.out


def test_nonexistent_path(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["prog", "/nonexistent/path/xyz"])
    with pytest.raises(SystemExit) as exc:
        main()
    assert exc.value.code == 1


def test_wrong_flag_on_file(tmp_path, monkeypatch):
    f = tmp_path / "test.txt"
    f.write_text("hello")

    monkeypatch.setattr(sys, "argv", ["prog", str(f), "--count"])
    result = main()

    assert result == 2


def test_info_on_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["prog", str(tmp_path), "--info"])
    result = main()

    assert result == 2

