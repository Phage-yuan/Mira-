
第二批数据抓取报告：额度探测 + make fetch + 自检留痕

本报告记录第二批（batch2）OpenAlex 数据抓取的全过程留痕。抓取按固定脚本 src/fetch_cd5.py 执行，脚本逻辑、抽样参数、判定标准均未改动。本版在上一轮抓取记录的基础上做了一次只读核对与订正：所有数字来自留存日志与实际重算，本轮没有重新抓取、没有补数、没有修改 data/ 下任何文件。

一、本轮核对的性质与边界

本轮任务是"只读核对已完成的上游留痕"，不是重新执行抓取。核对时只用本地已存在的四份留痕文件（results/fetch_log.txt、results/fetch_stdout.txt、results/quota_probe.txt、data/batch2_mira.csv）做一致性重算，没有发出任何网络请求，也没有触碰脚本。data/batch2_mira.csv 在本工作区是 shared 副本的逐字节拷贝，sha256 与副本完全相同（3685ba99…），因此下游可以放心以它为输入。

核对发现上一轮报告存在若干表述与哈希层面的问题（详见第七节），本轮一并如实修订；抓取结果本身（294 篇、自检 10/10、主流程 885 次请求、729 秒）经重算全部成立。

二、留痕文件与可复核哈希

以下是当前工作区实际存在、且本轮逐字节计算过的文件指纹：

文件	sha256
shared/data/batch2_mira.csv（=data/batch2_mira.csv）	3685ba995e994322aeab4f5eac82e5f13400bc502af9829823c696a64eb9fa7b
shared/results/fetch_log.txt	cb966c00defbdc185fde081ade3d47e1995699dcae110053dffc30dd5714a208
shared/results/fetch_stdout.txt	c997a4394cd60b7e8f4eeb493852aff2a3c1fc01c0bca8c76d30ef4c77980e4f
shared/results/quota_probe.txt	d2aebd8d63e41b9f9c937dec4018cc3d9d426b7b40c98aff181f007850fdc194
shared/role_inputs/batch1_local.csv（第一批排除名单）	c3e089ab0136545326a2432c2eeadd1ca4f1b22c06a64d021a6dbf690152d674
shared/role_inputs/PROTOCOL.md	19c438683cf05c967124a55701b940c109114cdfb2a21246ba3f031afd49c6a1

复核命令示例：sha256sum results/fetch_log.txt results/fetch_stdout.txt results/quota_probe.txt data/batch2_mira.csv。

需要开口说明的一处缺口：上一轮报告曾给出 Makefile 与 src/fetch_cd5.py 的 sha256，但这两个文件在当前工作区已不存在（抓取时的工作目录未保留），本轮无法复核它们的哈希，因此不在上表列出。上表的 batch1_local.csv 哈希与上一轮报告中记录的 316e96… 不同，见第七节第 2 条。

三、额度探测（第 1 步）

抓取前用 curl 向 OpenAlex 发 1 次只读请求，把 HTTP 状态码与全部 x-ratelimit-* 响应头原样写入 results/quota_probe.txt：

1curl -sS -i -o - 'https://api.openalex.org/works?filter=cited_by_count:%3E0&per-page=1'

原始记录中的关键行（完整响应头与响应体见该文件）：

1HTTP/2 429
2retry-after: 11777
3x-ratelimit-limit: 1000
4x-ratelimit-remaining: 0
5x-ratelimit-reset: 11777
6{"error":"Rate limit exceeded","reason":"daily_budget","retryAfter":11777,"dailyRemainingUsd":0,...}

如实记录：这次不带 API key 的匿名探测返回 HTTP 429，x-ratelimit-remaining 原始值为 0，响应体说明匿名请求按 IP 共享的每日预算已用尽（$0 remaining; resets at midnight UTC），retry-after 为 11777 秒。curl 退出码为 0——HTTP 429 是服务端状态，不是 curl 自身报错。

这次 429 针对的是匿名共享额度池；随后 make fetch 运行时脚本检测到环境中有 OPENALEX_API_KEY（日志首行"密钥 有"），走的是密钥自己的额度池，起始剩余 8659，因此抓取正常完成。两条额度线相互独立，报告里不混为一谈。

四、抓取执行（第 2 步）与请求量核对

实际执行的命令（fetch_stdout.txt 首两行原样记录）：

1python3 src/fetch_cd5.py --seeds 20261124,20261125,20261126 --per-seed 100 \
2  --exclude data/batch1_local.csv --out data/batch2_mira.csv --check 10 --log results/fetch_log.txt

关键运行数字直接读自 results/fetch_log.txt：

指标	数值	出处
开始 / 结束	2026-11-21 20:43:48 → 20:56:05（Asia）	日志首行与末行
主流程用时	729 秒	"主流程请求 885 次，用时 729 秒"
墙钟总时长	737 秒（重算之差）	20:56:05 − 20:43:48
主流程请求次数	885 次	同上
算出篇数	294 篇	"算出 294 篇"
refs 不在 5–100 跳过	6 篇	同上
与第一批重复跳过	0 篇	同上
密钥池额度	起始 8659 → 结束 7765	日志首行与末行

请求次数构成可以逐项对上：3 个种子各 1 次随机抽样 + 294 篇各 1 次元数据请求 + 294 篇各 2 次参考文献分页请求 = 3 + 294 + 588 = 885，与日志计数一致（此分解为推算，依据是每篇 A 与 B 需分页抓取；不是日志逐条打印的值）。墙钟 737 秒与主流程 729 秒相差 8 秒，是自检与收尾开销，两者不矛盾。

五、自检逐行结果与汇总（10/10）

