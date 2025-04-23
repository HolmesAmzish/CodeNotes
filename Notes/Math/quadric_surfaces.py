import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Create a 2x3 grid of subplots
fig = plt.figure(figsize=(18, 12))
plt.subplots_adjust(wspace=0.3, hspace=0.3)

# Common parameters
u = np.linspace(-2, 2, 50)
v = np.linspace(0, 2*np.pi, 50)
U, V = np.meshgrid(u, v)

# 1. Elliptic Cone: (x²/1) + (y²/1) - (z²/1) = 0
ax1 = fig.add_subplot(231, projection='3d')
X = U * np.cos(V)
Y = U * np.sin(V)
Z = U
ax1.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)
ax1.plot_surface(X, Y, -Z, cmap='viridis', alpha=0.8)
ax1.set_title('Elliptic Cone\n$\\frac{x^2}{a^2} + \\frac{y^2}{b^2} = \\frac{z^2}{c^2}$')

# 2. Ellipsoid: (x²/1) + (y²/1) + (z²/2) = 1
ax2 = fig.add_subplot(232, projection='3d')
X = np.outer(np.cos(U), np.sin(V))
Y = np.outer(np.sin(U), np.sin(V))
Z = np.outer(np.ones_like(U), np.cos(V)) * 1.5
ax2.plot_surface(X, Y, Z, cmap='plasma', alpha=0.8)
ax2.set_title('Ellipsoid\n$\\frac{x^2}{a^2} + \\frac{y^2}{b^2} + \\frac{z^2}{c^2} = 1$')

# 3. Hyperboloid of One Sheet: (x²/1) + (y²/1) - (z²/2.25) = 1
ax3 = fig.add_subplot(233, projection='3d')
X = np.sqrt(0.6 + U**2) * np.cos(V)
Y = np.sqrt(0.6 + U**2) * np.sin(V)
Z = U
ax3.plot_surface(X, Y, Z, cmap='inferno', alpha=0.8)
ax3.set_title('Hyperboloid of One Sheet\n$\\frac{x^2}{a^2} + \\frac{y^2}{b^2} - \\frac{z^2}{c^2} = 1$')

# 4. Hyperboloid of Two Sheets: (x²/1) + (y²/1) - (z²/1) = -1
ax4 = fig.add_subplot(234, projection='3d')
u = np.linspace(-2, -1.1, 25)  # Negative range for one sheet
u = np.append(u, np.linspace(1.1, 2, 25))  # Positive range for other sheet
v = np.linspace(0, 2*np.pi, 50)
U, V = np.meshgrid(u, v)

X = np.sqrt(U**2 - 1) * np.cos(V)
Y = np.sqrt(U**2 - 1) * np.sin(V)
Z = U
ax4.plot_surface(X, Y, Z, cmap='magma', alpha=0.8)
ax4.plot_surface(X, Y, -Z, cmap='magma', alpha=0.8)
ax4.set_title('Hyperboloid of Two Sheets\n$\\frac{x^2}{a^2} + \\frac{y^2}{b^2} - \\frac{z^2}{c^2} = -1$')

# 5. Elliptic Paraboloid: z = (x²/1) + (y²/1)
ax5 = fig.add_subplot(235, projection='3d')
X, Y = np.meshgrid(np.linspace(-2, 2, 50), np.linspace(-2, 2, 50))
Z = X**2 + Y**2
ax5.plot_surface(X, Y, Z, cmap='cool', alpha=0.8)
ax5.set_title('Elliptic Paraboloid\n$z = \\frac{x^2}{a^2} + \\frac{y^2}{b^2}$')

# 6. Hyperbolic Paraboloid: z = (x²/1) - (y²/1)
ax6 = fig.add_subplot(236, projection='3d')
X, Y = np.meshgrid(np.linspace(-2, 2, 50), np.linspace(-2, 2, 50))
Z = X**2 - Y**2
ax6.plot_surface(X, Y, Z, cmap='spring', alpha=0.8)
ax6.set_title('Hyperbolic Paraboloid\n$z = \\frac{x^2}{a^2} - \\frac{y^2}{b^2}$')

plt.tight_layout()
plt.savefig('Notes/Math/quadric_surfaces.png')
plt.show()
