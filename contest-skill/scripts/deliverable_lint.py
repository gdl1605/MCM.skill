#!/usr/bin/env python3
"""
读什么：一个比赛工作目录或若干输出文件。
输出什么：中文交付物缺口报告，可选 JSON。
判定规则：检查路线图、完整通路、final answer artifact、摘要素材池、结论句和中文交付风格是否出现。
这不是：语义判卷器、自动修复器或复杂 CI 系统。
证据等级：[高频共性]；证据来源：output-contracts、minimum-deliverables-checklist、2025 gap 与跨年份回归总结。
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, Iterable, List, Sequence

TEXT_SUFFIXES = {".md", ".txt", ".csv", ".tsv", ".py", ".json"}

CHECKS = {
    "路线图/拆题": ["路线图", "全题拆解", "问题型判断", "主方案"],
    "至少一问完整通路": ["完整通路", "预处理", "结果表", "结论句"],
    "final answer artifact": ["final answer artifact", "最终推荐表", "最终排序表", "最终判定表", "方案表", "Top50"],
    "摘要素材池": ["摘要素材", "背景", "方法", "结果", "特点"],
    "验证或稳健性": ["验证", "稳健性", "灵敏度", "baseline", "对照"],
    "中文结论": ["综上", "因此", "最终", "建议", "判定", "结论"],
}


def iter_files(paths: Sequence[Path]) -> Iterable[Path]:
    for path in paths:
        if path.is_file() and path.suffix in TEXT_SUFFIXES:
            yield path
        elif path.is_dir():
            for child in path.rglob("*"):
                if child.is_file() and child.suffix in TEXT_SUFFIXES:
                    yield child


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def has_chinese(text: str) -> bool:
    return any("\u4e00" <= ch <= "\u9fff" for ch in text)


def run_checks(paths: Sequence[Path]) -> Dict[str, object]:
    files = list(iter_files(paths))
    combined = "\n".join(read_text(path) for path in files)
    details = []
    for name, keywords in CHECKS.items():
        hit = any(keyword in combined for keyword in keywords)
        details.append({"检查项": name, "通过": hit, "提示": "已发现相关交付痕迹" if hit else f"缺少关键词：{', '.join(keywords)}"})
    chinese_ok = has_chinese(combined)
    details.append({"检查项": "中文交付风格", "通过": chinese_ok, "提示": "含中文交付说明" if chinese_ok else "未发现中文内容，需检查是否偏英文"})
    return {
        "扫描文件数": len(files),
        "通过": all(item["通过"] for item in details),
        "检查结果": details,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="检查数学建模比赛目录是否具备最低交付物。")
    parser.add_argument("paths", nargs="+", help="要检查的目录或文件")
    parser.add_argument("--json", action="store_true", help="输出 JSON 而不是中文文本")
    args = parser.parse_args()

    report = run_checks([Path(p) for p in args.paths])
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"扫描文件数：{report['扫描文件数']}")
        for item in report["检查结果"]:
            mark = "通过" if item["通过"] else "缺口"
            print(f"[{mark}] {item['检查项']}：{item['提示']}")
        print("总体结论：" + ("可进入下一步审查" if report["通过"] else "仍有交付物缺口"))
    return 0 if report["通过"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
