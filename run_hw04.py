# -*- coding: utf-8 -*-
"""重启内核并运行 HW04 全部代码，把输出嵌入 notebook 后保存。"""
import os
import time

import nbformat
from nbclient import NotebookClient

HERE = os.path.dirname(os.path.abspath(__file__))
NB_PATH = os.path.join(HERE, "20244081132_唐林_hw04.ipynb")

nb = nbformat.read(NB_PATH, as_version=4)

# 模拟“重启内核后运行全部”：清空所有代码单元的执行计数与输出
for cell in nb.cells:
    if cell.cell_type == "code":
        cell.execution_count = None
        cell.outputs = []
        cell.metadata.pop("execution", None)

client = NotebookClient(
    nb,
    timeout=900,
    kernel_name="hw04",
    allow_errors=False,
    record_timing=True,
)

env = dict(os.environ)
env["CONDA_DEFAULT_ENV"] = "hw04"
env["CONDA_PREFIX"] = r"C:\Users\Administrator\Desktop\Anacona\envs\hw04"

start = time.time()
client.execute(env=env)
elapsed = time.time() - start

nbformat.write(nb, NB_PATH)
code_cells = [c for c in nb.cells if c.cell_type == "code"]
print(f"OK: executed {len(code_cells)} code cells in {elapsed:.1f}s -> {NB_PATH}")
