#!/bin/bash
# Specter prompt capture — sends prompt metadata to Specter API for analytics
# Buffer stdin first, then run in background to avoid blocking Claude Code
INPUT=$(cat)
echo "$INPUT" | /home/kloud/Desktop/SpectreAI/specter prompt-capture &
exit 0
