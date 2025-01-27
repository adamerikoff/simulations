import pygame

from environment import Environment

def main():
    # Initialize the environment with rendering mode enabled
    env = Environment(renderMode=True)
    
    # Reset the environment to get the initial state
    observation = env.reset()

    running = True
    while running:
        # Handle Pygame events
        action = "none"  # Default action if no key is pressed
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    action = "left"  # Move drone left
                elif event.key == pygame.K_RIGHT:
                    action = "right"  # Move drone right
                elif event.key == pygame.K_DOWN:
                    action = "drop"  # Drop grenade
        
        # Perform the action in the environment
        observation, reward, done, _ = env.step(action)
        # Render the environment if renderMode is enabled
        env.render()
        # Display the current observation (e.g., drone position, etc.)
        print(f"--- Simulation Status ---\n"
              f"State: {observation}\n"
              f"Reward: {reward}\n"
              f"Done: {done}\n"
              f"------------------------")

        # Check if the episode is done (e.g., max steps or grenade hit target)
        if done:
            print("Episode finished!")
            break
    
    # Close the environment and quit Pygame
    env.close()

if __name__ == "__main__":
    main()
