import random 

import pygame

from env.environment import Environment

MODE = "human"

def main():
    env = Environment(mode=MODE)
    if MODE == "human":
        # Run in human mode
        env.run()
    else:
        print("Starting agent simulation...")
        state = env.reset()
        done = False
        while not done:
            # Handle basic Pygame events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # Random action selection for demonstration
            action = random.choice(env.action_space)
            state, reward, done, info = env.step(action, render=True)
            print(f"State: {state}, Reward: {reward}, Done: {done}")

if __name__ == "__main__":
    main()
