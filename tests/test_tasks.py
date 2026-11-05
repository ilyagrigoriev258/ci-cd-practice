import json
import os
import tempfile
import unittest

from task_app import add_task, load_tasks, list_tasks, save_tasks


class TaskAppTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        self.tmp.close()
        self.path = self.tmp.name
        save_tasks([], self.path)

    def tearDown(self):
        if os.path.exists(self.path):
            os.remove(self.path)

    # --- 10+ тестов ---
    def test_add_task_returns_dict(self):
        task = add_task("Помыть посуду", path=self.path)
        self.assertIsInstance(task, dict)

    def test_add_task_saves_to_file(self):
        add_task("Купить хлеб", path=self.path)
        self.assertEqual(len(load_tasks(self.path)), 1)

    def test_blank_title_is_rejected(self):
        """Намеренно нарушаемое требование по варианту 1."""
        with self.assertRaises(ValueError):
            add_task("   ", path=self.path)

    def test_empty_string_title_is_rejected(self):
        with self.assertRaises(ValueError):
            add_task("", path=self.path)

    def test_invalid_priority_is_rejected(self):
        with self.assertRaises(ValueError):
            add_task("Задача", priority="urgent", path=self.path)

    def test_valid_priorities_accepted(self):
        for p in ("low", "normal", "high"):
            add_task(f"Задача {p}", priority=p, path=self.path)

    def test_author_saved(self):
        add_task("Тест", author="Иван", path=self.path)
        self.assertEqual(load_tasks(self.path)[0]["author"], "Иван")

    def test_title_is_stripped(self):
        add_task("  Пробелы  ", path=self.path)
        self.assertEqual(load_tasks(self.path)[0]["title"], "Пробелы")

    def test_list_tasks_returns_all(self):
        add_task("A", path=self.path)
        add_task("B", path=self.path)
        self.assertEqual(len(list_tasks(self.path)), 2)

    def test_save_and_load_roundtrip(self):
        data = [{"title": "X", "author": "Y", "priority": "high"}]
        save_tasks(data, self.path)
        self.assertEqual(load_tasks(self.path), data)

    def test_file_is_valid_json(self):
        add_task("JSON", path=self.path)
        with open(self.path, encoding="utf-8") as f:
            json.load(f)  # не должно упасть

    def test_multiple_tasks_order_preserved(self):
        add_task("First", path=self.path)
        add_task("Second", path=self.path)
        titles = [t["title"] for t in load_tasks(self.path)]
        self.assertEqual(titles, ["First", "Second"])


if __name__ == "__main__":
    unittest.main()