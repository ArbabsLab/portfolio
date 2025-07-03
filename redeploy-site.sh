#!/bin/bash


# 1. Kill all existing tmux sessions
echo "Killing all existing tmux sessions"
tmux list-sessions -F "#{session_name}" 2>/dev/null | xargs -r -n 1 tmux kill-session -t

# 2. Project directory
PROJECT_DIR=~/portfolio
cd "$PROJECT_DIR"

# 3. Fetch changes from main
echo "Fetching latest changes from main"
git fetch
git reset origin/main --hard

# 4. Activate virtual environment and install dependencies
VENV_DIR=python3-virtualenv
source "$VENV_DIR/bin/activate"
echo "Installing Python dependencies"
pip install -r requirements.txt
deactivate

# 5. Start a new detached tmux session and run Flask server
SESSION_NAME=flask-server
echo "Starting Flask server in new tmux session: $SESSION_NAME"
tmux new-session -d -s "$SESSION_NAME" bash -c "
    cd \"$PROJECT_DIR\"
    source \"$VENV_DIR/bin/activate\"
    echo 'Starting Flask server'
    flask run --host=0.0.0.0 --port=5000 "
echo "Deployment complete."

