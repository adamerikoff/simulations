import matplotlib.pyplot as plt
import numpy as np

# Read data from the CSV file
data = np.genfromtxt('plot_data.csv', delimiter=',')

# Extract x and y values
x = data[:, 0]
y = data[:, 1]

# Create the plot
plt.plot(x, y)

# Add labels and title
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Plot from plot_data.csv')

# Show the plot
plt.show()