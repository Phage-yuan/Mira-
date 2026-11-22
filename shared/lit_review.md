
文献核对报告：CD 指标定义、5 年窗口出处与公式等价性推导

本报告核对两篇一手文献的元数据与 DOI，说明 CD（颠覆性）指标与 5 年引用窗口（即 CD5）各自的原始出处，给出 src/fetch_cd5.py 中 CD5 = (A − 2J)/(A + B − J) 与文献定义 (n_i − n_j)/(n_i + n_j + n_k) 之间等价性的完整代数推导及其成立所依赖的假定，并如实记录原论文结论方向与查不到的条目。本报告只做核对，不修改任何上传文件，也未运行任何联网抓数命令；文中所有数字均来自本次实际的页面抓取或本地计算。

一、两篇文献的元数据与 DOI

两篇文献的元数据均通过出版社页面与 Crossref 公共记录双向核对一致，DOI 均可解析，不存在"查不到"的情况。

1. Wu, Wang & Evans (2019)

作者：Lingfei Wu、Dashun Wang、James A. Evans
标题：Large teams develop and small teams disrupt science and technology
刊物与卷期页码：Nature，volume 566，issue 7744，pp. 378–382（2019）
出版日期：在线首发 2019-02-13；纸版 2019-02-21
DOI：10.1038/s41586-019-0941-9
核对来源：Nature 文章页（S1）与 Crossref 记录（S2）一致；Europe PMC（S5）给出同一 DOI 与 PMID 30760923。Crossref 记录中原样字段为 "page":"378-382"、"volume":"566"、"issue":"7744"、"issued":{"date-parts":[[2019,2,13]]}。
参考格式：Wu, L., Wang, D. & Evans, J. A. Large teams develop and small teams disrupt science and technology. Nature 566, 378–382 (2019). https://doi.org/10.1038/s41586-019-0941-9

2. Funk & Owen-Smith (2017)

作者：Russell J. Funk、Jason Owen-Smith
标题：A Dynamic Network Measure of Technological Change
刊物与卷期页码：Management Science，volume 63，issue 3，pp. 791–817（2017 年 3 月号；Articles in Advance 在线版 2016-03-22）
DOI：10.1287/mnsc.2015.2366
核对来源：Crossref 记录（S3，出版方字段为 INFORMS）与作者公开提供的期刊排版 PDF（S4，页眉标注"Vol. 63, No. 3, March 2017, pp. 791–817"且 PDF 自带引用行含该 DOI）一致；Nature 2019 的参考文献第 22 条亦以同一 DOI 引用此文（S1）。
二、CD 指标与 5 年窗口的出处

CD 指标的一手定义出自 Funk & Owen-Smith 2017（下文简称 F&OS），Wu, Wang & Evans 2019（下文简称 WWE）直接沿用并改称"D"（disruption）。5 年窗口的原始依据同样见于 F&OS 正文，WWE 则把 5 年窗口作为主口径并在补充材料中做了从 5 年到 40 年的稳健性检验。

2.1 F&OS 2017 原文的算子定义

以下逐字引用来源 S4，第 794–795 页。原文先定义三类未来专利 i，再给出公式：

"New patents may join in one of three ways: (1) i can cite the focal patent's predecessors (type b), (2) i can cite the focal patent (type f ), or (3) i can cite the focal patent and its predecessors (both types f and b)."

"CD t ≡ 1/n_t Σ_{i=1}^{n_t} [(−2 f_it b_it + f_it) w_it], w_it > 0, (1)"

其中 f_it 与 b_it 的定义为（原文式 (2)(3)）：

"f_it = 1 if i cites the focal patent (type f ), 0 otherwise" "b_it = 1 if i cites any focal patent predecessors (type b), 0 otherwise"

"where n_t is the number of forward citations in i" "We emphasize that n_t is the number of forward citations of both the focal patent and/or its technological predecessors"

