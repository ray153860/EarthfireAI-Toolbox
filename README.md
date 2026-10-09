# EarthfireAI Knowledge Base

可独立运行的本地文档导入、分块、SQLite FTS5 索引、检索和来源定位组件。默认不调用云端服务，不包含私人知识库，也不要求安装完整 EarthfireAI。

## 已实现

- TXT、Markdown 直接导入。
- PDF、DOCX 通过可选依赖导入文字层。
- SHA-256 去重、可配置分块和重叠长度。
- SQLite FTS5 全文检索。
- 返回文件名、来源路径、分块序号和片段。
- 命令行创建、导入、列出和检索。

## 未实现或未承诺

- 扫描 PDF 自动 OCR、图片和复杂图表理解。
- 向量检索、重排序、自动网页爬取和生成式问答。
- WeKnora 本身及其数据库。EarthfireAI 整合版继续使用 WeKnora；本项目提供的是独立、轻量的公开组件。

## 安装

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -e .
# 需要 PDF / DOCX 时：
.venv\Scripts\python -m pip install -e ".[documents]"
```

## 使用

```powershell
earthfire-knowledge init --db .\data\knowledge.sqlite3
earthfire-knowledge import .\examples\public_sample.txt --db .\data\knowledge.sqlite3
earthfire-knowledge search "达西定律" --db .\data\knowledge.sqlite3
earthfire-knowledge list --db .\data\knowledge.sqlite3
```

检索结果会显示 `[文档标题 / chunk N]`，便于回到原文核对。默认数据库位于当前目录 `data/knowledge.sqlite3`，已被 `.gitignore` 排除。

## 测试

```powershell
python -m unittest discover -s tests -v
```

测试使用公开的虚构 TXT 样本，不读取个人资料。

## 与 EarthfireAI 整合版的关系

整合版的正式知识库仍是 WeKnora，本仓库不复制真实数据，也不替代现有数据库。未来可以通过适配器把相同的导入、检索接口接入整合版。

## 安全与限制

- 导入的文档只是数据，不能成为系统命令。
- 本项目不判断资料版权；使用者必须只导入有权处理的资料。
- FTS5 是关键词检索，不能等同于语义向量检索。
- PDF 只读取已有文字层；扫描件需要外部 OCR。

## 许可证

原创代码采用 Apache-2.0，见 `LICENSE`。
