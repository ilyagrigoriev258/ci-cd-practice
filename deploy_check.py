import os
import subprocess
import sys
import tempfile

def main():
    print("[OK] Начинаем дымовую проверку...")
    if not os.path.exists("task_app.py"):
        print("ОШИБКА: task_app.py не найден!")
        sys.exit(1)
    
    print("[OK] Файл task_app.py найден")
    
    # Создаем временный файл, чтобы избежать проблем с правами записи в папке деплоя
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as f:
        tmp_file = f.name
    
    # Устанавливаем переменную окружения TASKS_FILE, чтобы приложение писало именно туда
    env = dict(os.environ, TASKS_FILE=tmp_file)
    
    try:
        print("[OK] Запускаем добавление задачи...")
        subprocess.run(
            [sys.executable, "task_app.py", "add", "Smoke task"],
            capture_output=True, text=True, env=env, check=True
        )
        print("[OK] Задача создана")
        
        print("[OK] Запускаем чтение задач...")
        result = subprocess.run(
            [sys.executable, "task_app.py", "list"],
            capture_output=True, text=True, env=env, check=True
        )
        assert "Smoke task" in result.stdout, "Задача не найдена в списке"
        print("[OK] Задача читается")
        
    except subprocess.CalledProcessError as e:
        print(f"ОШИБКА при выполнении: {e.stderr}")
        sys.exit(1)
    finally:
        # Удаляем временный файл после проверки
        if os.path.exists(tmp_file):
            os.remove(tmp_file)
    
    print("[SUCCESS] Все дымовые проверки пройдены")
    sys.exit(0)

if __name__ == "__main__":
    main()