"The multiplication by −2 in the numerator of Equation (1) ensures that the measure ranges from −1 to 1, with positive values representing inventions that are more destabilizing and negative values highlighting inventions that are more consolidating."

把上式逐项求和展开即可得到按三类计数写的形式：令 n_i = 只引焦点文献的篇数（f=1, b=0）、n_j = 既引焦点文献又引其参考文献的篇数（f=1, b=1）、n_k = 只引焦点文献参考文献的篇数（f=0, b=1），则分子求和 = n_i − n_j，分母 n_t = n_i + n_j + n_k，故

CD = (n_i − n_j) / (n_i + n_j + n_k)

这一点可由前述逐字定义直接代数展开验证，不需要外部假设。

2.2 WWE 2019 对三类计数的图示说明

来源 S1，Extended Data Fig. 5g 图注，逐字：

"Simplified citation networks comprising focal papers (blue diamonds), references (grey circles) and subsequent work (rectangles). Subsequent work may cite: (1) only the focal work (i, green), (2) only its references (k, black) or (3) both focal work and references (j, brown)."

同一图注还列出 D_0（正文主口径）、D_1（剔除自引）、D_2（只看热门参考文献）、D_3 = n_i/(n_i + n_j)、D_4（按引文条数而非篇数计）等变体，并注明"D_0 is the definition of disruption used in the main text"。这说明 WWE 的 n_i / n_j / n_k 与 F&OS 的计数口径一一对应，WWE 只是把 CD 改称为 D。

2.3 5 年窗口的出处

来源 S4，逐字：

"When calculated five years after the focal patent's issue date, undefined values of the CD t and mCD t indexes were rare, occurring in only 82,572 cases of 2.9 million, a rate of 2.8%."

"Most of our analyses in this and later sections evaluate impact and the CD t and mCD t indexes using forward citations made during the first five years after the focal patent's issue, because annual citations of most patents reach their peak within this time frame (Jaffe and Trajtenberg 2002). We denote these quantities as I5, CD 5, and mCD 5, respectively."

即：CD5 的"5"就是"焦点文献发表（专利为授权）后前 5 年内的前向引用"这一窗口；窗口长度取 5 年的原始理由是"多数专利的年引用量在此区间内达到峰值"，作者并注明所依据的文献为 Jaffe & Trajtenberg (2002)。F&OS 还给出了该窗口下 CD5 的分布：均值 0.07、标准差 0.23、取值范围 [−1, 1]。

2.4 WWE 2019 的窗口用法

WWE 正文把 5 年窗口作为主口径（其补充图以"5 years to 40 years"的时间窗变化做稳健性检验）：Extended Data Fig. 3 的 d–h 子图说明为"robust to changes in the width of the time-window of observation from 5 years to 40 years"（样本为 1970 年发表的 166,310 篇 WOS 论文），i–m 子图对 1954–2014 年的 24,174,022 篇论文重复同样的检验（S1）。另有一篇 2025 年的开放获取论文（S6）在方法部分明确写道，文献中"often done"的做法是"compute the disruption score of a paper using … papers published in the following 5 years"，并以 WWE 2019 作为该做法的出处，可作为二手旁证。

需要如实说明的一点：WWE 正文中 CD 公式的逐字表述位于付费墙内，本次未能取得正文（详见第六节"查不到"清单）。因此本报告对 WWE 之处仅引用其公开摘要、参考文献与 Extended Data 图注中可核对的文字，公式本身的一手出处归于 F&OS，这是可核对的、且是更原始的来源。

三、关键等价性：完整代数推导

本节把 src/fetch_cd5.py 实际计算的 CD5 = (A − 2J)/(A + B − J) 与文献定义 (n_i − n_j)/(n_i + n_j + n_k) 放在一起逐项对应：先说明脚本中 A、B、J 三个计数分别对应文献的哪几类后续文献（3.1），再给出逐步代数推导（3.2），然后用符号运算与精确有理数数值做验证（3.3），接着明确等价性成立所需的数据层面假定（3.4），最后单独处理脚本中 B − 1 这一处口径差异（3.5、3.6）。

