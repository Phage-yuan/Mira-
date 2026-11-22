
统计分析结果：第二批数据按冻结口径的 H1 / H2 检验与四组占比

本文件按 PROTOCOL.md 写死的口径，对第二批数据（data/batch2_mira.csv）与两批合并数据运行 make repro，给出 H1、H2 的斜率、95% 自助法区间、按原文规则的判定，以及四个团队规模分组的篇数、CD5<0 占比与平均 CD5。src/analyze.py、Makefile、PROTOCOL.md 未做任何改动（sha256 与上传原件一致，见文末"输入完整性"）；自助法仍为 10000 次、随机种子 20261122。所有数字均抄自下列命令的实际输出，不手抄估算。

执行命令与终端留痕

主分析在 make repro 下顺序执行三次，完整终端输出用 tee 存档，退出码单独记录：

1make repro 2>&1 | tee results/repro_stdout.txt
2echo "exit=${PIPESTATUS[0]}" | tee results/repro_exit_code.txt

make repro 实际展开的三条命令（与 PROTOCOL.md 的统计方法一致）：

1python3 src/analyze.py --name 第一批 data/batch1_local.csv
2python3 src/analyze.py --name 第二批 data/batch2_mira.csv --json results/batch2.json
3python3 src/analyze.py --name 合并 data/batch1_local.csv data/batch2_mira.csv --json results/pooled.json

实测结果：results/repro_exit_code.txt 内容为 exit=0，三次运行全部正常结束，results/batch2.json 与 results/pooled.json 均正常写出。终端中出现的 RequestsDependencyWarning: urllib3 ... doesn't match a supported version 是运行环境的库版本提示，与计算无关，未影响任何数字。绘图命令为：

1python3 src/plot_share.py data/batch2_mira.csv results/fig_share.png

该脚本是新增的独立绘图脚本，不改动 analyze.py；它按同样的口径（cd5 为空不计、team<1 不计、分组边界 1 / 2–3 / 4–7 / ≥8）从同一份 data/batch2_mira.csv 重算四组数字，输出与 results/batch2.json 的 bins 逐项相同。

H1：延续型论文占比（CD5<0）对 log2(作者数) 的回归

H1 只用第二批数据。判定规则（PROTOCOL.md 原文）：区间下界大于 0 → "确认：团队越大，延续型论文占比越高"；区间跨过 0 → "未确认"；区间上界小于 0 → "方向相反"。

样本	斜率（每翻倍）	95% 自助法区间	判定	产生该数字的命令
第二批（n=294）	+0.0500	[+0.0026, +0.0966]	确认：团队越大，延续型论文占比越高（下界 +0.0026 > 0）	python3 src/analyze.py --name 第二批 data/batch2_mira.csv --json results/batch2.json
合并（n=614，仅作参考）	+0.0835	[+0.0485, +0.1178]	确认（下界 +0.0485 > 0）	python3 src/analyze.py --name 合并 data/batch1_local.csv data/batch2_mira.csv --json results/pooled.json
第一批（n=320，对照）	+0.1158	[+0.0680, +0.1644]	确认（下界 +0.0680 > 0）	python3 src/analyze.py --name 第一批 data/batch1_local.csv

第二批的 H1 区间下界 +0.0026 大于 0，按 PROTOCOL.md 的标准记"确认：团队越大，延续型论文占比越高"。需要如实说明两点：其一，这个区间离 0 很近（下界只有 0.0026），方向可靠但幅度估计不稳定；其二，PROTOCOL.md 自述第一批里"CD5<0 占比随团队上升"是看完数据后的事后发现、不能当结论，而本批（第二批）是在未看过的新数据上做的预先指定检验，因此这条 H1 判定属于对事前假设的检验结果。

H2：CD5 对 log2(作者数) 的回归

H2 用第二批数据，并按 PROTOCOL.md 要求另报两批合并的结果。判定规则（原文）：区间整体小于 0 → "方向复现"；跨过 0 → "未能复现方向"；整体大于 0 → "方向相反"。

