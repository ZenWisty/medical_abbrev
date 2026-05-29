---
name: video_speechtxt_translate
description: Translates a bilingual subtitle file (speech text with timestamps) into Chinese. Use this skill whenever the user provides a BV*_subtitle.md file path (from bilibili video speech text) and asks to translate it to Chinese, or mentions translating subtitle files, bilingual subtitles, or converting English subtitles to Chinese. Make sure to use this skill when the user wants to translate video speech text with timestamps.
compatibility: Read, Write, Bash
---

This skill translates a bilingual subtitle file (speech text with timestamps) into Chinese, preserving the per-line timestamp format.

**Important**: Do not write any code to execute this skill. Instead, follow the steps below directly using Claude's built-in tools (Read, Write, Bash) to read input files, translate content, and write output files. **严禁自己写代码或调用 anthropic SDK 来执行此 skill。**

When spawning a sub-agent (Agent tool) to assist with this skill, set `model: "opus"` or use the parent conversation's model so the sub-agent uses a capable model (not haiku).

## When to Use
When the user provides a `BV*_subtitle.md` file path (from bilibili video speech text) and wants it translated to Chinese and saved to a target `.md` location.

## Input
1. `source_file` — the path to the source subtitle file (e.g. `BV1Ra5K61EQ4_P2_P2_P2_subtitle.md`)
2. `target_file` — the path where the translated Chinese `.md` should be saved

## Output
A translated Chinese subtitle file where each line follows the format:
```
00:21:20,280|00:21:22,520|比如构建成一个连贯的教学法。
```

## Steps
1. Read the source file — it contains lines in the format `start_time|end_time|english_text`
2. Translate each line's text content from English to Chinese, keeping the `start_time|end_time|` prefix unchanged
3. Write the translated lines to `target_file`, preserving the exact same per-line format
4. Confirm the file was saved successfully

## Notes
- The timestamp prefix (`00:xx:xx,xxx|00:xx:xx,xxx|`) must be preserved exactly as-is
- Only translate the speech text portion after the second pipe `|`
- Do not reorder, merge, or modify any lines — output line count must equal input line count