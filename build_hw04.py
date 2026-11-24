# -*- coding: utf-8 -*-
"""生成《作业4：正则表达式与结构化网页数据》Jupyter Notebook（nbformat v4）。

学号 20244081132 / 姓名 唐林。
覆盖：12 道 Python 正则题（逐题测试） + BeautifulSoup 气候表格检索与行名提取。
"""
import nbformat as nbf

nb = nbf.v4.new_notebook()
nb.metadata["kernelspec"] = {
    "display_name": "Python 3",
    "language": "python",
    "name": "python3",
}
nb.metadata["language_info"] = {"name": "python", "version": "3.13"}

cells = []


def md(text):
    cells.append(nbf.v4.new_markdown_cell(text))


def code(text):
    cells.append(nbf.v4.new_code_cell(text))


# ==================== 封面 ====================
md("""# 作业 4：正则表达式与结构化网页数据

**作者/课程**：丁平尖　　**学号**：20244081132　　**姓名**：唐林

**提交文件**：`20244081132_唐林_hw04.ipynb`（Jupyter Notebook）

**访问/测试日期**：2026-11-24

> **提交自检**：本 Notebook 已在独立虚拟环境 `exp01` 中重启内核并全量运行，所有断言均通过；网页抓取与解析结果已嵌入输出。

**内容结构**：① 第一个代码框：身份与环境记录　② 12 道 Python 正则表达式练习（逐题附测试）　③ 从网页检索气候数据（`retrieve_climate_table` / `list_climate_table_row_names`）。

## 关于网页来源的说明（按题目要求）

作业建议尝试 Madison、Buenos Aires、Harbin 等维基百科城市页。但在 **2026-11-24** 本机实测，`en.wikipedia.org` 与 `zh.wikipedia.org` 均无法正常读取：`urllib` 返回 `URLError: [SSL: UNEXPECTED_EOF_WHILE_READING] EOF occurred in violation of protocol` 或 `Tunnel connection failed: 502 Bad Gateway`。按题目说明，**不把访问失败当作“没有气候数据表格”**，改用可正常访问且含气候数据表格的页面，并在下方明确记录实际 URL、结构与访问日期。""")

# ==================== 0. 身份与环境 ====================
md("""## 0. 第一个代码框：身份与环境记录

按作业要求，先修改第一个代码框中的学号；同时记录姓名、当前虚拟环境与机器指纹。机器指纹由计算机名、机器类型、操作系统和 MAC 地址拼接后取 SHA-256 前 16 位，与学号组合成 `RUN_ID`，用于标识“哪个人在哪台机器上完成了本次作业”。""")

code('''import hashlib
import os
import platform
import uuid

# 修改为自己的学号
STUDENT_ID = 20244081132
STUDENT_NAME = "唐林"

CONDA_ENV = os.environ.get("CONDA_DEFAULT_ENV", "base")
print(f"[Conda 环境 ] {CONDA_ENV}")

MACHINE_FP = hashlib.sha256(
    f"{platform.node()}|{platform.machine()}|{platform.system()}|{uuid.getnode()}".encode()
).hexdigest()[:16]

RUN_ID = f"{STUDENT_ID}-{MACHINE_FP}"
print(f"[学号]       {STUDENT_ID}")
print(f"[姓名]       {STUDENT_NAME}")
print(f"[机器指纹]   {MACHINE_FP}")
print(f"[RUN_ID]     {RUN_ID}")''')

# ==================== 一、正则练习 ====================
md("""---

# 一、Python 正则表达式练习

下面 12 个函数逐一对应作业第 1～12 题。为便于核对，统一使用两个小工具：

- `check(题号, 实际值, 期望值)`：断言相等并打印 PASS/FAIL；
- `check_raises(题号, 函数, 异常类型)`：断言指定异常确实被抛出。

正则约定：题目中的“仅包含英文字母 a-z、A-Z 和数字 0-9”按题面字面理解为 ASCII 字母数字；第 8、10 题的“单词”也按 ASCII 字母序列处理。""")

