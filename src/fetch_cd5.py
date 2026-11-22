"""从 OpenAlex 随机抽论文并计算颠覆性指标 CD5（计数法，每篇论文 3 次请求）。

CD5 定义（Funk & Owen-Smith 2017；Wu, Wang & Evans, Nature 2019 沿用）：
  发表后 5 年内，只引这篇论文的有 n_i 篇，既引它又引它参考文献的有 n_j 篇，
  只引它参考文献的有 n_k 篇；CD = (n_i - n_j) / (n_i + n_j + n_k)
计数法：不把引用记录逐条抓下来，只让接口返回"有多少篇"：
  A = 引这篇论文的篇数             = n_i + n_j
  B = 引它任一参考文献的篇数（去重） = n_j + n_k（要减掉这篇论文自己）
  J = 两者都引的篇数               = n_j
  CD5 = (A - 2J) / (A + B - J)
自检（--check K）：抽 K 篇，把引用者逐条抓下来在本地数一遍，A 和 J 必须与计数法一致。

用法：
  python3 src/fetch_cd5.py --seeds 20261124,20261125,20261126 --per-seed 100 \
      --exclude data/batch1_local.csv --out data/batch2_mira.csv --check 10 --log results/fetch_log.txt
只用标准库。匿名访问（每个 IP 每天约 1000 次请求）；如有 OpenAlex 密钥，设环境变量 OPENALEX_API_KEY。
额度用完会停下并保存已算出的部分，不会报废。
"""
import argparse, csv, json, os, sys, time, urllib.error, urllib.parse, urllib.request

BASE = "https://api.openalex.org/works"
FILTER = "type:article,publication_year:2005-2015,referenced_works_count:>4,cited_by_count:>0"
KEY = os.environ.get("OPENALEX_API_KEY", "")
N_REQ = 0
HDR = {}


class QuotaExhausted(Exception):
    pass


def get(params):
    """发一次请求；429（额度用完）直接抛出，其他错误重试 2 次。"""
    global N_REQ, HDR
    if KEY:
        params = dict(params, api_key=KEY)
    url = BASE + "?" + urllib.parse.urlencode(params, safe=":|,>-")
    req = urllib.request.Request(url, headers={"User-Agent": "research-script/1.0"})
    err = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                N_REQ += 1
                HDR = {a.lower(): b for a, b in r.headers.items()}
                time.sleep(0.11)
                return json.load(r)
        except urllib.error.HTTPError as e:
            N_REQ += 1
            if e.code == 429:
                raise QuotaExhausted(str(e))
            err = e
        except Exception as e:  # 网络抖动
            err = e
        time.sleep(2 * (attempt + 1))
    raise err


def short(wid):
    return wid.rsplit("/", 1)[-1]


def window(y):
    return f"from_publication_date:{y}-01-01,to_publication_date:{y + 5}-12-31"


def cd5_counts(f, y, refs):
    orr = "|".join(refs)
    win = window(y)
    A = get({"filter": f"cites:{f},{win}", "per-page": 1, "select": "id"})["meta"]["count"]
    B = get({"filter": f"cites:{orr},{win}", "per-page": 1, "select": "id"})["meta"]["count"] - 1
    J = get({"filter": f"cites:{f},cites:{orr},{win}", "per-page": 1, "select": "id"})["meta"]["count"]
    return A, B, J


