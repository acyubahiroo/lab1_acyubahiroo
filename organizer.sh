#!/bin/bash
#
# organizer.sh
# Archives the current grades.csv file into an "archive" folder with a
# timestamped filename, resets the workspace with a fresh empty grades.csv,
# and logs every run to organizer.log.

SOURCE_FILE="grades.csv"
ARCHIVE_DIR="archive"
LOG_FILE="organizer.log"

# ---------------------------------------------------------------------
# 1. Make sure the source file actually exists before doing anything
# ---------------------------------------------------------------------
if [ ! -f "$SOURCE_FILE" ]; then
    echo "Error: '$SOURCE_FILE' not found in the current directory. Nothing to archive."
    exit 1
fi

# ---------------------------------------------------------------------
# 2. Check if the archive directory exists; create it if it doesn't
# ---------------------------------------------------------------------
if [ ! -d "$ARCHIVE_DIR" ]; then
    mkdir "$ARCHIVE_DIR"
    echo "Created archive directory: $ARCHIVE_DIR"
fi

# ---------------------------------------------------------------------
# 3. Generate a timestamp string
# ---------------------------------------------------------------------
TIMESTAMP=$(date +"%Y%m%d-%H%M%S")

# ---------------------------------------------------------------------
# 4. Build the new, timestamped filename and move it to the archive
# ---------------------------------------------------------------------
NEW_FILENAME="grades_${TIMESTAMP}.csv"
mv "$SOURCE_FILE" "$ARCHIVE_DIR/$NEW_FILENAME"

# ---------------------------------------------------------------------
# 5. Workspace Reset: create a fresh, empty grades.csv
# ---------------------------------------------------------------------
touch "$SOURCE_FILE"

# ---------------------------------------------------------------------
# 6. Logging: append the details of this run to organizer.log
# ---------------------------------------------------------------------
echo "[$TIMESTAMP] Archived '$SOURCE_FILE' as '$ARCHIVE_DIR/$NEW_FILENAME'" >> "$LOG_FILE"

echo "Archiving complete."
echo "  Original file moved to: $ARCHIVE_DIR/$NEW_FILENAME"
echo "  New empty '$SOURCE_FILE' created."
echo "  Log entry added to: $LOG_FILE"
