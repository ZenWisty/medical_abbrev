---
name: filter-out-medterm
description: |
  医学术语过滤技能 - 当用户提供字幕文件并要求提取医疗知识内容时必须使用此技能。
  适用场景：医学讲座字幕过滤、临床对话提取、医院场景字幕处理、患者对话分析。
  输入格式：00:start|end|text 格式的双语字幕文件。
  输出：只保留含有临床医学术语的行（疾病名称、药物名称、医疗操作、临床指标等）。
  排除内容：社工对话、心理支持、音乐歌词、寒暄闲聊等非临床内容。
---

This skill filters a bilingual subtitle file to keep only lines containing medical terms, preserving the original document format.

**Important**: Do not write any code to execute this skill. Instead, follow the steps below directly using Claude's built-in tools (Read, Write, Bash) to read input files, analyze content line by line, and write output files.

When spawning a sub-agent (Agent tool) to assist with this skill, set `model: "opus"` so the sub-agent uses a capable model.

## When to Use
When the user has a subtitle file (in `00:start|end|text` format) and wants to extract only medical knowledge related content, removing casual chat and non-medical dialogue.

## Input
1. `source_file` — the path to the subtitle file
2. `target_file` — the path where the filtered content should be saved (typically same directory with `_medfilt` suffix added)

## Output
A filtered subtitle file containing only lines with medical terms, in the original format:
```
00:xx:xx,xxx|00:xx:xx,xxx|medical content here
```

## Step-by-Step Process

1. **Read source file** — Use Read tool to load the source file
2. **Evaluate each line** — Check if the line contains clinical medical terms:
   - If the line contains clinical medical terms → keep it
   - If the line contains no clinical medical terms → skip it, continue to next line
3. **Write target file** — Write all kept lines to target_file, preserving original format
4. **Confirm completion** — Report filtering results (lines processed, lines kept)

## Medical Terms Reference

### Keep lines containing these types of terms:

**Diseases/Conditions:**
- 室颤/心室颤动 (ventricular fibrillation), 心脏骤停 (cardiac arrest), 心脏病 (heart disease)
- 高钾血症 (hyperkalemia), 低钾血症 (hypokalemia), 电解质紊乱 (electrolyte imbalance)
- 肾衰竭/肾功能衰竭 (renal failure), 横纹肌溶解 (rhabdomyolysis)
- 脑出血 (cerebral hemorrhage), 脑水肿 (cerebral edema), 脑疝 (cerebral hernia)
- 肺脓肿 (lung abscess), 肺炎 (pneumonia), 误吸 (aspiration)
- 肠梗阻 (intestinal obstruction), 胆结石 (gallstone)
- 脓毒症/败血症 (sepsis)
- 阿尔茨海默病 (Alzheimer's disease)
- 糖尿病酮症酸中毒 (diabetic ketoacidosis)
- 心力衰竭 (heart failure), 心脏填塞 (cardiac tamponade)
- 开放性骨折 (open fracture), 脱位 (dislocation)

**Medications:**
- 劳拉西泮 (lorazepam), 利眠宁 (clonazepam), 氯胺酮 (ketamine), 吗啡 (morphine)
- 胰岛素 (insulin), 葡萄糖 (glucose), 甘露醇 (mannitol)
- 头孢曲松 (ceftriaxone), 阿奇霉素 (azithromycin), 阿莫西林 (amoxicillin)
- 肾上腺素 (epinephrine), 去甲肾上腺素 (norepinephrine)
- 利多卡因 (lidocaine), 昂丹司琼 (ondansetron)
- 肝素 (heparin), 华法林 (warfarin)
- PCC, FFP (fresh frozen plasma)

**Medical Procedures:**
- CT扫描 (CT scan), X光 (X-ray), 胸片 (chest X-ray)
- 透析/血液透析 (dialysis)
- 除颤 (defibrillation), 电击 (electric shock), 心肺复苏 (CPR)
- 插管 (intubation), 气道管理 (airway management)
- 神经阻滞 (nerve block), 股神经阻滞 (femoral nerve block)
- 中心静脉置管 (central venous catheterization), 静脉输液 (IV fluid)
- 胸外按压 (chest compression), Lucas按压系统 (Lucas compression system)

**Clinical Indicators:**
- 血压 (blood pressure), 心率 (heart rate), 血氧饱和度 (SpO2)
- 瞳孔 (pupil size and reaction)
- GCS评分 (Glasgow Coma Scale)
- 血细胞比容 (hematocrit), 肌酐 (creatinine), 钾/钠 (potassium/sodium)
- 乳酸 (lactate), 血培养 (blood culture)

**Symptoms:**
- 濒死呼吸 (agonal breathing), 呼吸骤停 (respiratory arrest)
- 呕吐/呕血 (vomiting/hematemesis)
- 腹痛/胸痛 (abdominal pain/chest pain)
- 休克 (shock)

### Lines to Exclude (even if they contain some medical words):

**Social worker / psychological support conversations — MUST exclude:**
- Lines containing "社工" (social worker), "帮助他，保护他，拯救他"
- Social worker self-introductions: "我是社工", "她是社工"
- Emotional/psychological support talks about grief, depression, mental health
- Comforting questions: "你怎么样？" (how are you?), "你还好吗？" (are you okay?)
- Discussions about deceased family members, school problems, family issues

**Other exclusions:**
- Music lyrics, sound effects
- Greetings, small talk, casual chat
- Hospital administration complaints about nurse shortages, bed management (unless directly related to specific patient conditions)
- Patient satisfaction survey discussions

## Filtering Principle

**Key rule: Only keep lines that explicitly contain clinical medical terms.**

- If a line mentions a condition but has no specific medical terminology → exclude
- If a line is from a social worker or support staff → exclude (even if it mentions "heart" or "blood pressure")
- In the same episode: doctor's clinical dialogue → keep; social worker's supportive dialogue → exclude

## Example

**Input:**
```
00:01:19,740|00:01:21,740|J.A.和贾斯汀。
00:01:27,080|00:01:27,920|- R-R-T-R。
00:04:51,460|00:04:54,860|做美普罗斯托米，还有一个小肠梗阻
00:04:54,860|00:04:58,140|等手术等了三个小时。
00:04:58,140|00:05:02,820|克拉肯还在急诊室留观。
00:09:43,020|00:09:44,540|CT和血管造影阴性。
00:09:47,820|00:09:49,140|- 他们复查血细胞比容了吗？
00:09:50,900|00:09:52,660|- 用头孢曲松出院，明天复查，
00:48:22,860|00:48:24,780|- 帮助他，保护他，拯救他。
```

**Output (filtered):**
```
00:04:51,460|00:04:54,860|做美普罗斯托米，还有一个小肠梗阻
00:04:54,860|00:04:58,140|等手术等了三个小时。
00:04:58,140|00:05:02,820|克拉肯还在急诊室留观。
00:09:43,020|00:09:44,540|CT和血管造影阴性。
00:09:47,820|00:09:49,140|- 他们复查血细胞比容了吗？
00:09:50,900|00:09:52,660|- 用头孢曲松出院，明天复查，
```

Note: Lines without medical terms (names, small talk) and social worker dialogues are excluded.

## Notes
- Preserve exact original timestamp format
- Do not modify or summarize the content
- Output should be a valid subtitle file in the same format as input
- Process line by line — each line is evaluated independently