样本	斜率（每翻倍）	95% 自助法区间	判定	产生该数字的命令
第二批（n=294）	−0.00157	[−0.00289, −0.00053]	方向复现（区间整体小于 0：上界 −0.00053 < 0）	python3 src/analyze.py --name 第二批 data/batch2_mira.csv --json results/batch2.json
合并（n=614）	−0.00169	[−0.00309, −0.00036]	方向复现（整体小于 0：上界 −0.00036 < 0）	python3 src/analyze.py --name 合并 data/batch1_local.csv data/batch2_mira.csv --json results/pooled.json
第一批（n=320，对照）	−0.00185	[−0.00437, +0.00042]	未能复现方向（区间跨过 0）	python3 src/analyze.py --name 第一批 data/batch1_local.csv

第二批 H2 的区间上界为 −0.00053，整体位于 0 以下，按标准记"方向复现"；两批合并后区间为 [−0.00309, −0.00036]，上界仍小于 0，同样记"方向复现"。作为对照，第一批单独看时区间跨过 0（上界 +0.00042），当时记"未能复现方向"。也就是说：单用第一批不足以下 H2 结论，加上第二批合并后才过线；第二批本身的区间也刚过线（上界离 0 只有约 0.0005），属于边界性通过，而不是强证据。

四个团队规模分组（第二批）

分组按 PROTOCOL.md：1 人 / 2–3 人 / 4–7 人 / 8 人以上。占比 = 组内 CD5<0 的篇数 ÷ 组内篇数；平均 CD5 为组内算术平均。数字原样抄自 results/repro_stdout.txt（make repro 的第二批一次运行）与 results/batch2.json。

分组	篇数	CD5<0 篇数	CD5<0 占比	平均 CD5
1 人	43	28	65.1%	−0.0010
2–3 人	102	78	76.5%	−0.0031
4–7 人	118	90	76.3%	−0.0033
8 人以上	31	26	83.9%	−0.0077
合计 / 整体	294	222	75.5%	−0.0034（中位 −0.0009）

上表的篇数、占比、平均 CD5 均为 analyze.py 与 plot_share.py 的直接输出；"CD5<0 篇数"一列是由"篇数 × 占比"反推得到的整数（28 / 78 / 90 / 26，合计 222，与整体 75.5% × 294 对应），属于推算值。本表只列第二批；合并样本的四组数字为 1 人 89 篇 51.7%、2–3 人 210 篇 67.6%、4–7 人 244 篇 73.8%、8 人以上 71 篇 78.9%（出自 results/pooled.json），仅供对照。

表格体现的模式是：占比从 1 人的 65.1% 升到 8 人以上的 83.9%，平均 CD5 从 −0.0010 降到 −0.0077，与 H1、H2 的斜率方向一致。但注意 2–3 人与 4–7 人两组的占比几乎相同（76.5% vs 76.3%），上升并非逐组单调。

对应图形为 results/fig_share.png：四根柱形按上述四组绘制，y 轴为百分比（0–100%），每根柱顶部标注 n，柱内标注占比；标题与坐标轴标签为中文，使用 Noto Sans CJK SC 字体渲染，已用图像检查确认无豆腐块。图中数字由 python3 src/plot_share.py data/batch2_mira.csv results/fig_share.png 的输出产生，打印结果为 1 人 n=43 65.1% / 2–3 人 n=102 76.5% / 4–7 人 n=118 76.3% / 8 人以上 n=31 83.9%，与上表逐项一致。

样本量与量具自检核对

PROTOCOL.md 规定：第二批有效论文少于 150 篇 → 记"数据不足，不下结论"；自检 10 篇必须 A、J 全部一致，有一篇不一致则整批不得用于下结论。逐条核对如下：

门槛	要求	第二批实际	是否达标	出处
样本量	≥ 150 篇	294 篇	达标	results/repro_stdout.txt 中"=== 第二批：n = 294"；results/batch2.json 的 "n": 294；data/batch2_mira.csv 共 294 行数据
量具自检	10/10 篇一致	10/10 一致，不一致 0 篇	达标	results/fetch_log.txt 的 10 行"自检 W… 一致"逐篇明细与汇总行"自检：10 / 10 篇两种办法一致"；shared/data_collection_report.md 第四节自检表
抓取退出码	正常结束	0	正常	shared/data_collection_report.md 第六节；results/fetch_log.txt 末行记录正常结束与额度剩余 7765

