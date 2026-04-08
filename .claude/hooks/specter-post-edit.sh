#!/bin/bash
# Specter post-edit hook — records AI attribution after AI edits a file
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
[ -z "$FILE_PATH" ] && exit 0
/home/kloud/Desktop/SpectreAI/specter post-edit --file "$FILE_PATH" --agent claude-code --model claude-opus-4-6 2>/dev/null
exit 0
