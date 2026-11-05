"""Дымовая проверка после deploy."""
import os
import subprocess
import sys
import tempfile

def main():
    out = subprocess.run(
        [sys.executable, "task_app.py", "--help"],
        capture_output=True, text=True, check=True
    )
    assert "usage" in out.stdout.lower(), "Нет справки в выводе"
    print("[OK] --help работает")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as f:
        tmp = f.name
    env = dict(os.environ, TASKS_FILE=tmp)

    add = subprocess.run(
        [sys.executable, "task_app.py", "add", "Smoke task"],
        capture_output=True, text=True, env=env, check=True
    )
    assert "Smoke task" in add.stdout
    print("[OK] Задача создана")

    lst = subprocess.run(
        [sys.executable, "task_app.py", "list"],
        capture_output=True, text=True, env=env, check=True
    )
    assert "Smoke task" in lst.stdout
    print("[OK] Задача читается")

    os.remove(tmp)
    print("[SUCCESS] Все дымовые проверки пройдены")

if __name__ == "__main__":
    main()