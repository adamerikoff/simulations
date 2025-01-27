import pygame

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
        ACTION_SPACE = ["right", "left", "drop"]
        STATE_SIZE = 9
        EPISODES = 1000
        # state = [
        #     observation["drone_position"].x, observation["drone_position"].y,
        #     observation["grenade_position"].x, observation["grenade_position"].y,
        #     observation["target_position"].x, observation["target_position"].y,
        #     observation["wind_vector"].x, observation["wind_vector"].y,
        #     observation["released_grenade"]
        # ]

        agent = DQNAgent(STATE_SIZE, len(ACTION_SPACE))

        for episode in range(EPISODES):
            state = env.reset()  # Reset the environment and get initial state
            total_reward = 0
            done = False

            while not done:
                action = agent.act(state)  # Get action from agent
                next_state, reward, done, _ = env.step(action)  # Take action in the environment
                # Render the environment if renderMode is enabled
                env.render()
                # Display the current observation (e.g., drone position, etc.)
                print(f"--- Simulation Status ---\n"
                    f"State: {state}\n"
                    f"Reward: {reward}\n"
                    f"Done: {done}\n"
                    f"------------------------")
                agent.replay_buffer.add((state, action, reward, next_state, done))  # Add experience to the replay buffer
                agent.train()  # Train the agent using the experiences in the replay buffer
                state = next_state  # Update the state
                total_reward += reward

            print(f"Episode {episode+1}/{EPISODES}, Total Reward: {total_reward}, Epsilon: {agent.epsilon:.2f}")
    env.close()
    
if __name__ == "__main__":
    main("training")
