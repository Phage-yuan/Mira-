PY ?= python3

# 用仓库里已有的数据重算全部结论（不联网，几秒钟）
repro:
	$(PY) src/analyze.py --name 第一批 data/batch1_local.csv
	@if [ -f data/batch2_mira.csv ]; then \
	  $(PY) src/analyze.py --name 第二批 data/batch2_mira.csv --json results/batch2.json; \
	  $(PY) src/analyze.py --name 合并 data/batch1_local.csv data/batch2_mira.csv --json results/pooled.json; \
	fi

# 重新抓第二批（联网，约 900 次请求、5–7 分钟；匿名额度每个 IP 每天约 1000 次）
fetch:
	$(PY) src/fetch_cd5.py --seeds 20261124,20261125,20261126 --per-seed 100 \
	  --exclude data/batch1_local.csv --out data/batch2_mira.csv --check 10 --log results/fetch_log.txt

# 现场演示：抽 5 篇，联网算 CD5 并用笨办法核对（约 20 次请求、10 秒）
demo:
	$(PY) src/fetch_cd5.py --seeds 7 --per-seed 5 --out results/demo.csv --check 5

.PHONY: repro fetch demo
