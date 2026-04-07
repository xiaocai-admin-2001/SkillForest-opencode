import unittest
from datetime import datetime

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
    def test_extract_skill_usage_event_parses_skill_tool_record(self):
        part_data = {
            "type": "tool",
            "tool": "skill",
            "state": {"status": "completed", "input": {"name": "create-colleague"}},
        }

        event = gui.extract_skill_usage_event(part_data, 1775549140000)
        self.assertIsNotNone(event)
        assert event is not None

        self.assertEqual(event["skill"], "create-colleague")
        self.assertEqual(event["time_created"], 1775549140000)

    def test_canonical_skill_name_maps_runtime_name_to_local_skill(self):
        self.assertEqual(
            gui.canonical_skill_name("systematic-debugging"),
            "sp-systematic-debugging",
        )
        self.assertEqual(
            gui.canonical_skill_name("verification-before-completion"),
            "sp-verification-before-completion",
        )
        self.assertEqual(gui.canonical_skill_name("kaizen:why"), "cek-five-whys")
        self.assertEqual(
            gui.canonical_skill_name("create-colleague"), "create-colleague"
        )

    def test_get_skill_display_name_formats_prefixed_skills_clearly(self):
        self.assertEqual(
            gui.get_skill_display_name("sp-systematic-debugging"),
            "Superpowers 系统调试（sp-systematic-debugging）",
        )
        self.assertEqual(
            gui.get_skill_display_name("devops-helm-generator"),
            "DevOps · helm generator（devops-helm-generator）",
        )

    def test_summarize_skill_usage_counts_and_scores(self):
        events = [
            {"skill": "create-colleague", "time_created": 3000},
            {"skill": "create-colleague", "time_created": 2000},
            {"skill": "cek-brainstorm", "time_created": 1000},
            {"skill": "systematic-debugging", "time_created": 500},
        ]

        summary = gui.summarize_skill_usage(events)

        self.assertEqual(summary["create-colleague"]["usage_count"], 2)
        self.assertEqual(summary["create-colleague"]["usage_score"], 30)
        self.assertEqual(summary["create-colleague"]["score"], 30)
        self.assertEqual(summary["create-colleague"]["last_used_ts"], 3000)
        self.assertEqual(summary["cek-brainstorm"]["score"], 25)
        self.assertEqual(summary["sp-systematic-debugging"]["usage_count"], 1)

    def test_compose_skill_score_blends_quality_and_usage(self):
        self.assertEqual(gui.compose_skill_score(30, 90), 69)
        self.assertEqual(gui.compose_skill_score(0, 90), 72)
        self.assertEqual(gui.compose_skill_score(30, 0), 30)

    def test_merge_skill_metrics_combines_usage_and_quality_reviews(self):
        rows = [{"Skill": "cek-commit"}, {"Skill": "skill-registry"}]
        usage_summary = {
            "cek-commit": {
                "usage_count": 2,
                "usage_score": 30,
                "score": 30,
                "last_used_ts": 1000,
                "last_used": "2026-04-07 10:00",
            }
        }
        quality_reviews = {
            "cek-commit": {
                "quality_score": 90,
                "summary": "结构清晰",
                "reviewed_at": "2026-04-07 11:00",
                "recommendations": ["补一个输出模板"],
            }
        }

        merged = gui.merge_skill_metrics(rows, usage_summary, quality_reviews)

        self.assertEqual(merged["cek-commit"]["quality_score"], 90)
        self.assertEqual(merged["cek-commit"]["usage_score"], 30)
        self.assertEqual(merged["cek-commit"]["score"], 69)
        self.assertEqual(merged["skill-registry"]["score"], 0)

    def test_get_skill_recommendations_includes_opencode_best_practices(self):
        self.assertIn(
            "opencode-skill-best-practices",
            gui.get_skill_recommendations("cek-create-skill"),
        )
        self.assertIn(
            "opencode-skill-quality-reviewer",
            gui.get_skill_recommendations("opencode-skill-best-practices"),
        )

    def test_usage_overview_reports_total_invocations_and_recent_events(self):
        events = [
            {"skill": "create-colleague", "time_created": 3000},
            {"skill": "cek-brainstorm", "time_created": 2000},
            {"skill": "create-colleague", "time_created": 1000},
        ]

        overview = gui.build_usage_overview(events)

        self.assertEqual(overview["total_invocations"], 3)
        self.assertEqual(overview["recent_events"][0]["skill"], "create-colleague")
        self.assertEqual(overview["recent_events"][1]["skill"], "cek-brainstorm")

    def test_build_operations_dashboard_summary(self):
        usage_summary = {
            "skill-registry": {
                "usage_count": 6,
                "score": 50,
                "last_used_ts": 1_776_000_000_000,
                "last_used": "2026-04-11 10:00",
            },
            "cek-brainstorm": {
                "usage_count": 2,
                "score": 30,
                "last_used_ts": 1_776_100_000_000,
                "last_used": "2026-04-12 10:00",
            },
        }

        dashboard = gui.build_operations_dashboard(
            SAMPLE_ROWS,
            usage_summary,
            now_ts=1_776_120_000_000,
        )

        self.assertEqual(dashboard["summary"]["high_usage_count"], 1)
        self.assertEqual(dashboard["summary"]["active_7d_count"], 2)
        self.assertEqual(dashboard["summary"]["sleeping_count"], 1)
        self.assertEqual(dashboard["summary"]["average_score"], 27)
        self.assertEqual(dashboard["top_used"][0]["Skill"], "skill-registry")
        self.assertEqual(dashboard["recent_active"][0]["Skill"], "cek-brainstorm")
        self.assertEqual(
            dashboard["cleanup_candidates"][0]["Skill"], "create-colleague"
        )
        self.assertTrue(dashboard["insight_text"])

    def test_dashboard_preview_items_limits_length(self):
        items = [{"Skill": f"skill-{i}"} for i in range(6)]
        preview = gui.dashboard_preview_items(items, limit=3)

        self.assertEqual(
            [item["Skill"] for item in preview], ["skill-0", "skill-1", "skill-2"]
        )

    def test_operations_panel_toggle_label(self):
        self.assertEqual(gui.operations_panel_toggle_label(False), "收起运营面板")
        self.assertEqual(gui.operations_panel_toggle_label(True), "展开运营面板")

    def test_usage_summary_changed_detects_updates(self):
        previous = {
            "create-colleague": {"usage_count": 1, "score": 25, "last_used_ts": 1000}
        }
        current = {
            "create-colleague": {"usage_count": 2, "score": 30, "last_used_ts": 2000}
        }

        self.assertTrue(gui.usage_summary_changed(previous, current))
        self.assertFalse(gui.usage_summary_changed(current, current.copy()))

    def test_index_registry_rows_builds_cached_search_blob(self):
        usage_summary = {
            "create-colleague": {
                "usage_count": 2,
                "usage_score": 30,
                "quality_score": 0,
                "score": 30,
                "last_used_ts": 1775549140000,
            }
        }
        indexed = gui.index_registry_rows(SAMPLE_ROWS, usage_summary)

        self.assertEqual(indexed[0]["row"]["Skill"], "create-colleague")
        self.assertIn("新安装", indexed[0]["search_blob"])
        self.assertEqual(indexed[0]["status_label"], "启用")
        self.assertEqual(indexed[0]["top_category"], "未分类")
        self.assertEqual(indexed[0]["usage_count"], 2)
        self.assertEqual(indexed[0]["usage_score"], 30)
        self.assertEqual(indexed[0]["score"], 30)

    def test_index_registry_rows_supports_score_sort(self):
        usage_summary = {
            "skill-registry": {"usage_count": 1, "score": 25, "last_used_ts": 1000},
            "cek-brainstorm": {"usage_count": 5, "score": 45, "last_used_ts": 2000},
            "create-colleague": {"usage_count": 2, "score": 30, "last_used_ts": 3000},
        }

        indexed = gui.index_registry_rows(SAMPLE_ROWS, usage_summary, sort_mode="score")

        self.assertEqual(
            [item["row"]["Skill"] for item in indexed],
            ["cek-brainstorm", "create-colleague", "skill-registry", "tob-semgrep"],
        )

    def test_index_registry_rows_supports_usage_sort(self):
        usage_summary = {
            "skill-registry": {"usage_count": 1, "score": 25, "last_used_ts": 1000},
            "cek-brainstorm": {"usage_count": 5, "score": 45, "last_used_ts": 2000},
            "create-colleague": {"usage_count": 2, "score": 30, "last_used_ts": 3000},
        }

        indexed = gui.index_registry_rows(SAMPLE_ROWS, usage_summary, sort_mode="usage")

        self.assertEqual(
            [item["row"]["Skill"] for item in indexed],
            ["cek-brainstorm", "create-colleague", "skill-registry", "tob-semgrep"],
        )

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
        indexed = gui.index_registry_rows(SAMPLE_ROWS, {})
        visible, remaining = gui.limit_visible_rows(indexed, limit=2)

        self.assertEqual(
            [item["row"]["Skill"] for item in visible],
            ["create-colleague", "cek-brainstorm"],
        )
        self.assertEqual(remaining, 2)


if __name__ == "__main__":
    unittest.main()
