import os

import pygame
import torch

from environment import Environment
from agent import DQNAgent


def main(mode="human"):
    env = Environment(renderMode=True)
    if mode == "human":
        # Reset the environment to get the initial state
        state = env.reset()
        done = False
        while not done:
            # Handle Pygame events
            action = "none"  # Default action if no key is pressed
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        action = 0  # Move drone right
                    elif event.key == pygame.K_LEFT:
                        action = 1  # Move drone left
                    elif event.key == pygame.K_DOWN:
                        action = 2  # Drop grenade
            # Perform the action in the environment
            state, reward, done, _ = env.step(action)
            # Render the environment if renderMode is enabled
            env.render()
            # Display the current observation (e.g., drone position, etc.)
            print(f"--- Simulation Status ---\n"
                  f"State: {state}\n"
                  f"Reward: {reward}\n"
                  f"Done: {done}\n"
                  f"------------------------")
        print("Episode finished!")

    elif mode == "training":
        env = Environment(renderMode=True)  # Enable rendering
        action_space = ["right", "left", "drop"]
        state_size = 9
        episodes = 5000

        agent = DQNAgent(state_size, len(action_space))

        # Create the directory to save models if it doesn't exist
        save_dir = "brains"
        os.makedirs(save_dir, exist_ok=True)

        for episode in range(episodes):
            state = env.reset()  # Reset the environment and get initial state
            total_reward = 0
            done = False
            steps = 0
            while not done:
                env.score = total_reward
                action = agent.act(state)  # Get action from agent
                next_state, reward, done, _ = env.step(action)  # Take action in the environment
                env.render()  # Ensure rendering happens
                pygame.event.get()  # Process Pygame events to avoid freezing
                agent.replay_buffer.add((state, action, reward, next_state, done))  # Add experience to replay buffer
                agent.train()  # Train the agent using replay buffer
                state = next_state  # Update state
                total_reward += reward
                steps += 1
                if steps > 200:
                    done = True
                    total_reward += -1000

            if (episode + 1) % 2 == 0:
                agent.decay_epsilon()
            
            print(f"--- Simulation Status ---\n"
                  f"Episode {episode+1}/{episodes}\n"
                  f"Total Reward: {total_reward}\n"
                  f"Epsilon: {agent.epsilon:.2f}\n"
                  f"Steps: {steps}\n"
                  f"------------------------")

            # Save the model every 100 episodes
            if (episode + 1) % 250 == 0:
                model_path = os.path.join(save_dir, f"model_episode_{episode+1}.pth")
                torch.save(agent.q_network.state_dict(), model_path)
                print(f"Model saved at episode {episode+1} to {model_path}")

    elif mode == "test":
        # Select a model from the brain folder
        model_name = ""
        model_path = os.path.join("brains", model_name)

        if not os.path.exists(model_path):
            print(f"Model file {model_path} not found!")
            return

        # Initialize agent and load the model
        action_space = ["right", "left", "drop"]
        state_size = 9
        agent = DQNAgent(state_size, len(action_space))
        agent.q_network.load_state_dict(torch.load(model_path))
        agent.q_network.eval()  # Set the model to evaluation mode

        print(f"Loaded model: {model_name}")

        # Run the model 10 times
        for trial in range(10):
            print(f"Trial {trial + 1}/10")
            state = env.reset()
            total_reward = 0
            done = False

            while not done:
                action = agent.act(state, greedy=True)  # Always take the best action
                state, reward, done, _ = env.step(action)
                env.render()
                pygame.event.get()  # Process Pygame events to avoid freezing
                total_reward += reward

            print(f"Trial {trial + 1} Total Reward: {total_reward}")

    env.close()


if __name__ == "__main__":
    main("training")
