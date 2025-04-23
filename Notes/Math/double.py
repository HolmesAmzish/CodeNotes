import numpy as np
import matplotlib.pyplot as plt

def generate_hyperbola(a, c):
    """
    Generates a graph of the hyperbola  \frac{x^2}{a^2} - \frac{z^2}{c^2} = 1.

    Args:
        a: The value of 'a' in the equation.
        c: The value of 'c' in the equation.
    """

    # Create a range of x values for the two branches
    x1 = np.linspace(a, 3*a, 400)  # Adjust the upper limit as needed
    x2 = np.linspace(-3*a, -a, 400) # Adjust the lower limit as needed

    # Calculate the corresponding z values for each branch
    z1_upper = c * np.sqrt((x1**2) / (a**2) - 1)
    z1_lower = -c * np.sqrt((x1**2) / (a**2) - 1)
    z2_upper = c * np.sqrt((x2**2) / (a**2) - 1)
    z2_lower = -c * np.sqrt((x2**2) / (a**2) - 1)

    # Create the graph
    plt.figure(figsize=(8, 6))
    plt.plot(x1, z1_upper, label=f'Upper branch (a={a}, c={c})', color='blue')
    plt.plot(x1, z1_lower, color='blue')
    plt.plot(x2, z2_upper, color='blue')
    plt.plot(x2, z2_lower, color='blue')

    plt.xlabel('x')
    plt.ylabel('z')
    plt.title(f'Graph of Hyperbola:  $\\frac{{x^2}}{{{a^2}}} - \\frac{{z^2}}{{{c^2}}} = 1$  (a={a}, c={c})')
    plt.axvline(a, color='gray', linestyle='--')
    plt.axvline(-a, color='gray', linestyle='--')
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.legend()
    plt.grid(True)
    plt.axis('equal')
    plt.show()

# Example usage:
a = 2
c = 3
generate_hyperbola(a, c)

a = 1
c = 1
generate_hyperbola(a, c)

# 设置参数
a = 1
c = 1
u = np.linspace(-2, 2, 100)
v = np.linspace(0, 2 * np.pi, 100)
u, v = np.meshgrid(u, v)

# 1. 绘制旋转单叶双曲面 (绕 z 轴)
fig1 = plt.figure(figsize=(8, 8))
ax1 = fig1.add_subplot(111, projection='3d')

x_single = a * np.cosh(u) * np.cos(v)
y_single = a * np.cosh(u) * np.sin(v)
z_single = c * np.sinh(u)

ax1.plot_surface(x_single, y_single, z_single, color='lightgreen', alpha=0.7)
ax1.set_xlabel('X')
ax1.set_ylabel('Y')
ax1.set_zlabel('Z')
ax1.set_title('Rotational Hyperboloid of One Sheet (around z-axis)')
ax1.set_xlim([-3, 3])
ax1.set_ylim([-3, 3])
ax1.set_zlim([-3, 3])

# 2. 绘制旋转双叶双曲面 (绕 x 轴)
fig2 = plt.figure(figsize=(8, 8))
ax2 = fig2.add_subplot(111, projection='3d')

# 上叶 (x >= a)
x_double_upper = a * np.cosh(u)
y_double_upper = c * np.sinh(u) * np.cos(v)
z_double_upper = c * np.sinh(u) * np.sin(v)
ax2.plot_surface(x_double_upper, y_double_upper, z_double_upper, color='skyblue', alpha=0.7)

# 下叶 (x <= -a)
x_double_lower = -a * np.cosh(u)
y_double_lower = c * np.sinh(u) * np.cos(v)
z_double_lower = c * np.sinh(u) * np.sin(v)
ax2.plot_surface(x_double_lower, y_double_lower, z_double_lower, color='lightcoral', alpha=0.7)

ax2.set_xlabel('X')
ax2.set_ylabel('Y')
ax2.set_zlabel('Z')
ax2.set_title('Rotational Hyperboloid of Two Sheets (around x-axis)')
ax2.set_xlim([-3, 3])
ax2.set_ylim([-3, 3])
ax2.set_zlim([-3, 3])

plt.show()