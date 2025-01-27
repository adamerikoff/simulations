#!/bin/bash

# Check if mode is provided, if not, default to "human"
MODE=$1

if [ -z "$MODE" ]; then
  echo "No mode provided, defaulting to 'human'"
  MODE="human"
fi

# Execute the appropriate command based on the mode
if [ "$MODE" == "human" ]; then
  echo "Running in human mode..."
  python -m main  # This should run the human-mode script (main.py)
elif [ "$MODE" == "dqn" ]; then
  echo "Starting DQN training..."
  python -m agent.dqn_train  # This should run the training script (dqn_train.py)
else
  echo "Invalid mode. Please use 'human' or 'dqn'."
  exit 1
fi