def brute_force(f, y, refs):
    """笨办法：把 5 年内引用这篇论文的记录逐条抓下来，本地数 A 和 J（只用于 A<=200 的论文）。"""
    res = get({"filter": f"cites:{f},{window(y)}", "per-page": 200, "select": "id,referenced_works"})["results"]
    rs = set(refs)
    return len(res), sum(1 for c in res if rs & {short(x) for x in c["referenced_works"]})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", required=True, help="逗号分隔的随机种子")
    ap.add_argument("--per-seed", type=int, default=100, help="每个种子抽多少篇（接口上限 100）")
    ap.add_argument("--exclude", default="", help="已有结果 csv，里面出现过的论文跳过")
    ap.add_argument("--out", required=True)
    ap.add_argument("--check", type=int, default=10, help="用笨办法核对多少篇")
    ap.add_argument("--log", default="")
    a = ap.parse_args()

    lines = []

    def say(*x):
        s = " ".join(str(i) for i in x)
        print(s, flush=True)
        lines.append(s)

    seen = set()
    if a.exclude and os.path.exists(a.exclude):
        seen = {r["id"] for r in csv.DictReader(open(a.exclude, encoding="utf-8"))}
    rows, keep, skipped, dup, t0 = [], {}, 0, 0, time.time()
    say("开始", time.strftime("%Y-%m-%d %H:%M:%S %Z"), "种子", a.seeds, "每种子", a.per_seed, "密钥", "有" if KEY else "无（匿名）")
    stopped = ""
    try:
        for seed in [int(s) for s in a.seeds.split(",")]:
            sample = get({"filter": FILTER, "sample": a.per_seed, "seed": seed, "per-page": 100,
                          "select": "id,publication_year,referenced_works,authorships"})["results"]
            say("种子", seed, "抽到", len(sample), "篇；额度剩余", HDR.get("x-ratelimit-remaining"))
            for w in sample:
                f, y = short(w["id"]), w["publication_year"]
                refs = [short(r) for r in w["referenced_works"]]
                if f in seen:
                    dup += 1
                    continue
                if not (5 <= len(refs) <= 100):  # 接口一次最多"或"100 个值
                    skipped += 1
                    continue
                seen.add(f)
                A, B, J = cd5_counts(f, y, refs)
                d = A + B - J
                rows.append(dict(id=f, year=y, team=len(w["authorships"]), refs=len(refs), A=A, B=B, J=J,
                                 cd5=(A - 2 * J) / d if d > 0 else ""))
                keep[f] = (y, refs)
                if len(rows) % 50 == 0:
                    say("已算", len(rows), "篇，%.0f 秒，请求 %d 次" % (time.time() - t0, N_REQ))
    except QuotaExhausted as e:
        stopped = "额度用完，提前停止：" + str(e)
        say(stopped)
    main_req, main_sec = N_REQ, time.time() - t0

    ok = checked = 0
    try:
        for r in [x for x in rows if 0 < x["A"] <= 200][: a.check]:
            y, refs = keep[r["id"]]
            a2, j2 = brute_force(r["id"], y, refs)
            checked += 1
            good = (a2 == r["A"] and j2 == r["J"])
            ok += good
            say("自检", r["id"], "计数法 A=%d J=%d；逐条法 A=%d J=%d；%s" % (r["A"], r["J"], a2, j2, "一致" if good else "不一致"))
    except QuotaExhausted as e:
        say("自检阶段额度用完：", e)

    if rows:
        os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
        with open(a.out, "w", newline="", encoding="utf-8") as fh:
            wr = csv.DictWriter(fh, fieldnames=list(rows[0]))
            wr.writeheader()
            wr.writerows(rows)
    say("---")
    say("算出 %d 篇；参考文献数不在 5–100 而跳过 %d 篇；与已有样本重复跳过 %d 篇" % (len(rows), skipped, dup))
    say("主流程请求 %d 次，用时 %.0f 秒" % (main_req, main_sec))
    say("自检：%d / %d 篇两种办法一致" % (ok, checked))
    sa, sb = sum(r["A"] for r in rows), sum(r["B"] for r in rows)
    say("引用记录规模：A 合计 %d，B 合计 %d；逐条抓（每页 200 条）至少需 %d 次请求" % (sa, sb, (sa + sb) // 200))
    say("额度剩余：", HDR.get("x-ratelimit-remaining"), "；结束", time.strftime("%Y-%m-%d %H:%M:%S %Z"))
    if a.log:
        os.makedirs(os.path.dirname(a.log) or ".", exist_ok=True)
        open(a.log, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    if checked and ok != checked:
        sys.exit(2)  # 自检不过：数据不能用
    if stopped and not rows:
        sys.exit(3)


if __name__ == "__main__":
    main()