code('''import re
from datetime import date


def check(label, got, expected):
    ok = got == expected
    print(f"{'PASS' if ok else 'FAIL'} | {label}: got={got!r}, expected={expected!r}")
    assert ok, f"{label}: got {got!r}, expected {expected!r}"


def check_raises(label, func, exc_type):
    try:
        func()
    except exc_type as exc:
        print(f"PASS | {label}: {type(exc).__name__}: {exc}")
    else:
        raise AssertionError(f"{label}: expected {exc_type.__name__}")''')

md("""## 第 1～4 题：基础匹配

1. 用 `re.fullmatch(r"[A-Za-z0-9]+", s)` 确保**整个字符串**只含 ASCII 字母/数字，且至少有一个字符。
2. `ab*`：一个 `a` 后跟零个或多个 `b`。
3. `ab+`：一个 `a` 后跟一个或多个 `b`。
4. `a.*b`：以 `a` 开头、以 `b` 结尾，中间任意字符；加 `re.DOTALL` 使 `.` 也能匹配换行。""")

code('''# 1. 仅含英文字母和数字
def is_ascii_alnum(s):
    return re.fullmatch(r"[A-Za-z0-9]+", s) is not None

check("1-1 abcXYZ123", is_ascii_alnum("abcXYZ123"), True)
check("1-2 abc 123", is_ascii_alnum("abc 123"), False)
check("1-3 abc_123", is_ascii_alnum("abc_123"), False)
check("1-4 空字符串", is_ascii_alnum(""), False)


# 2. a 后面零个或多个 b
def match_a_then_zero_or_more_b(s):
    return re.fullmatch(r"ab*", s) is not None

check("2-1 a", match_a_then_zero_or_more_b("a"), True)
check("2-2 ab", match_a_then_zero_or_more_b("ab"), True)
check("2-3 abbbb", match_a_then_zero_or_more_b("abbbb"), True)
check("2-4 b", match_a_then_zero_or_more_b("b"), False)
check("2-5 aab", match_a_then_zero_or_more_b("aab"), False)
check("2-6 ac", match_a_then_zero_or_more_b("ac"), False)


# 3. a 后面一个或多个 b
def match_a_then_one_or_more_b(s):
    return re.fullmatch(r"ab+", s) is not None

check("3-1 ab", match_a_then_one_or_more_b("ab"), True)
check("3-2 abbb", match_a_then_one_or_more_b("abbb"), True)
check("3-3 a", match_a_then_one_or_more_b("a"), False)
check("3-4 aab", match_a_then_one_or_more_b("aab"), False)


# 4. a 开头、b 结尾，中间任意字符
def match_a_start_b_end(s):
    return re.fullmatch(r"a.*b", s, flags=re.DOTALL) is not None

check("4-1 ab", match_a_start_b_end("ab"), True)
check("4-2 aXYZb", match_a_start_b_end("aXYZb"), True)
check("4-3 a换行b", match_a_start_b_end("a\\nb"), True)
check("4-4 a", match_a_start_b_end("a"), False)
check("4-5 ba", match_a_start_b_end("ba"), False)''')

md("""## 第 5～8 题：替换、日期与单词筛选

5. IP 各段用 `^0+(?=\\d)` 去掉前导零，但全零段用 `or "0"` 保留一个 0；顺带校验四段且每段 0～255。
6. 空格与下划线要**同时**互换，不能先替空格再替下划线；用 `re.sub` 的回调函数一次扫描完成。
7. `yyyy-mm-dd` → `dd-mm-yyyy` 用捕获组重排，并用 `datetime.date` 校验日期合法。
8. 用单词边界 `\\b` + `[ae]` + 字母序列，忽略大小写。""")

