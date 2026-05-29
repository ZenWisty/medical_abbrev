---
name: video_speechtxt_shrink
description: Condenses a translated Chinese subtitle file into a topic-focused summary format. Use this skill whenever the user has a translated Chinese subtitle file (in 00:start|end|text format) and wants it condensed into topic-focused summary lines, or mentions shrinking subtitles, summarizing subtitles, or grouping subtitle lines by topic. Make sure to use this skill when the user wants to condense or summarize subtitle content.
compatibility: Read, Write, Bash
---

This skill condenses a translated Chinese subtitle file into a summary format, grouping adjacent lines that share a common topic into single summarized lines.

**Important**: Do not write any code to execute this skill. Instead, follow the steps below directly using Claude's built-in tools (Read, Write, Bash) to read input files, analyze content, and write output files. **严禁自己写代码或调用 anthropic SDK 来执行此 skill。**

When spawning a sub-agent (Agent tool) to assist with this skill, set `model: "opus"` or use the parent conversation's model so the sub-agent uses a capable model (not haiku).

## When to Use
When the user has a translated Chinese subtitle file (in `00:start|end|text` format) and wants it condensed into topic-focused summary lines, similar to `test_trans_shrink.md`.

## Input
1. `source_file` — the path to the translated Chinese subtitle file
2. `target_file` — the path where the condensed summary should be saved

## Output
A condensed subtitle file where each line follows the format:
```
00:xx:xx,xxx|00:xx:xx,xxx|**Topic Title** — Core point of this segment
```

Each output line represents one topic/segment, with:
- Merged timestamp range from the first to last line of that topic
- A bold topic title capturing the central theme
- A dash separator followed by a concise summary of the key points discussed

## Steps
1. Read the source file line by line
2. Analyze adjacent lines and identify topic boundaries — group lines that discuss the same theme
3. For each topic group:
   - Use the start timestamp of the first line and end timestamp of the last line
   - Derive a short bold topic title (e.g. `**研究问题的定义**`)
   - Summarize the core discussion into a concise phrase after the dash
4. Write all condensed lines to `target_file`
5. Confirm the file was saved successfully

## Example
Input lines about signing in, course credit vs audit explanation → Output single line:
```
00:00:00,000|00:00:26,000|**签到与课程介绍** — 统计选课人数，说明学分/旁听两种参与方式及分组规则
```

## Notes
- Each output line must be a single line (no wrapping)
- Topic titles should be short (3-8 characters) and descriptive
- The summary should be a concise phrase, not a full sentence
- Preserve the original meaning — do not add new information not present in the source