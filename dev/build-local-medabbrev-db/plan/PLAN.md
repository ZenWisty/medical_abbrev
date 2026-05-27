# build-local-medabbrev-db Skill Plan

## 目标
构建一个用于构建本地医疗缩写数据库的 skill，包含数据采集、清洗、存储到 @./doc 的完整流程。

---

## Step 1: 数据源评估与爬取

### 数据源列表
| # | 来源 | URL | 备注 |
|---|------|-----|------|
| 1 | Medical Transcription Samples | https://www.mtsamples.com/ | 需评估爬取范围 |
| 2 | BigBio MedQA | https://huggingface.co/datasets/bigbio/med_qa | 需评估是否全量爬取 |
| 3 | Wikipedia 医疗缩写表格 | https://en.wikipedia.org/wiki/List_of_medical_abbreviations | 仅爬取 abbreviation 表格 |
| 4 | Clinical Abbreviations (lisavirginia) | https://github.com/lisavirginia/clinical-abbreviations | 需评估 |
| 5 | MCP-MedLookup (hypersniper05) | https://github.com/hypersniper05/MCP-MedLookup | 需评估 |

### 任务
- [ ] 逐个访问各数据源，评估数据规模和质量
- [ ] 确定每个数据源的爬取策略（全量/采样/仅元数据）
- [ ] 编写或复用爬虫代码获取数据
- [ ] 将原始数据存入 `@examples/tmp/raw/<source_name>/`

---

## Step 2: 数据清洗与标准化

### 任务
- [ ] 定义统一的医疗缩写数据结构
- [ ] 对各来源数据进行清洗（去重、格式统一）
- [ ] 处理冲突：同一缩写不同来源的不同解释
- [ ] 输出标准化数据到 `@examples/tmp/cleaned/`

---

## Step 3: 构建复杂 CONTEXT.md 结构

按照 `.claude/skills/grill-with-docs/SKILL.md` 描述的格式逐步构建：
- [ ] 创建 `@./doc/CONTEXT.md` 主文档
- [ ] 拆分 sub-context（如有需要）
- [ ] 更新术语表（Language）
- [ ] 定义 Relationships
- [ ] 记录 Flagged ambiguities
- [ ] 编写 Example dialogue

---

## Step 4: 创建 Skill

### 任务
- [ ] 参照 PLAN.md 完整流程创建 SKILL.md
- [ ] 定义 skill 的触发条件和执行逻辑
- [ ] 整合进项目 SKILL.md 总目录

---

## 当前进度

- [x] 创建 PLAN.md
- [ ] Step 1: 数据源评估与爬取
- [ ] Step 2: 数据清洗与标准化
- [ ] Step 3: 构建 CONTEXT.md
- [ ] Step 4: 创建 Skill

---

## 待确认事项
- [ ] 各数据源的 License 是否允许爬取？
- [ ] 数据量的预估（多少条缩写记录？）
- [ ] 是否需要实时增量更新？