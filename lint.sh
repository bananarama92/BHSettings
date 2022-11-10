#!/bin/bash

set -euo pipefail

# turn the detached message off
git config --global advice.detachedHead false

# Check if any changes have been made to the admin or ban list and, if so, append the commit message
cp room_settings.yaml /tmp/head.yaml
git checkout HEAD~1
cp room_settings.yaml /tmp/head_1.yaml
git checkout -
COMMIT_BEFORE=$(git log --format=%B -n 1 HEAD)
COMMIT_AFTER=$(python get_commit.py /tmp/head.yaml /tmp/head_1.yaml "$COMMIT_BEFORE")

# Check if any linting is required
HASH_BEFORE=$(python get_hash.py room_settings.yaml)
python lint.py room_settings.yaml
HASH_AFTER=$(python get_hash.py room_settings.yaml)
echo
echo "Pre-lint hash: $HASH_BEFORE"
echo "Post-lint hash: $HASH_BEFORE"
echo

if [[ "$HASH_BEFORE" != "$HASH_AFTER" || "$COMMIT_BEFORE" != "$COMMIT_AFTER" ]]; then
    echo "Changes detected; pushing updated room_settings.yaml file"
    git config --global user.name "GitHub Action"
    git config --local user.email "action@github.com"
    git add room_settings.yaml
    git commit --amend -m "$COMMIT_AFTER"
    git push --force
else
    echo "No changes detected"
fi