results/fetch_log.txt 中自检逐篇明细我逐行核对过：W1483624304 (A=4,J=3)、W2057360632 (3,3)、W2189873017 (13,12)、W1976401013 (2,2)、W2095428202 (23,21)、W2137597219 (12,12)、W2082713776 (10,6)、W2073811760 (13,12)、W2021354748 (2,2)、W2060044351 (6,6)，每一篇计数法与逐条法的 A、J 两个数都相同。据此两项门槛均达标，第二批数据可用于按 PROTOCOL.md 下结论，本文件的判定文字即为按标准给出的结果，未触发"数据不足，不下结论"或"自检未全过，数据不得用于下结论"。

哪些是实测、哪些是推算

实测（直接来自命令输出）：第二批 n=294；H1 斜率 +0.0500、区间 [+0.0026, +0.0966]；H2 斜率 −0.00157、区间 [−0.00289, −0.00053]；合并 H1 +0.0835 [+0.0485, +0.1178]、H2 −0.00169 [−0.00309, −0.00036]；第一批 H1 +0.1158 [+0.0680, +0.1644]、H2 −0.00185 [−0.00437, +0.00042]；四组篇数 43 / 102 / 118 / 31、占比 65.1% / 76.5% / 76.3% / 83.9%、平均 CD5 −0.0010 / −0.0031 / −0.0033 / −0.0077；整体均值 −0.0034、中位 −0.0009、占比 75.5%；自检 10/10 一致；退出码 0。

推算（由实测值派生，不是独立测量）：各组的 CD5<0 篇数（28 / 78 / 90 / 26，由篇数 × 占比取整）；"每翻倍"的表述是对 log2 斜率的口语化说明；"第二批区间离 0 很近"、"第二与第三组占比几乎相同"等定性描述，是对实测区间的读法。

输入完整性与未改动声明

Makefile、src/analyze.py、src/fetch_cd5.py、data/batch1_local.csv 均由上传原件逐字节复制，PROTOCOL.md 取自项目根目录原件；sha256 与上传原件逐一相等——Makefile 21050554…ec1d5、analyze.py 593d8a3a…e2cd5、fetch_cd5.py 5db1ea3b…424c6、batch1_local.csv 316e96bc…e42d6c8、PROTOCOL.md 19c43868…d49c6a1（其中前三个与 shared/data_collection_report.md 记录的校验值一致）。data/ 下文件未修改，第二批数据未重新抓取。PROTOCOL.md 的判定标准与自助法参数（10000 次、seed 20261122）未改动。

局限（按 PROTOCOL.md，不因结果好看而省略）

第二批只有 294 篇，未按学科、年代分层，8 人以上组仅 31 篇；CD5 用的是原始值而非原论文的全库百分位；OpenAlex 的引用数据与原论文用的 Web of Science 不是同一库；参考文献超过 100 篇的论文（6 篇）被排除。因此本文件的判定只是在"这批公开数据 + 这套冻结口径"下的结论，不等于对 Wu, Wang & Evans（2019）原文结论的全面复现；H2 与 H1 在第二批都只是刚过线。独立复核（PROTOCOL.md 的 1e-9 门槛）由审核成员执行，不在本文件范围内。

本次只读核对（产物一致性确认）

在移交审核与报告前，对本目录全部产物做了一次只读核对，未运行任何分析或绘图脚本、未改动自助法参数与判定标准、未改动数据。做法是把 results/batch2.json、results/pooled.json 的斜率/区间/判定与 results/repro_stdout.txt 逐项比对（斜率与区间按 4 位小数完全一致，H2 斜率取 5 位小数为 −0.00157 / −0.00169 也一致），并对 data/batch2_mira.csv 按 PROTOCOL.md 的分组边界独立重算四组篇数、占比、平均 CD5 与整体 CD5<0 占比，结果与表内数字逐项相同；再按原文判定规则由区间复算判定，与 JSON 中的判定一致。图形经视觉检查确认为有效 PNG（1860×1170），四根柱均带 n 标注与中文标签、无缺字方框。核对中发现一处笔误："输入完整性与未改动声明"中 batch1_local.csv 的 sha256 前缀原先漏写为 316e96bc…2d6c8，已按实际校验值改为 316e96bc…e42d6c8，不涉及任何数字、结论或脚本。