脚本用"把引用记录逐条抓下来本地数"的笨办法核了 10 篇，比较计数法与逐条法的 A、J。以下逐字取自 results/fetch_log.txt：

#	论文 id	计数法 A	计数法 J	逐条法 A	逐条法 J	结论
1	W1483624304	4	3	4	3	一致
2	W2057360632	3	3	3	3	一致
3	W2189873017	13	12	13	12	一致
4	W1976401013	2	2	2	2	一致
5	W2095428202	23	21	23	21	一致
6	W2137597219	12	12	12	12	一致
7	W2082713776	10	6	10	6	一致
8	W2073811760	13	12	13	12	一致
9	W2021354748	2	2	2	2	一致
10	W2060044351	6	6	6	6	一致

本轮用正则逐条重解析该日志，10 行明细的计数法 A/J 与逐条法 A/J 全部相等，结论均为"一致"，汇总为 10 / 10（0 篇不一致）。另外把这 10 个 id 回查 CSV，其 A、J 与日志中的计数法数值完全相等，说明计数结果正确落盘。按 PROTOCOL.md 的量具自检标准（A 与 J 必须全部一致），本批通过量具自检。

统计口径说明：日志中以"自检"开头的行共 11 行，其中 10 行为逐篇明细、1 行为汇总句"自检：10 / 10 篇两种办法一致"。直接用 startswith('自检') 计"一致"会得到 11，是因为汇总句也含"一致"二字，按明细口径应读作 10/10。

六、data/batch2_mira.csv 结构与重算核对

本轮对该文件做了只读重算（pandas 读入，不写回）：

项目	结果
字段	id, year, team, refs, A, B, J, cd5（8 列，顺序与验收要求一致）
数据行数	294（wc -l 为 295，含表头）
重复 id	0
cd5 空值	0
年份范围	2005–2015
A 合计 / B 合计	4251 / 1995072（与日志末段一致）
cd5 回代误差	max|cd5 − (A−2J)/(A+B−J)| = 9.97e-17

四个团队规模分组的分布（本轮按 team 列重数，合计 294）：

分组	篇数
1 人	43
2–3 人	102
4–7 人	118
8 人以上	31

team 原始人数完整分布（用于核对，合计 294）：1 人 43、2 人 54、3 人 48、4 人 39、5 人 40、6 人 21、7 人 18、8 人 10、9 人 6、10 人 4、11 人 1、12 人 3、13/14/15/16 人各 1、24 人 2、29 人 1。与第一批的 id 交集实测为 0 篇，与日志"重复跳过 0 篇"一致。

七、不一致与异常（如实记录，已升级）

本轮核对发现上一轮报告中若干需要订正或提请主管确认之处，逐条列明，不做美化。

协议写定时间与抓取时间的先后相反。PROTOCOL.md 正文写"写定时间：2026-11-22（北京时间），早于第二批数据的抓取"，但日志显示抓取发生在 2026-11-21 20:43:48（Asia），即抓取早于该日期。判定标准的内容本身未受影响，但"事前置定"这一说法在时间证据上站不住，必须提请主管核实协议实际写定时间，最终报告中不得据此宣称"标准先于数据固定"。
上一轮报告的输入哈希表无法复核。其中 data/batch1_local.csv 记为 316e96…，而现存文件为 c3e089…；Makefile 与 src/fetch_cd5.py 已不在工作区。本轮不沿用那组哈希，只列可复核值，并声明这两个文件当前缺失。
上一轮报告团队原始分布表述有误。其写作"13/14/15/16 各 1"，但同时把这一段的合计写作 4，实际为 13、14、15、16 人各 1 共 4 篇；本轮已按实测完整列出。
results/fetch_exit_code.txt 当前不存在。上一轮报告记录 make fetch 退出码为 0，但工作区没有该文件；现存 results/repro_exit_code.txt（exit=0）属于 make repro，不能挪来当 fetch 的退出码。本轮如实说明：抓取退出码 0 只能引用上一轮记录，无法独立复核。
匿名探测 429：这次探测失败属实，已完整留存原始响应头；它不代表抓取失败，因为抓取走密钥池。这一点在本报告第三节与第八节分别说明，不合并叙述。

以下为不影响结论的环境告警，一并照实记录：终端有 RequestsDependencyWarning: urllib3 (2.6.3) or chardet (7.7.0)/charset_normalizer (3.5.2) doesn't match a supported version，以及 curl 的 libcurl.so.4 no version information available，均为版本提示，不影响请求与结果。

八、结论与移交

第二批数据抓取在 OpenAlex 公开接口上完成：三个种子各抽 100 篇，算出 294 篇有效论文，主流程请求 885 次、用时 729 秒，自检 10/10 一致，密钥池额度剩余 7765。CSV 共 294 行，8 个字段齐全，cd5 无空值，A/B 合计与日志逐项吻合，cd5 回代误差在浮点精度内，满足 PROTOCOL.md 的样本量下限（≥150 篇）。

移交说明：本报告只负责抓取与留痕，不做打分或结论判定。统计分析可以 data/batch2_mira.csv 与 results/fetch_log.txt 为输入；最终报告在引用本批结论时，需同时写入第七节第 1 条的协议时间问题与第 4 条的退出码缺口，不得省略。

九、交付文件清单
文件	内容
results/quota_probe.txt	匿名额度探测的原始 curl 输出（含 HTTP/2 429 与 x-ratelimit-remaining: 0）
results/fetch_stdout.txt	抓取脚本的完整终端输出（含实际命令行与环境告警）
results/fetch_log.txt	脚本自写日志（逐篇自检、汇总、请求数与额度）
data/batch2_mira.csv	第二批 294 篇论文的指标表（id,year,team,refs,A,B,J,cd5）
shared/data_collection_report.md	本报告