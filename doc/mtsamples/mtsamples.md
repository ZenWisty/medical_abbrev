`mtsamples.com` 是临床医学界非常著名的“宝库”，它包含了超过 5000 份真实的医学转录样本。但该网站的 HTML 结构比较老旧，嵌套深，且 URL 逻辑稍显混乱。

建议采用 **“三级策略”**。

---

### 第一步：网站结构解构

1.  **一级页面（分类页）**：左侧边栏（Index by Type）是所有科室的入口。
    *   例如：`https://www.mtsamples.com/site/pages/browse.asp?type=10-Cardiovascular%20/%20Pulmonary`
2.  **二级页面（列表页）**：点击某个科室后，会看到该科室下的所有样本列表。
3.  **三级页面（内容页）**：最终的转录文本页面。
    *   **关键标签**：所有的转录内容都在 `id="sampletext"` 的 `div` 标签内。

---

### 第二步：爬取逻辑实现 (Python)

由于该网站是静态渲染为主，使用 `requests` + `BeautifulSoup` 是最高效的。如果需要大规模爬取，建议使用 `Scrapy`。

以下是一个核心逻辑脚本，展示如何精准定位医学术语和转录内容：

```python
import requests
from bs4 import BeautifulSoup
import json
import time

class MTSamplesScraper:
    def __init__(self):
        self.base_url = "https://www.mtsamples.com"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def get_categories(self):
        """第一步：获取所有科室分类链接"""
        response = requests.get(self.base_url, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        # 寻找侧边栏链接
        categories = []
        for link in soup.select('div.sideBar a'):
            href = link.get('href')
            if 'type=' in href:
                categories.append({
                    "name": link.text.strip(),
                    "url": self.base_url + href
                })
        return categories

    def get_sample_links(self, category_url):
        """第二步：在分类页获取所有具体的样本链接"""
        response = requests.get(category_url, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = []
        # 寻找表格中的样本链接
        for link in soup.select('table td a'):
            href = link.get('href')
            if 'sample.asp?sample=' in href:
                links.append(self.base_url + href)
        return list(set(links)) # 去重

    def parse_sample(self, sample_url):
        """第三步：抓取并清洗临床文本"""
        response = requests.get(sample_url, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        content = {}
        # 寻找核心文本区域
        sample_text_div = soup.find('div', {'id': 'sampletext'})
        if not sample_text_div:
            return None

        # 提取标题和描述
        content['title'] = soup.find('h1').text.strip() if soup.find('h1') else ""
        
        # 提取关键词（这是提取术语最快的地方！）
        keywords_div = soup.find('div', string=lambda t: t and 'Keywords' in t)
        content['keywords'] = keywords_div.find_next_sibling(text=True).strip() if keywords_div else ""

        # 提取全文并按段落切分（方便 AI 学习对话上下文）
        paragraphs = [p.text.strip() for p in sample_text_div.find_all(['p', 'b'])]
        content['body'] = "\n".join(paragraphs)

        return content

# 使用示例
scraper = MTSamplesScraper()
# 我们可以只抓取 'Cardiovascular / Pulmonary' 作为一个测试
test_url = "https://www.mtsamples.com/site/pages/browse.asp?type=10-Cardiovascular%20/%20Pulmonary"
links = scraper.get_sample_links(test_url)
for link in links[:3]: # 先测试3个
    data = scraper.parse_sample(link)
    print(f"Extracted: {data['title']}")
```

---

### 第三步：针对 AI 训练的数据清洗逻辑

爬取下来后，你不能直接喂给 AI，需要进行 **“语义对齐”** 处理。

1.  **提取 Key-Value 对**：
    MTSamples 的内容通常是 `TITLE: Content` 的格式。例如 `HISTORY OF PRESENT ILLNESS: ...`。你可以用正则把它们切分成 JSON 对象，让 AI 理解“病史”、“主诉”、“体检”的对应关系。
    ```python
    import re
    # 匹配类似 "PAST MEDICAL HISTORY:" 这样的标题
    sections = re.split(r'\n([A-Z\s]{5,}):', full_text)
    ```

2.  **术语挖掘 (Terminology Mining)**：
    该网站底部有 `Keywords` 字段，这些是现成的医学术语标签。
    *   **策略**：将 Keywords 里的词汇建立一个 `clinical_terms.txt`，作为你的 AI 挂载词典。

3.  **对话模拟提取**：
    寻找包含 `CHIEF COMPLAINT` (主诉) 和 `HISTORY` (病史) 的部分，这些部分最接近真实医患交流的英文表达。

---

### 第四步：给你的建议（避坑指南）

1.  **频率限制**：MTSamples 没有任何复杂的反爬，但为了礼貌，请在循环中加入 `time.sleep(1)`，否则可能会被暂时封禁 IP。
2.  **直接利用现有成果**：
    *   实际上，由于这个网站太出名，Kaggle 上已经有人把它爬好并做成了 **CSV 数据集**。
    *   你可以直接在 Kaggle 搜索 **"Medical Transcriptions"**。下载那个 7MB 左右的 CSV 文件，里面已经清洗好了 `description`, `medical_specialty`, `sample_name`, `transcription`, `keywords` 五列。
    *   **这比你自己写爬虫快得多。**

### 如何将爬到的数据喂给 Claude CLI？
下载或爬取 CSV 后，将其转化为 **Markdown 格式**（每 50 份样本一个文件），放在你的 Claude CLI 能够读取的目录下。
在对话时告诉它：
> "I have uploaded 5000 clinical samples in `./med_data/`. When I discuss clinical cases, search these files to understand the typical phrasing and terminology used by US clinicians."