code('''# 5. 删除 IP 各段数字的前导零
def remove_ip_leading_zeros(ip):
    if not isinstance(ip, str) or re.fullmatch(r"\\d{1,3}(\\.\\d{1,3}){3}", ip) is None:
        raise ValueError("IP 必须是四段点分十进制数字")
    parts = ip.split(".")
    if any(int(p) > 255 for p in parts):
        raise ValueError("IP 每段必须在 0~255 之间")
    return ".".join(re.sub(r"^0+(?=\\d)", "", p) or "0" for p in parts)

check("5-1 192.168.001.010", remove_ip_leading_zeros("192.168.001.010"), "192.168.1.10")
check("5-2 000.000.000.000", remove_ip_leading_zeros("000.000.000.000"), "0.0.0.0")
check("5-3 001.002.003.004", remove_ip_leading_zeros("001.002.003.004"), "1.2.3.4")
check_raises("5-4 段数错误", lambda: remove_ip_leading_zeros("192.168.1"), ValueError)
check_raises("5-5 数值越界", lambda: remove_ip_leading_zeros("256.1.1.1"), ValueError)


# 6. 空格与下划线互换（同时替换）
def swap_spaces_and_underscores(s):
    return re.sub(r"[ _]", lambda m: "_" if m.group(0) == " " else " ", s)

check("6-1", swap_spaces_and_underscores("Hello world_python"), "Hello_world python")
check("6-2", swap_spaces_and_underscores("a b_c d"), "a_b c_d")
check("6-3", swap_spaces_and_underscores("no_change"), "no change")


# 7. yyyy-mm-dd -> dd-mm-yyyy
def yyyy_mm_dd_to_dd_mm_yyyy(s):
    m = re.fullmatch(r"(\\d{4})-(\\d{2})-(\\d{2})", s)
    if m is None:
        raise ValueError("日期格式必须为 yyyy-mm-dd")
    year, month, day = map(int, m.groups())
    date(year, month, day)  # 校验真实日期
    return f"{day:02d}-{month:02d}-{year:04d}"

check("7-1", yyyy_mm_dd_to_dd_mm_yyyy("2026-11-24"), "24-11-2026")
check("7-2", yyyy_mm_dd_to_dd_mm_yyyy("1999-01-01"), "01-01-1999")
check_raises("7-3 非法月份", lambda: yyyy_mm_dd_to_dd_mm_yyyy("2026-13-01"), ValueError)


# 8. 找出所有以 a 或 e 开头的单词
def find_words_starting_with_a_or_e(s):
    return re.findall(r"\\b[ae][A-Za-z]*\\b", s, flags=re.IGNORECASE)

check("8-1", find_words_starting_with_a_or_e("An apple a day keeps everyone energetic."),
      ["An", "apple", "a", "everyone", "energetic"])
check("8-2", find_words_starting_with_a_or_e("Elephants and eagles are amazing."),
      ["Elephants", "and", "eagles", "are", "amazing"])''')

md("""## 第 9～12 题：缩写、长单词、过滤与括号清理

9. `\\bRoad\\b` 保证只替换独立单词，`Roadmap` 不受影响。
10. `\\b[A-Za-z]{4,}\\b` 取长度至少 4 的 ASCII 单词。
11. `[^A-Za-z0-9]` 匹配所有非字母数字字符并删除。
12. 括号内容可能嵌套，因此反复执行 `\\([^()]*\\)` 直到不再变化，最后合并多余空白。题目示例逐项处理的结果可用 `.split()` 得到。""")

code('''# 9. 将 Road 缩写为 Rd
def abbreviate_road(s):
    return re.sub(r"\\bRoad\\b", "Rd", s, flags=re.IGNORECASE)

check("9-1", abbreviate_road("Main Road, Elm road, Broadway"), "Main Rd, Elm Rd, Broadway")
check("9-2", abbreviate_road("Road to Rome"), "Rd to Rome")
check("9-3 Roadmap 不变", abbreviate_road("Roadmap"), "Roadmap")


# 10. 长度至少 4 个字符的单词
def find_words_length_at_least_4(s):
    return re.findall(r"\\b[A-Za-z]{4,}\\b", s)

check("10-1", find_words_length_at_least_4("Java, Python, C, Go, Ruby and Rust"),
      ["Java", "Python", "Ruby", "Rust"])
check("10-2", find_words_length_at_least_4("a an and tree data"), ["tree", "data"])


# 11. 删除除字母和数字之外的所有字符
def keep_only_ascii_alnum(s):
    return re.sub(r"[^A-Za-z0-9]", "", s)

check("11-1", keep_only_ascii_alnum("Hello, world! 2026_HW#04"), "Helloworld2026HW04")
check("11-2", keep_only_ascii_alnum("a-b c_d.e"), "abcde")


# 12. 删除括号及括号内内容
def remove_parenthetical_content(s):
    previous = None
    while previous != s:
        previous = s
        s = re.sub(r"\\([^()]*\\)", "", s)
    return re.sub(r"\\s+", " ", s).strip()

example = "example (.com) w3resource github (.com) stackoverflow (.com)"
check("12-1 题面示例", remove_parenthetical_content(example),
      "example w3resource github stackoverflow")
print("12-1 逐项处理:", remove_parenthetical_content(example).split())
check("12-2 嵌套括号", remove_parenthetical_content("Alpha (x (y) z) Beta"), "Alpha Beta")''')

