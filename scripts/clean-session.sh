# 1. Check current total size (so you can see how much you'll reclaim)
du -sh ~/.claude/projects

# 2. Create a timestamped backup OUTSIDE ~/.claude (so Claude Code never touches it)
BACKUP_DIR=~/claude-session-backup-$(date +%Y%m%d-%H%M%S)
mkdir -p "$BACKUP_DIR"
cp -r ~/.claude/projects "$BACKUP_DIR"/

# 3. Verify the backup was created and has content
du -sh "$BACKUP_DIR"
ls "$BACKUP_DIR/projects" | head -5

# 4. Delete all .jsonl session files across every project
find ~/.claude/projects -type f -name "*.jsonl" -delete

# 5. Also delete any sub-session directories (some sessions have folders alongside .jsonl files)
find ~/.claude/projects -mindepth 2 -type d -empty -delete

# 6. Verify reclaimed space
du -sh ~/.claude/projects

# 7. Confirm backup is intact
echo "Backup location: $BACKUP_DIR"
du -sh "$BACKUP_DIR"