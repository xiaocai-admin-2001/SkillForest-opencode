import unittest

import skill_registry_gui as gui


SAMPLE_ROWS = [
    {
        "ID": "skill-001",
        "Skill": "skill-registry",
        "Status": "active",
        "Agent": "OpenCode",
        "Source": "manual",
        "LocalPath": "C:/skills/skill-registry",
        "Installed": "2026-04-01",
        "LastUpdated": "2026-04-06",
        "Purpose": "维护技能注册表并提供可视化管理界面",
        "Notes": "常用",
    },
    {
        "ID": "skill-002",
        "Skill": "cek-brainstorm",
        "Status": "active",
        "Agent": "OpenCode",
        "Source": "manual",
        "LocalPath": "C:/skills/cek-brainstorm",
        "Installed": "2026-04-07",
        "LastUpdated": "2026-04-07",
        "Purpose": "把模糊想法逐步澄清成可执行设计",
        "Notes": "方案设计",
    },
    {
        "ID": "skill-003",
        "Skill": "tob-semgrep",
        "Status": "removed",
        "Agent": "OpenCode",
        "Source": "manual",
        "LocalPath": "C:/skills/tob-semgrep",
        "Installed": "2026-03-31",
        "LastUpdated": "2026-04-05",
        "Purpose": "用于安全审计、漏洞分析和风险检测",
        "Notes": "已停用",
    },
    {
        "ID": "skill-004",
        "Skill": "create-colleague",
        "Status": "active",
        "Agent": "OpenCode",
        "Source": "manual",
        "LocalPath": "C:/skills/create-colleague",
        "Installed": "2026-04-07",
        "LastUpdated": "2026-04-01",
        "Purpose": "把同事资料蒸馏成 AI Skill",
        "Notes": "新安装",
    },
]


class RegistryViewModelTests(unittest.TestCase):
    def test_index_registry_rows_builds_cached_search_blob(self):
        indexed = gui.index_registry_rows(SAMPLE_ROWS)

        self.assertEqual(indexed[0]["row"]["Skill"], "create-colleague")
        self.assertIn("新安装", indexed[0]["search_blob"])
        self.assertEqual(indexed[0]["status_label"], "启用")
        self.assertEqual(indexed[0]["top_category"], "未分类")

    def test_summarize_registry_rows(self):
        summary = gui.summarize_registry_rows(SAMPLE_ROWS)

        self.assertEqual(summary["total"], 4)
        self.assertEqual(summary["active"], 3)
        self.assertEqual(summary["removed"], 1)
        self.assertEqual(summary["categories"], 4)
        self.assertEqual(summary["latest"], "2026-04-07")

    def test_build_filter_options(self):
        filters = gui.build_filter_options(SAMPLE_ROWS)
        filter_map = {item["key"]: item for item in filters}

        self.assertEqual(filter_map["all"]["count"], 4)
        self.assertEqual(filter_map["active"]["count"], 3)
        self.assertEqual(filter_map["removed"]["count"], 1)
        self.assertIn("category:技能管理", filter_map)
        self.assertIn("category:规划实施", filter_map)
        self.assertIn("category:安全与测试", filter_map)
        self.assertIn("category:未分类", filter_map)

    def test_filter_skill_rows_by_category_and_query(self):
        filtered = gui.filter_skill_rows(
            SAMPLE_ROWS,
            selected_filter="category:规划实施",
            query="设计",
        )

        self.assertEqual([row["Skill"] for row in filtered], ["cek-brainstorm"])

    def test_filter_skill_rows_prioritizes_latest_install(self):
        filtered = gui.filter_skill_rows(SAMPLE_ROWS, selected_filter="all", query="")

        self.assertEqual(
            [row["Skill"] for row in filtered],
            ["create-colleague", "cek-brainstorm", "skill-registry", "tob-semgrep"],
        )

    def test_mousewheel_units_maps_delta_to_scroll_units(self):
        self.assertEqual(gui.mousewheel_units(120), -1)
        self.assertEqual(gui.mousewheel_units(-120), 1)
        self.assertEqual(gui.mousewheel_units(240), -2)
        self.assertEqual(gui.mousewheel_units(0), 0)

    def test_limit_visible_rows_reports_remaining_count(self):
        indexed = gui.index_registry_rows(SAMPLE_ROWS)
        visible, remaining = gui.limit_visible_rows(indexed, limit=2)

        self.assertEqual(
            [item["row"]["Skill"] for item in visible],
            ["create-colleague", "cek-brainstorm"],
        )
        self.assertEqual(remaining, 2)


if __name__ == "__main__":
    unittest.main()