3.1 记号与脚本中的 A、B、J

src/fetch_cd5.py 的文档字符串与 cd5_counts() 函数给出如下口径（下文称"计数法"）：

A = cites:{焦点文献} 在 5 年窗口内的篇数 = n_i + n_j
B = cites:{焦点文献的任一参考文献} 在 5 年窗口内的篇数，再 减 1（脚本原文 ... ["meta"]["count"] - 1，注释为"要减掉这篇论文自己"）
J = cites:{焦点文献},cites:{任一参考文献} 在 5 年窗口内的篇数 = n_j
CD5 = (A − 2J) / (A + B − J)
3.2 逐步推导

设 n_i、n_j、n_k 均为非负整数，且分母不为零。

第一步（A 展开）：A = n_i + n_j。5 年窗口内引用焦点文献的每一篇后续文献，要么只引焦点文献（n_i 类），要么同时引用焦点文献的参考文献（n_j 类），两类互斥且穷尽，故求和即得。

第二步（J 展开）：J = n_j。既引焦点文献又引其任一参考文献的后续文献，正是 n_j 类。

第三步（B 展开，这一处需要一个假定）：设脚本返回的原始计数为 C = B + 1（因为脚本减了 1）。若假定"5 年窗口内引用焦点文献参考文献集合的后续文献，恰好落在 n_j ∪ n_k 两类之中，没有其他文献被误计入"，则 C = n_j + n_k，于是 B = n_j + n_k − 1。下文先用一般记号把"−1"写成"−k"（即 B = n_j + n_k − k）以便看清差异来源，最后再代入 k = 1。

第四步（分子化简）： A − 2J = (n_i + n_j) − 2n_j = n_i − n_j。

第五步（分母化简，k = 0 的情形）： A + B − J = (n_i + n_j) + (n_j + n_k) − n_j = n_i + n_j + n_k。

第六步（合并）： (A − 2J)/(A + B − J) = (n_i − n_j)/(n_i + n_j + n_k)。

至此，"A + B − J"与文献分母"n_i + n_j + n_k"是两个恒等相等的表达式（第五步），分子也恒等相等（第四步），因此在第三步的假定下，两式作为有理函数完全相等。

3.3 计算验证（实际运行输出）

符号验证（sympy，把 n_i、n_j、n_k 设为正数符号，A = n_i+n_j、B = n_j+n_k、J = n_j）：

simplify((A-2J)/(A+B-J)) = (ni - nj)/(ni + nj + nk)
simplify(LHS - RHS)      = 0
symbolic identity holds  : True
denominator LHS expanded : ni + nj + nk


数值验证（有理数精确算术，n_i、n_j、n_k 各自独立均匀取 0–500 的整数，共 200,000 组）：

随机整数检验次数 200000，不等次数 = 0  最大绝对误差 = 0.0


两项都表明：在"B = n_j + n_k"的假定下，等价性是严格相等，而非近似。

3.4 等价性是严格还是近似：结论与前提

结论：在 B = n_j + n_k 的假定成立时，等价性是严格代数恒等（符号与数值检验均给出零差）；若该假定不成立（B 的实际原始计数不等于 n_j + n_k），则两式只是"口径近似"而非恒等。因此把等价性定性为"严格"时，必须同时声明它所依赖的假定。

成立所依赖的三个假定：

