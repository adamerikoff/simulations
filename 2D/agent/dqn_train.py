import torch
import random
from env.environment import Environment
from agent.dqn import DQNAgent

def train_dqn(agent, environment, num_episodes=1000, update_target_every=10):
    episode_rewards = []
    
    for episode in range(num_episodes):
        state = environment.reset()
        done = False
        total_reward = 0
        
        while not done:
            # Agent takes action using the DQN agent
            action = agent.act(state)  # Get action from agent
            
            # Step the environment
            next_state, reward, done, _ = environment.step(action, render=True)
            
            # Store the experience in replay buffer
            agent.remember(state, action, reward, next_state, done)
            
            # Perform learning step (experience replay)
            agent.replay()
            
            # Update state
            state = next_state
            total_reward += reward
        
        # Update target network periodically
        if episode % update_target_every == 0:
            agent.update_target_network()

        episode_rewards.append(total_reward)
        print(f"Episode {episode+1}/{num_episodes}, Total Reward: {total_reward}, Epsilon: {agent.epsilon:.2f}")

    return episode_rewards

# Initialize DQN agent
input_dim = len(Environment().get_state())  # State vector size from environment's get_state method
output_dim = len(Environment().action_space)  # Number of possible actions (1, 2, 3)
agent = DQNAgent(input_dim, output_dim)

# Create the environment in RL mode
env = Environment(mode="rl")

# Start training the DQN agent
rewards = train_dqn(agent, env)