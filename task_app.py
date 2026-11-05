#!/usr/bin/env python3
"""Простое приложение для управления задачами."""
import argparse
import json
import os
import sys

DATA_FILE = os.environ.get("TASKS_FILE", "tasks.json")


def load_tasks(path=DATA_FILE):
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:  # Если файл пустой
                return []
            return json.loads(content)
    except json.JSONDecodeError:
        return []

def save_tasks(tasks, path=DATA_FILE):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


def add_task(title, author="anonymous", priority="normal", path=DATA_FILE):
    """Добавляет задачу. Пустое название запрещено."""
    if not title or not title.strip():
        raise ValueError("Название задачи не может быть пустым")
    if priority not in ("low", "normal", "high"):
        raise ValueError("Недопустимый приоритет")
    tasks = load_tasks(path)
    task = {"title": title.strip(), "author": author, "priority": priority}
    tasks.append(task)
    save_tasks(tasks, path)
    return task


def list_tasks(path=DATA_FILE):
    return load_tasks(path)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Менеджер задач")
    sub = parser.add_subparsers(dest="command")

    add_p = sub.add_parser("add", help="Добавить задачу")
    add_p.add_argument("title")
    add_p.add_argument("--author", default="anonymous")
    add_p.add_argument("--priority", default="normal")

    sub.add_parser("list", help="Показать задачи")

    args = parser.parse_args(argv)

    if args.command == "add":
        task = add_task(args.title, args.author, args.priority)
        print(f"Добавлено: {task}")
    elif args.command == "list":
        for t in list_tasks():
            print(f"[{t['priority']}] {t['title']} ({t['author']})")
    else:
        parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())