集合完全一致：5 年窗口内"引用焦点文献任一参考文献"的后续文献集合，与文献定义的"引用焦点文献的前驱集合"（F&OS 中称 focal patent's predecessors）是同一个集合。若 OpenAlex 的 referenced_works 与 F&OS / WWE 所用"参考文献"范围不同（例如 WWE 用 WOS 收录的参考文献），则 n_k 与 n_j 的计数基础不同，此假定被削弱。
sum 与 count 口径一致：OpenAlex 的 meta.count 统计的是"文献（篇）数"而非"引用条数"，且不受分页影响；否则 A、B、J 与文献的 n_i、n_j、n_k 不同量纲。
文献定义本身已去重：F&OS 的 b_it 定义为"cites any focal patent predecessors"，即按后续文献去重计 1 篇（原文式 (3)），与 OpenAlex cites:{参考集合}"引用任一即算一篇"的语义相同。这正是 B 可以被理解为"引用任一参考文献的篇数"的原因：一个后续文献即使多次引用同一参考文献或引用多篇参考文献，也只计 1 篇，因为规则按"篇"而非按"边"计数，所以不会重复计数。该假定可直接在 F&OS 原文核对。

据此可以把严格性拆开来说，以免误导下游：

"引用焦点文献的篇数 A"与"两者都引的篇数 J"：与 n_i+n_j、n_j 的对应是定义级的，不需要额外假定。
"引用其任一参考文献的篇数 B"与"n_j+n_k"的对应：需要一个数据层面的假定（上面 1–3），它不是逻辑恒等式，而是该接口的计数语义恰好与 b_it 的定义对齐。因此严格地说，分母项的严格性是有条件的严格。
3.5 脚本中的"− 1"是什么意思

脚本里 B = ... - 1 的写法和注释"要减掉这篇论文自己"存在一个真实的口径问题，这里如实指出：

语义层面：如果 B 的原始计数是"引用焦点文献参考文献集合的篇数"，那么按 b_it 的定义，n_j 与 n_k 两类文献都不会是焦点文献本身（焦点文献不可能在 5 年窗口内引用自己，因为引用必须指向时间上更早的文献，而焦点文献的参考文献都比它更早）。因此在"引用其参考文献的篇数"这个口径下，不存在"焦点文献自己"被计入的问题，这个"− 1"在理论上没有依据。

数值层面：把它写成"− k"，则实际计算的是 (A − 2J)/(A + B − J) 而 B = n_j + n_k − k，它等于

(n_i − n_j) / (n_i + n_j + n_k − k)

只有当 k = 0 时与文献式严格相等；k = 1 时两者差值为一个小量（见 3.6 节，均为有理数精确值）。

本批数据上的量级（2026-11-22 只读复核时用 fractions.Fraction 对 320 行原样精确重算；偏移定义为 Δ = CD5(B) − CD5(B+1)，即"脚本值 − 文献式值"）：data/batch1_local.csv（320 篇）中，Δ 的均值约 +1.49×10⁻⁴、中位数约 −1.59×10⁻⁸，范围 [−2.02×10⁻³, +4.76×10⁻²]，最大偏移来自 A=2、B=4、J=0 的一篇（编号 W2319460288）；Δ>0 的 70 篇、Δ<0 的 202 篇、Δ=0 的 48 篇，没有任何一篇的 CD5 正负号发生翻转（320 篇符号全部不变）。也就是说，这个"− 1"带来的是系统性的小正偏移：多数论文的偏移近于 0（中位数约 −1.6×10⁻⁸，可忽略），少数 A 很小而 B 也很小的论文（分母 ~10 量级）偏移可达 10⁻² 量级，这些少数大偏移把均值抬到 +1.49×10⁻⁴。由于 B 常常远大于 A（例如某篇 A=19、B=2502），分母变化占比极小，所以在"CD5<0 占比"这类符号判断上不会改变判定，但在个体 CD5 数值与边际效应上会造成偏差。

更正说明：本轮上一轮版本此处写为"均值约 −1.49×10⁻⁴……202 篇偏移为正、70 篇为负"，属符号写反（量级本身正确，成因是把"文献式 − 脚本式"的结果误标为"脚本式 − 文献式"）。2026-11-22 本轮只读复核用精确有理数重算发现并已按实测更正；结论（"− 1"无理论依据、偏移量级小、不翻转任何符号、不影响 H1 判定）不受影响。核验过程见 artifacts/recheck_notes.md。

