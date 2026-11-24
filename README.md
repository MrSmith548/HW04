# 作业4：正则表达式与结构化网页数据

唐林 / 20244081132

## 内容

- `20244081132_唐林_hw04.ipynb`：正式 Notebook，已全量运行并嵌入输出。
- `build_hw04.py`：生成 Notebook 的脚本。
- `run_hw04.py`：重启内核、全量执行 Notebook 的脚本。
- `environment.yml` / `requirements.txt`：conda 环境与依赖清单。

## 环境

使用 conda 环境 `hw04`（Python 3.13）：

```bash
conda env create -f environment.yml
conda activate hw04
python -m ipykernel install --user --name hw04 --display-name "Python (hw04)"
python run_hw04.py
```

## 完成情况

1. 12 道正则表达式题逐题实现并附断言测试，全部通过。
2. `retrieve_climate_table(s)` 与 `list_climate_table_row_names(s)`：
   - 成功但无表格返回 `None`；
   - HTTP 错误抛 `HTTPError`，网络错误抛 `URLError`；
   - 行名为去空白后的纯字符串，已排除标题行、列标题与来源行。
3. 网页来源（访问日期 2026-11-24）：
   - Los Angeles / Hyderabad：worldweatheronline
   - Boston：timeanddate（表格结构与前两页不同）
   - 维基百科因 `SSL UNEXPECTED_EOF` / `Tunnel 502` 无法访问，已按题目要求更换页面。
4. Notebook 已在 conda `hw04` 环境全新内核执行，9 个代码单元零报错。
