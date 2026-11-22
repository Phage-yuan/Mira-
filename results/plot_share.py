#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""按 PROTOCOL.md 的四个团队规模分组，画第二批数据的"CD5<0（延续型）论文占比"柱状图。

这是新增的独立绘图脚本，不读取、不修改 src/analyze.py 的任何计算逻辑。
判定口径与 src/analyze.py 保持一致（逐字复刻其 load() 过滤规则与 BINS 边界）：
  - cd5 为空的行不计入；
  - team < 1 的行不计入；
  - 重复 id 只保留首次出现（与 analyze.py 的 seen 集合一致）；
  - 分组：（1 人）1、（2–3 人）2–3、（4–7 人）4–7、（8 人以上）>=8；
  - CD5<0 ⇔ 延续型。

用法：
  python3 src/plot_share.py data/batch2_mira.csv results/fig_share.png
"""
import csv
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

BOOT_BINS = (("1 人", 1, 1), ("2–3 人", 2, 3), ("4–7 人", 4, 7), ("8 人以上", 8, 10 ** 9))


def pick_cjk_font():
    """选一个可用的中文字体，避免豆腐块；都找不到就返回 None。"""
    names = {f.name for f in fm.fontManager.ttflist}
    for cand in ("Noto Sans CJK SC", "Noto Sans CJK JP", "WenQuanYi Zen Hei",
                 "Droid Sans Fallback", "Source Han Sans SC"):
        if cand in names:
            return cand
    return None


def load_rows(path):
    rows, seen = [], set()
    for r in csv.DictReader(open(path, encoding="utf-8")):
        if r["cd5"] == "" or r["id"] in seen or int(r["team"]) < 1:
            continue
        seen.add(r["id"])
        rows.append((int(r["team"]), float(r["cd5"])))
    return rows


def main():
    csv_path = sys.argv[1] if len(sys.argv) > 1 else "data/batch2_mira.csv"
    out_path = sys.argv[2] if len(sys.argv) > 2 else "results/fig_share.png"
    rows = load_rows(csv_path)

    font = pick_cjk_font()
    if font:
        plt.rcParams["font.sans-serif"] = [font, "DejaVu Sans"]
    else:
        print("[WARN] 未找到中文字体，改用英文标签")
    plt.rcParams["axes.unicode_minus"] = False

    labels, stat = [], []
    for label, a0, b0 in BOOT_BINS:
        g = [c for t, c in rows if a0 <= t <= b0]
        if not g:
            continue
        share = sum(1 for c in g if c < 0) / len(g)
        labels.append(label)
        stat.append((len(g), share, sum(g) / len(g)))
        print("%s: n=%d, CD5<0 share=%.4f (%.1f%%), mean_cd5=%+.4f"
              % (label, len(g), share, 100 * share, sum(g) / len(g)))
    print("total n = %d" % len(rows))

    zh = font is not None
    fig, ax = plt.subplots(figsize=(6.2, 3.9), dpi=300)
    shares = [s[1] * 100 for s in stat]
    bars = ax.bar(range(len(labels)), shares, width=0.62, color="#0072B2",
                  edgecolor="black", linewidth=0.6, zorder=3)
    for i, (b, (n, share, _mean)) in enumerate(zip(bars, stat)):
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 1.4,
                "n=%d" % n, ha="center", va="bottom", fontsize=8.5, zorder=4)
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() / 2,
                "%.1f%%" % (100 * share), ha="center", va="center",
                fontsize=8.5, color="white", fontweight="bold", zorder=4)

    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels if zh else ["1", "2-3", "4-7", "8+"])
    ax.set_ylim(0, 100)
    ax.set_yticks(range(0, 101, 20))
    ax.set_yticklabels(["%d%%" % v for v in range(0, 101, 20)])
    if zh:
        ax.set_xlabel("团队规模（作者数）")
        ax.set_ylabel("CD5<0（延续型）论文占比")
        ax.set_title("第二批 OpenAlex 样本：延续型论文占比随团队规模上升（n=%d）" % len(rows),
                     fontsize=10)
    else:
        ax.set_xlabel("Team size (authors)")
        ax.set_ylabel("Share of papers with CD5 < 0 (consolidating)")
        ax.set_title("Batch 2 (OpenAlex): share of consolidating papers by team size (n=%d)" % len(rows),
                     fontsize=10)
    ax.yaxis.grid(True, color="0.85", linewidth=0.6, zorder=0)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    fig.tight_layout()
    fig.savefig(out_path, dpi=300, facecolor="white")
    print("saved:", out_path)


if __name__ == "__main__":
    main()