是否影响 PROTOCOL 判定：按当前证据不影响 H1（320/320 符号未翻转）；但它属于计算口径与文献定义不完全一致的问题。按任务约定我不改脚本、不改 PROTOCOL，只把决定权交回主管：如果最终报告要写"与文献严格等价"，应披露这一口径差异，或另开任务把这一行改为不减并重跑第二批（约 900 次请求）。在此标记：需主管升级（是否处理由主管决定）。

3.6 k 取值对两式差异的示意

以下为有理数精算结果（由 Python fractions.Fraction 计算）：

n_i	n_j	n_k	k = 0（文献式）	k = 1（脚本）	k = 1 相对 k = 0 的差
10	5	20	1/7	5/34	+1/238（≈ +0.00420）
3	0	50	3/53	3/52	+3/2756（≈ +0.00109）
0	4	100	−1/26	−4/103	−1/2678（≈ −0.00037）
5	2	30	3/37	1/12	+1/444（≈ +0.00225）

可见当 A 远小于 B 时差异极小，但当 A 与 B 同量级、或 k 与 n_k 的相对比例变大时差异不可忽略。这条表也说明：文献式与脚本式的差别不是近似技巧，而是 k 是否为零的差别。

四、原论文的主要结论

本节只记录能从原论文公开文字中直接核对到的结论方向，不转述二手综述。WWE 2019 的结论方向取自其公开摘要与 Extended Data 图注（正文付费墙不可及），F&OS 2017 的结论取自作者公开的期刊排版 PDF。最后单独说明两篇文献在"团队规模—颠覆性"方向上的差别，以免下游误用。

4.1 WWE 2019 的方向与作者的解释口径

以下以 S1 摘要逐字与 Extended Data 图注为限，S1 摘要与 S5 摘要相互一致：

数据规模与时段："more than 65 million papers, patents and software products that span the period 1954–2014"。
主结论（方向）："smaller teams have tended to disrupt science and technology with new ideas and opportunities, whereas larger teams have tended to develop existing ones"。即团队越大，越倾向于"发展（develop）"而非"颠覆（disrupt）"。
作者给出的解释口径：大团队的工作"builds on more-recent and popular developments, and attention to their work comes immediately"；小团队的工作"search more deeply into the past, are viewed as disruptive to science and technology and succeed further into the future—if at all"。（这一"深挖过去 / 紧贴近期"的机制，在 Extended Data Fig. 6 中被量化为参考文献年龄分布 P(t) ~ e^{−λt}、λ ~ m^{0.07} 一类关系。）
异质性：差异在"higher-impact work"上被放大（"small teams known for disruptive work and large teams for developing work"）。
机制归因："Differences in topic and research design account for a small part of the relationship…; most of the effect occurs at the level of the individual, as people move between smaller and larger teams"。
政策口径：两类团队都必要，"science policies should aim to support a diversity of team sizes"。
4.2 与 F&OS 方向叙述的差别

F&OS 2017 在专利数据上报告，发明人数与 CD5 的相关系数是正的（S4："the small positive correlation between the number of inventors and the CD 5 (r = 0.02, p < 0.001)"），而 WWE 2019 在论文数据上报告的是负关系。两者不矛盾，但数据对象（专利 vs 论文）、测量窗口与样本都不同，引用时必须标明，不能把 F&OS 当作"大团队更颠覆"论据，也不能把 WWE 的数字套给专利。

五、查不到清单

以下条目在本次检索中查不到，故不填写，也不凭印象补全。每条附上尝试过的检索路径与查询词。

