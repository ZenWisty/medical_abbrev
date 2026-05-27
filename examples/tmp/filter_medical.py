#!/usr/bin/env python3
"""
Strict medical filter for subtitle files.
Keeps lines with clinical medical knowledge, excludes social worker/support dialogue.
"""

import re

# Clinical terms patterns - diseases, conditions, medications, procedures, vitals
CLINICAL_PATTERNS = [
    # Diseases/Conditions
    r'室颤', r'高钾血症', r'肾衰竭', r'横纹肌溶解', r'心肌梗死',
    r'心脏骤停', r'心室颤动', r'心脏填塞', r'脑出血', r'脑水肿',
    r'肺脓肿', r'误吸', r'肠梗阻', r'胆结石', r'阑尾炎',
    r'脓毒症', r'糖尿病', r'癫痫', r'创伤', r'骨折',
    r'脱位', r'烧伤', r'烫伤', r'高血压', r'低血压',
    r'心率', r'血压', r'血氧', r'体温', r'瞳孔',
    r'阿尔茨海默', r'肺气肿', r'心力衰竭', r'多发性硬化',
    r'脱水', r'呕吐', r'胸痛', r'腹痛', r'头痛',

    # Medications
    r'劳拉西泮', r'氯胺酮', r'吗啡', r'胰岛素', r'葡萄糖',
    r'头孢', r'阿奇霉素', r'甘露醇', r'利多卡因', r'肾上腺素',
    r'昂丹司琼', r'Keppra', r'布洛芬', r'泰诺',

    # Procedures
    r'CT', r'MRI', r'超声', r'透析', r'除颤', r'电击',
    r'心肺复苏', r'插管', r'胸外按压', r'静脉输液', r'输血',
    r'神经阻滞', r'缝合', r'包扎', r'引流', r'导管',
    r'气管插管', r'心电图', r'胸片', r'血管造影',

    # Lab values
    r'血细胞比容', r'肌酐', r'钾', r'钠', r'钙',
    r'乳酸', r'D-二聚体', r'血糖', r'血常规', r'生化',
    r'血培养',

    # Medical roles
    r'医生', r'护士', r'住院医', r'实习生', r'主治',
    r'急诊', r'ICU', r'病房',
]

# Patterns for social worker / psychological support - EXCLUDE these
EXCLUDE_PATTERNS = [
    r'社工',
    r'我是一本打开的书',
    r'你可以随时来找我',
    r'你怎么样了',
    r'你还好吗',
    r'帮助他',
    r'保护他',
    r'拯救他',
    r'悲伤',
    r'去世',
    r' grief',
    r' support',
    r'我们只是想确保',
    r'能应付',
    r'有可以倾诉的人',
    r'学校怎么样',
    r'你有什么喜欢的吗',
    r'照顾妈妈',
    r'你确定不想',
    r'别烦我',
    r'我们需要谈谈',
    r'我为你感谢',
    r'合十',
]

def is_clinical_line(line):
    """Check if line contains clinical medical knowledge."""
    # First check if it's clearly medical by matching clinical patterns
    has_clinical = any(re.search(pattern, line) for pattern in CLINICAL_PATTERNS)

    # Check if it's social worker / support dialogue
    has_exclude = any(re.search(pattern, line) for pattern in EXCLUDE_PATTERNS)

    # Check for common non-clinical patterns
    # Song lyrics
    if line.startswith('♪') or line.endswith('♪'):
        return False
    # Timestamps only
    if re.match(r'^\d{2}:\d{2}:\d{2}', line) and '|' not in line:
        return False
    # Sound effects
    if re.match(r'^\([^)]+\)$', line.strip()):
        return False

    return has_clinical and not has_exclude

def filter_file(input_path, output_path):
    """Filter subtitle file keeping only clinical medical content."""
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    filtered_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if is_clinical_line(line):
            filtered_lines.append(line)

    with open(output_path, 'w', encoding='utf-8') as f:
        for line in filtered_lines:
            f.write(line + '\n')

    print(f"Filtered {len(lines)} lines to {len(filtered_lines)} lines")
    print(f"Output written to: {output_path}")

if __name__ == '__main__':
    input_file = '/home/hyxseu/ws/Scrapy/medical_abbrev/data/speech/ThePITS01/ThePITS01E01_translate.md'
    output_file = '/home/hyxseu/ws/Scrapy/medical_abbrev/data/speech/ThePITS01/ThePITS01E01_translate_medfilt.md'
    filter_file(input_file, output_file)