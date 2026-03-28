#!/bin/bash
# Specter pre-edit hook — snapshots file before AI edits it
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
[ -z "$FILE_PATH" ] && exit 0
/usr/local/bin/specter pre-edit --file "$FILE_PATH" 2>/dev/null
exit 0