WWE 2019 正文中 CD 公式的逐字原文：查不到。Nature 文章页为付费墙，仅公开摘要；Europe PMC 仅提供摘要、未收录免费全文；PubMed 页面返回 CAPTCHA 验证。已尝试：Nature 文章页（S1）、Europe PMC（S5）、PubMed（被拦截）、DuckDuckGo 查询 "Large teams develop and small teams disrupt" PMC full text disruption index formula；未找到可访问的 arXiv 预印本或机构库全文。可替代的一手证据是 F&OS 原文（S4）与 WWE Extended Data Fig. 5g 图注（S1）。
WWE 2019 正文中"5 年窗口"的逐字表述句：查不到（已尝试同上）。可核对的是其摘要、Extended Data Fig. 3（5→40 年稳健性）及 S6 的二手转述。
WWE 2019 正文中 CD5 回归的具体系数：未能取得正文，因此本报告不声称任何正文系数（回看图注只提到回归控制年份、主题与作者，没有可核对的整数系数）。
Jaffe & Trajtenberg (2002) 原文：仅作为 F&OS 中"5 年窗口"理由的被引文献，未找到原文正文，本报告未引用其任何具体数字。
六、"需主管升级"事项

按任务约定，本报告不修改 PROTOCOL.md、Makefile、src/*.py、data/*。但有一条问题影响到"与文献定义严格等价"这一表述的可核实性：src/fetch_cd5.py 中对 B 做了减 1（见 3.5 节）。按文献中 b_it 的定义，"引用焦点文献任一参考文献"的后续文献里不会包含焦点文献自身，所以这个减 1 在理论上无依据；在 batch1 的 320 篇上它使 CD5 产生系统性的小偏移（Δ 均值约 +1.49×10⁻⁴，中位数约 −1.59×10⁻⁸，最大约 +4.76×10⁻²；Δ>0 的 70 篇、Δ<0 的 202 篇），但未翻转任何一篇的 CD5 符号（320 篇中符号全部不变）。建议主管在最终报告中如实披露该口径差异，或另开任务修正后重跑，以便"等价性"的表述与代码实际执行一致。

七、检索记录

本节列出本次实际访问并用于取证的页面（含取用范围），以及被拒绝采用的检索结果。

编号	来源类型	URL	用途	结论
S1	出版社文章页（Nature）	https://www.nature.com/articles/s41586-019-0941-9	WWE 元数据、摘要、参考文献 22、Extended Data Fig. 5g/3 图注	采用
S2	Crossref 公共记录	https://api.crossref.org/works/10.1038/s41586-019-0941-9	WWE 卷期页码与 DOI 核对	采用
S3	Crossref 公共记录	https://api.crossref.org/works/10.1287/mnsc.2015.2366	F&OS 卷期页码、出版方与 DOI 核对	采用
S4	作者公开的期刊排版 PDF	https://public.websites.umich.edu/~jdos/papers/A_Dynamic_Network_Measure_of_Technological_Change.pdf	F&OS 原文式 (1)(2)(3)、n_t 定义、CD5 与 5 年窗口理由、CD5 分布、发明人数与 CD5 相关系数	采用
S5	Europe PMC	https://europepmc.org/article/MED/30760923	WWE 摘要与 DOI/PMID 交叉核对	采用
S6	开放获取二手文献（Scientific Reports 2025, Li, Livan & Righi）	https://www.nature.com/articles/s41598-025-95264-8	旁证：文献中"following 5 years"的 CD5 做法与 D 公式形态	作为二手旁证采用，不当作一手定义

检索查询词（DuckDuckGo，实际使用）：Wu Wang Evans "Large teams develop and small teams disrupt science and technology" Nature 2019 DOI；Funk Owen-Smith "A dynamic network measure of technological change" Management Science 2017 DOI；Wu Wang Evans 2019 disruption "n_i" "n_j" "n_k" CD index definition "5 years" preprint arXiv；"Large teams develop and small teams disrupt" PMC full text disruption index formula；"Large teams develop and small teams disrupt science and technology" full text pdf knowledge lab uchicago OR arxiv.org 1902。

未采用的检索结果：搜索引擎返回的 www.google.com/goto?url=... 跳转链接（非原始页面，无法核对原文）；ResearchGate 论文页（需登录，未见正文）；PubMed 页面（返回 CAPTCHA 验证页，未取得内容）。

本地计算与本地文件：data/batch1_local.csv（只读，320 行）用于量化"− 1"在真实数据上的偏移；计算工具为 Python + sympy + fractions.Fraction，实际输出已粘贴在第 3.3、3.5、3.6 节。核对过程中未运行任何联网抓数脚本，未写入 data/、results/、src/ 下任何文件。

八、本轮只读复核记录（2026-11-22）

本节记录对本报告与 shared/lit_findings.json 的第二次只读复核：确认两份产物可读、完整，并把所有可在线核对的元数据与原文引文重新独立核对一遍。复核不改变第 1–6 节的任何结论，只更正了第 3.5 节与第 6 节里一处写反符号的数字（见下第 3 条）。

DOI 与卷期页码：通过 Crossref 公共接口重新解析两个 DOI，与第 1 节完全一致——WWE 2019 为 Nature 566(7744):378-382，online 2019-02-13、print 2019-02-21；F&OS 2017 为 Management Science 63(3):791-817，INFORMS，2017 年 3 月。两篇均给出 DOI，不存在"查不到"的 DOI 条目。
原文引文：重新下载 F&OS 作者公开 PDF（772,720 字节）并抽取正文，逐字命中式 (1)(2)(3)、三类引用的文字定义、n_t 涵盖"the focal patent and/or its technological predecessors"、"first five years after the focal patent's issue … (Jaffe and Trajtenberg 2002)"、82,572/2.9 million（2.8%）、CD5 均值 0.07/标准差 0.23/范围 [−1, 1]，以及"larger teams produce more destabilizing inventions"（Table 4/5 中 Inventors 系数为正且显著）。WWE 页面重新抓取后，摘要的"smaller teams … disrupt / larger teams … develop"、"65 million"、Extended Data Fig. 5g 的 i/k/j 三类定义、Extended Data Fig. 3 的"5 years to 40 years / 166,310 / 24,174,022"均逐字命中；页面含登录与购买入口，确认正文公式逐字原文仍属"查不到"，第 5 节第 1、2 条成立。
数字更正：第 3.5 节与第 6 节中"把 B 换成 B+1 后 CD5 偏移"的统计，上一版写作均值约 −1.49×10⁻⁴、202 篇为正 / 70 篇为负。本轮用 fractions.Fraction 对 320 行精确重算，实测为：Δ 均值 +1.49×10⁻⁴、中位数 −1.59×10⁻⁸、范围 [−2.02×10⁻³, +4.76×10⁻²]、Δ>0 的 70 篇 / Δ<0 的 202 篇 / Δ=0 的 48 篇、符号翻转 0 篇。数值量级与"零翻转"结论正确，只是正负方向写反（把"文献式 − 脚本式"误标成"脚本式 − 文献式"），现已按实测改正。该更正不改变"− 1 无理论依据、偏移小、不影响 H1 符号判定"的结论，但请下游引用时以本节数值为准。
等价性推导复核：sympy 重新验证 simplify((A−2J)/(A+B−J) − (n_i−n_j)/(n_i+n_j+n_k)) = 0、分母展开为 n_i+n_j+n_k；20 万组 [0,500]³ 随机整数用有理数精确比较不等次数 0；k 效应表四行（1/238、3/2756、−1/2678、1/444）逐项复算一致。
完整性：shared/lit_findings.json 可被 python -c "import json; json.load(...)" 正常解析；minus_one_analysis.batch1_effect 中的偏移方向已同步改为与本节实测一致。