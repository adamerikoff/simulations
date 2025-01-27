import torch
import torch.nn as nn
import torch.nn.functional as F

import torch.optim as optim
import random
import numpy as np
from collections import deque

class QNetwork(nn.Module):
    def __init__(self, state_size, action_size):
        super(QNetwork, self).__init__()
        # Define the layers of the neural network
        self.fc1 = nn.Linear(state_size, 1024)  # Input to first hidden layer
        self.fc2 = nn.Linear(1024, 512)  # Second hidden layer
        self.fc3 = nn.Linear(512, 256)  # Third hidden layer
        self.fc4 = nn.Linear(256, 128)  # Fourth hidden layer
        self.fc5 = nn.Linear(128, 64)   # Fifth hidden layer
        self.fc6 = nn.Linear(64, 32)    # Sixth hidden layer
        self.fc7 = nn.Linear(32, 16)    # Seventh hidden layer
        self.fc8 = nn.Linear(16, 8)     # Eighth hidden layer
        self.fc9 = nn.Linear(8, 4)      # Ninth hidden layer
        self.fc10 = nn.Linear(4, 2)     # Tenth hidden layer
        self.fc11 = nn.Linear(2, 1)     # Eleventh hidden layer
        self.fc12 = nn.Linear(1, action_size)  # Output layer (Q-values for each action)
    
    def forward(self, state):
        # Apply activation functions after each layer
        x = F.relu(self.fc1(state))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        x = F.relu(self.fc4(x))
        x = F.relu(self.fc5(x))
        x = F.relu(self.fc6(x))
        x = F.relu(self.fc7(x))
        x = F.relu(self.fc8(x))
        x = F.relu(self.fc9(x))
        x = F.relu(self.fc10(x))
        x = F.relu(self.fc11(x))
        return self.fc12(x)  # Output Q-values for each action
    
class ReplayBuffer:
    def __init__(self, buffer_size, batch_size):
        self.buffer = deque(maxlen=buffer_size)
        self.batch_size = batch_size

    def add(self, experience):
        self.buffer.append(experience)

    def sample(self):
        return random.sample(self.buffer, self.batch_size)

    def size(self):
        return len(self.buffer)
    
class DQNAgent:
    def __init__(self, state_size, action_size, learning_rate=0.001, gamma=0.99, epsilon=1.0, epsilon_min=0.01, epsilon_decay=0.995):
        self.state_size = state_size
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration rate
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        # Initialize the Q-network and optimizer
        self.q_network = QNetwork(state_size, action_size)
        self.optimizer = optim.Adam(self.q_network.parameters(), lr=self.learning_rate)
        # Replay buffer
        self.replay_buffer = ReplayBuffer(buffer_size=5000, batch_size=128)

    def act(self, state):
        # Epsilon-greedy policy
        if random.random() <= self.epsilon:
            return random.randint(0, self.action_size - 1)  # Explore: Random action
        state = torch.FloatTensor(state).unsqueeze(0)  # Convert state to tensor
        q_values = self.q_network(state)  # Get Q-values from the network
        return torch.argmax(q_values).item()  # Exploit: Action with max Q-value

    def train(self):
        if self.replay_buffer.size() < self.replay_buffer.batch_size:
            return
        # Sample a batch from the replay buffer
        batch = self.replay_buffer.sample()
        # Prepare the batch for training
        states, actions, rewards, next_states, dones = zip(*batch)
        states = torch.FloatTensor(states)
        next_states = torch.FloatTensor(next_states)
        actions = torch.LongTensor(actions)
        rewards = torch.FloatTensor(rewards)
        dones = torch.FloatTensor(dones)
        # Get Q-values for the current states and next states
        q_values = self.q_network(states)
        next_q_values = self.q_network(next_states)
        # Select the Q-values corresponding to the chosen actions
        q_value = q_values.gather(1, actions.unsqueeze(1)).squeeze(1)
        # Compute the target Q-values using the Bellman equation
        target_q_value = rewards + (self.gamma * next_q_values.max(1)[0] * (1 - dones))
        # Compute the loss (mean squared error)
        loss = nn.MSELoss()(q_value, target_q_value)
        # Update the Q-network
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
    
    def decay_epsilon(self):
        # Decay epsilon
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