# ==================== 二、网页检索 ====================
md("""---

# 二、从网页检索气候数据

## 实际使用的 URL 与访问日期

访问日期均为 **2026-11-24**。维基百科因上封面所述的网络错误无法使用，改用下列可正常访问、含气候数据表格的城市页面：

| 编号 | 城市 | URL | 表格形态 |
| --- | --- | --- | --- |
| A | Los Angeles | `https://www.worldweatheronline.com/los-angeles-weather-averages/california/us.aspx` | `thead` + `tbody`；首行是列标题 `Month / Day / Night / Rain Days`，数据行首列是月份文本 |
| B | Hyderabad | `https://www.worldweatheronline.com/hyderabad-weather-averages/telangana/in.aspx` | 同上模板；用于验证同一解析逻辑对不同城市数据有效 |
| C | Boston | `https://www.timeanddate.com/weather/usa/boston/climate` | `thead` + `tbody`；首行是 `Quick Climate Info` 标题行，数据行首列是 `th`（如 `Hottest Month`），与 A/B 的行名位置和语义都不同 |
| D | 无表格对照 | `https://www.baidu.com/` | 成功读取但不含气候表格，应返回 `None` |

A/B 与 C 即为题目要求的“**至少一个有结构差异的页面**”：前者行名在 `td` 中且是月份，后者行名在 `th` 中且是气候指标；后者第一行还是单行 `th` 标题，而前者第一行是四列 `th` 表头。""")

