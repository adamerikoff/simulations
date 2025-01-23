import torch
import torch.nn as nn
import torch.optim as optim
import random
import numpy as np
from collections import deque
import torch.nn.functional as F

class QNetwork(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(QNetwork, self).__init__()
        self.fc1 = nn.Linear(input_dim, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, output_dim)

    def forward(self, state):
        x = F.relu(self.fc1(state))
        x = F.relu(self.fc2(x))
        return self.fc3(x)
    
class DQNAgent:
    def __init__(self, input_dim, output_dim, gamma=0.99, epsilon=1.0, epsilon_min=0.01, epsilon_decay=0.995, lr=0.001, batch_size=32):
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration rate
        self.epsilon_min = epsilon_min  # Minimum epsilon (exploration)
        self.epsilon_decay = epsilon_decay  # Decay rate for epsilon
        self.batch_size = batch_size

        # Initialize Q-network and target network
        self.q_network = QNetwork(input_dim, output_dim)
        self.target_network = QNetwork(input_dim, output_dim)
        self.target_network.load_state_dict(self.q_network.state_dict())  # Copy weights from Q-network to target network

        # Set up optimizer
        self.optimizer = optim.Adam(self.q_network.parameters(), lr=lr)

        # Replay buffer
        self.memory = deque(maxlen=2000)
    
    def act(self, state):
        """Select action using epsilon-greedy policy"""
        if random.random() < self.epsilon:
            return random.choice(range(self.output_dim))  # Exploration: random action
        else:
            state = torch.tensor(state, dtype=torch.float32).unsqueeze(0)
            with torch.no_grad():
                q_values = self.q_network(state)
            return torch.argmax(q_values).item()  # Exploitation: action with highest Q-value

    def remember(self, state, action, reward, next_state, done):
        """Store experience in replay buffer"""
        self.memory.append((state, action, reward, next_state, done))

    def replay(self):
        """Experience replay: sample from memory and update Q-network"""
        if len(self.memory) < self.batch_size:
            return
        
        batch = random.sample(self.memory, self.batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)

        states = torch.tensor(states, dtype=torch.float32)
        next_states = torch.tensor(next_states, dtype=torch.float32)
        rewards = torch.tensor(rewards, dtype=torch.float32)
        dones = torch.tensor(dones, dtype=torch.float32)

        # Compute Q-values for current and next states
        q_values = self.q_network(states)
        next_q_values = self.target_network(next_states)

        # Compute target Q-values
        target_q_values = q_values.clone()
        for i in range(self.batch_size):
            target_q_values[i, actions[i]] = rewards[i] + self.gamma * torch.max(next_q_values[i]) * (1 - dones[i])

        # Compute loss (Mean Squared Error)
        loss = F.mse_loss(q_values, target_q_values)

        # Backpropagation
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        # Decay epsilon
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def update_target_network(self):
        """Soft update of the target network"""
        self.target_network.load_state_dict(self.q_network.state_dict())