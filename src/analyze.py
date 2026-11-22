"""按 PROTOCOL.md 写死的口径做判定。只用标准库，固定随机种子，重跑结果逐位相同。

用法：
  python3 src/analyze.py --name 第二批 data/batch2_mira.csv
  python3 src/analyze.py --name 合并 data/batch1_local.csv data/batch2_mira.csv
  加 --json results/xxx.json 可把数字另存一份
"""
import argparse, csv, json, math, random

BOOT_N = 10000
BOOT_SEED = 20261122
BINS = (("1 人", 1, 1), ("2–3 人", 2, 3), ("4–7 人", 4, 7), ("8 人以上", 8, 10 ** 9))


def load(paths):
    rows, seen = [], set()
    for p in paths:
        for r in csv.DictReader(open(p, encoding="utf-8")):
            if r["cd5"] == "" or r["id"] in seen or int(r["team"]) < 1:
                continue
            seen.add(r["id"])
            rows.append((math.log2(int(r["team"])), float(r["cd5"]), int(r["team"])))
    return rows


def slope(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx if sxx > 0 else float("nan")


def boot_ci(xs, ys):
    """自助法（有放回重抽样）百分位 95% 区间。"""
    rng = random.Random(BOOT_SEED)
    n, out = len(xs), []
    for _ in range(BOOT_N):
        idx = [rng.randrange(n) for _ in range(n)]
        s = slope([xs[i] for i in idx], [ys[i] for i in idx])
        if s == s:
            out.append(s)
    out.sort()
    return out[int(0.025 * len(out))], out[int(0.975 * len(out)) - 1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--name", default="样本")
    ap.add_argument("--json", default="")
    a = ap.parse_args()
    rows = load(a.files)
    xs = [r[0] for r in rows]
    cd = [r[1] for r in rows]
    neg = [1.0 if c < 0 else 0.0 for c in cd]
    n = len(rows)
    res = {"name": a.name, "files": a.files, "n": n}
    print("=== %s：n = %d" % (a.name, n))

    s1 = slope(xs, neg)
    lo1, hi1 = boot_ci(xs, neg)
    v1 = "确认" if lo1 > 0 else ("方向相反" if hi1 < 0 else "未确认")
    print("H1 延续型占比：人数每翻倍，CD5<0 的占比变化 %+.4f，95%% 区间 [%+.4f, %+.4f] → %s" % (s1, lo1, hi1, v1))

    s2 = slope(xs, cd)
    lo2, hi2 = boot_ci(xs, cd)
    v2 = "方向复现" if hi2 < 0 else ("方向相反" if lo2 > 0 else "未能复现方向")
    print("H2 指标均值：人数每翻倍，CD5 变化 %+.5f，95%% 区间 [%+.5f, %+.5f] → %s" % (s2, lo2, hi2, v2))

    res.update(H1=dict(slope=s1, lo=lo1, hi=hi1, verdict=v1), H2=dict(slope=s2, lo=lo2, hi=hi2, verdict=v2), bins=[])
    for label, a0, b0 in BINS:
        g = [r for r in rows if a0 <= r[2] <= b0]
        if not g:
            continue
        share = sum(1 for r in g if r[1] < 0) / len(g)
        mean = sum(r[1] for r in g) / len(g)
        print("  %s：%d 篇，CD5<0 占 %.1f%%，平均 CD5 %+.4f" % (label, len(g), 100 * share, mean))
        res["bins"].append(dict(label=label, n=len(g), share_neg=share, mean_cd5=mean))
    cds = sorted(cd)
    res.update(mean=sum(cd) / n, median=cds[n // 2], share_neg=sum(neg) / n)
    print("  整体：平均 %+.4f，中位 %+.4f，CD5<0 占 %.1f%%" % (res["mean"], res["median"], 100 * res["share_neg"]))
    if a.json:
        json.dump(res, open(a.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