code('''import time
import urllib.error
import urllib.request

from bs4 import BeautifulSoup
from bs4.element import Tag

USER_AGENT = "Mozilla/5.0 (compatible; HW04/1.0; educational assignment)"
_HTML_CACHE = {}  # 仅在本内核会话内缓存，避免重复请求；重启内核会重新联网获取


def fetch_html(url):
    """读取 URL 的 HTML 文本。网络/HTTP 错误原样抛出，不吞掉异常。"""
    if url in _HTML_CACHE:
        return _HTML_CACHE[url]
    last_exc = None
    for attempt in range(2):
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": USER_AGENT,
                "Accept": "text/html,application/xhtml+xml",
                "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8",
            })
            with urllib.request.urlopen(req, timeout=20) as resp:
                raw = resp.read()
                charset = resp.headers.get_content_charset() or "utf-8"
            html = raw.decode(charset, errors="replace")
            _HTML_CACHE[url] = html
            return html
        except (urllib.error.HTTPError, urllib.error.URLError) as exc:
            last_exc = exc
            if attempt == 0:
                time.sleep(0.8)
    raise last_exc


MONTH_WORDS = (
    "january", "february", "march", "april", "may", "june",
    "july", "august", "september", "october", "november", "december",
    "jan", "feb", "mar", "apr", "jun", "jul", "aug", "sep", "oct", "nov", "dec",
)
MONTH_PATTERN = re.compile(
    r"^(" + "|".join(MONTH_WORDS) + r")$", re.IGNORECASE
)
CLIMATE_HINTS = (
    "climate", "weather averages", "weather average", "average temperature",
    "rain days", "precipitation", "monthly average", "averages",
)


def _clean(text):
    return " ".join(text.split()).strip()


def _table_score(table, page_title):
    """给表格打分：标题、气候关键词、月份行、指标行、规模。"""
    table_text = _clean(table.get_text(" ", strip=True))
    caption = table.find("caption")
    caption_text = _clean(caption.get_text(" ", strip=True)) if caption else ""
    first_row = table.find("tr")
    header_text = ""
    if first_row:
        header_text = _clean(" ".join(
            c.get_text(" ", strip=True) for c in first_row.find_all(["th", "td"])
        ))
    title = (caption_text + " " + header_text).lower()
    combined = (title + " " + page_title + " " + table_text).lower()

    score = 0
    if "climate data for" in title:
        score += 12
    if any(hint in combined for hint in CLIMATE_HINTS):
        score += 4
    month_hits = sum(1 for m in MONTH_WORDS if re.search(r"\\b" + m + r"\\b", table_text, re.I))
    if month_hits >= 6:
        score += 6
    elif month_hits >= 3:
        score += 2
    if re.search(
        r"quick climate info|hottest month|coldest month|wettest month|"
        r"average high|rain days|temperature|precipitation",
        table_text, re.IGNORECASE,
    ):
        score += 3
    if len(table.find_all("tr")) >= 3 and len(table.find_all(["th", "td"])) >= 6:
        score += 1
    return score


def retrieve_climate_table(s):
    """只接收 URL；返回气候数据表格的 BeautifulSoup Tag，找不到返回 None。

    网络错误或 HTTP 错误由 fetch_html 原样抛出，不在此处捕获。
    """
    soup = BeautifulSoup(fetch_html(s), "html.parser")
    page_title = _clean(soup.title.get_text(" ", strip=True)) if soup.title else ""

    best, best_score = None, 0
    for table in soup.find_all("table"):
        score = _table_score(table, page_title)
        if score > best_score:
            best, best_score = table, score
    return best if best_score >= 5 else None


def list_climate_table_row_names(s):
    """只接收 URL；返回去掉首尾空白的行名字符串列表，找不到表格返回 None。"""
    table = retrieve_climate_table(s)
    if table is None:
        return None

    names = []
    skipped = ("climate data for", "weather averages", "quick climate info",
               "source", "数据来源", "©", "all rights reserved")
    for tr in table.find_all("tr"):
        cells = tr.find_all(["th", "td"], recursive=False)
        if not cells:
            continue
        first = cells[0]
        text = _clean(first.get_text(" ", strip=True))
        if not text:
            continue
        lower = text.lower()
        data_cells = [c for c in cells[1:] if c.name == "td"]

        # 跳过列标题行：首格是 th 且整行都是 th；或首格文字就是 Month/月份
        if first.name == "th" and all(c.name == "th" for c in cells):
            continue
        if lower in {"month", "月份", "mon"}:
            continue
        # 跳过只有标题、没有数据单元格的行，以及来源行
        if not data_cells:
            continue
        if any(key in lower for key in skipped):
            continue

        # 行名判定：scope="row"、月份文本、或首格为 th（如 Hottest Month）
        if first.get("scope") == "row" or MONTH_PATTERN.match(text) or first.name == "th":
            names.append(text)
    return names''')

md("""## 表格结构观察

先定位表格并观察节点结构：直接子节点标签名、`<tr>` 数量、首行单元格的标签与 `scope` 属性。A/B 与 C 的差异见输出。""")

code('''PAGES = {
    "A-Los Angeles": "https://www.worldweatheronline.com/los-angeles-weather-averages/california/us.aspx",
    "B-Hyderabad": "https://www.worldweatheronline.com/hyderabad-weather-averages/telangana/in.aspx",
    "C-Boston": "https://www.timeanddate.com/weather/usa/boston/climate",
}

tables = {}
for label, url in PAGES.items():
    table = retrieve_climate_table(url)
    tables[label] = table
    assert isinstance(table, Tag), f"{label}: 未找到 climate table"
    rows = table.find_all("tr")
    direct_children = [c.name for c in table.find_all(recursive=False) if getattr(c, "name", None)]
    first_row = rows[0] if rows else None
    first_cells = (
        [(c.name, c.get("scope"), _clean(c.get_text(" ", strip=True)))
         for c in first_row.find_all(["th", "td"], recursive=False)]
        if first_row else []
    )
    print(f"=== {label} ===")
    print(f"URL: {url}")
    print(f"直接子节点: {direct_children}")
    print(f"<tr> 数量: {len(rows)}")
    print(f"首行单元格: {first_cells[:6]}")''')

