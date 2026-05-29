# issues-local-medabbrev-db-provider.md

## 问题记录

### 1. mtsamples.com 无法访问

**现象：**
- 访问主页面 `https://www.mtsamples.com` 返回 HTTP 500
- 访问分类页 `https://www.mtsamples.com/site/pages/browse.asp?type=10-Cardiovascular%20/%20Pulmonary` 返回 HTTP 403
- 访问样本页 `https://www.mtsamples.com/site/pages/sample.asp?sample=1` 返回 HTTP 500

**影响：**
- 无法抓取真实医学样本数据
- AFK slice #4 (HTTP Client) 和 #5 (Parser) 无法进行端到端测试
- 无法完成 Issue #7 QA 中的 #5 Parser 真实 HTML 验证

**建议：**
- 等待 mtsamples.com 服务恢复后重试
- 或参考 doc/mtsamples/mtsamples.md 中的建议，使用 Kaggle 上的 "Medical Transcriptions" CSV 数据集
- 或准备 HTML fixtures 进行 Parser 单元测试

### 2. 尝试用 stub provider 数据的限制

**现象：**
- `MedAbbrevProvider` 是硬编码的 stub 数据，只有 2 条样本
- 无法通过它获取 20 条真实数据

**建议：**
- 需要真实数据源（Kaggle CSV 或其他）才能获取实际样本

### 3. fetch_mtsamples.py 脚本

**位置：**
- `examples/tmp/fetch_mtsamples.py`

**用途：**
- 尝试从 mtsamples.com 抓取数据的脚本
- 当前因网站返回 403/500 无法使用
- 保留脚本以便网站恢复后可立即使用

### 4. 当前可用的替代方案

参考 `doc/mtsamples/mtsamples.md` 第四节的建议：
- Kaggle 上有 "Medical Transcriptions" CSV 数据集（~7MB）
- 包含 `description`, `medical_specialty`, `sample_name`, `transcription`, `keywords` 五列
- 可以下载后转换为 JSON 格式使用