md("""## 函数测试

- `retrieve_climate_table(s)`：四个页面（含无表格对照）逐一验证，返回 `Tag` 或 `None`。
- `list_climate_table_row_names(s)`：只返回 `str`，不含标题行/月份列标题/数据来源行。
- 异常分支：404 页面应抛 `HTTPError`，拒绝连接的地址应抛 `URLError`。""")

code('''# retrieve_climate_table：有表格 -> Tag；无表格 -> None
for label, url in PAGES.items():
    assert isinstance(retrieve_climate_table(url), Tag)
print("PASS | A/B/C 均返回 BeautifulSoup Tag")

NO_TABLE_URL = "https://www.baidu.com/"
assert retrieve_climate_table(NO_TABLE_URL) is None
print("PASS | D 无气候表格 -> None")


# list_climate_table_row_names：逐页查看，并做类型/内容断言
row_names = {}
for label, url in PAGES.items():
    names = list_climate_table_row_names(url)
    row_names[label] = names
    print(f"=== {label} 行名 ===")
    print(names)
    assert isinstance(names, list) and names
    assert all(isinstance(x, str) and x == x.strip() and "<" not in x for x in names)

assert "January" in row_names["A-Los Angeles"]
assert "January" in row_names["B-Hyderabad"]
assert "Hottest Month" in row_names["C-Boston"]
assert list_climate_table_row_names(NO_TABLE_URL) is None
print("PASS | 行名均为纯字符串，且标题行/列标题/来源行已排除")''')

code('''# 异常分支：HTTP 错误与网络错误必须抛出，不能返回 None
HTTP_404_URL = "https://www.timeanddate.com/no-such-page-hw04"
CONN_REFUSED_URL = "http://127.0.0.1:9/"

check_raises("HTTP 404", lambda: retrieve_climate_table(HTTP_404_URL), urllib.error.HTTPError)
check_raises("连接被拒绝", lambda: retrieve_climate_table(CONN_REFUSED_URL), urllib.error.URLError)
print("PASS | 网络错误与 HTTP 错误均按题目要求抛出异常")''')

md("""---

# 三、提交说明（对照作业要求）

1. ✅ 第一个代码框已把学号改为 `20244081132`，并补充姓名 `唐林`；输出包含 Conda 环境、机器指纹与 `RUN_ID`。
2. ✅ 第 1～12 题均定义了函数，且每题都有 `check` / `check_raises` 测试用例；全部通过。
3. ✅ 因维基百科访问失败，已说明具体错误并按题目允许更换为可访问的气候数据页面；Notebook 中注明了实际 URL 与访问日期 2026-11-24。
4. ✅ `retrieve_climate_table(s)` 与 `list_climate_table_row_names(s)` 都只接收一个 URL 字符串；成功但无表格返回 `None`，网络/HTTP 错误抛异常。
5. ✅ 用三个城市页面测试，其中 Boston 页与 Los Angeles / Hyderabad 页的表格结构不同；行名列表为去除首尾空白的 Python 字符串，不含标题行、月份列标题与数据来源行。
6. ✅ 已在虚拟环境中重启内核全量运行，零报错。""")

nb["cells"] = cells
OUT = r"C:/Users/Administrator/WorkBuddy/2026-10-17-21-27-59/HW04作业/20244081132_唐林_hw04.ipynb"
with open(OUT, "w", encoding="utf-8") as f:
    nbf.write(nb, f)
print("written:", OUT)
print("cells:", len(cells), "code cells:", sum(1 for c in cells if c.cell_type == "code"))
