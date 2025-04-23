import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 创建x和y的范围
x = np.linspace(0, 10, 100)
y = np.linspace(-5, 5, 100)
z = np.linspace(-5, 5, 100)

# 创建抛物柱面
# 方法1：生成柱面上的点
theta = np.linspace(0, 2*np.pi, 100)
y_cylinder = np.sqrt(2*x) * np.cos(theta[:,None])
z_cylinder = np.sqrt(2*x) * np.sin(theta[:,None])
X_cylinder, Y_cylinder = np.meshgrid(x, y)

# 创建3D图形
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# 更清晰地绘制抛物柱面
u = np.linspace(-5, 5, 50)  # z轴范围
v = np.linspace(0, 10, 100)  # x轴范围
U, V = np.meshgrid(u, v)
Y = np.sqrt(2*V)
X = V

# 绘制柱面两侧
ax.plot_surface(X, Y, U, color='red', alpha=0.5)
ax.plot_surface(X, -Y, U, color='blue', alpha=0.5)

# 绘制z=0平面的抛物线
ax.plot(x, np.sqrt(2*x), 0, color='green', linewidth=3, label='y²=2x')
ax.plot(x, -np.sqrt(2*x), 0, color='green', linewidth=3)

# 设置坐标轴标签和视角
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')
ax.set_title('Parabola y² = 2x')
ax.view_init(elev=30, azim=45)  # 调整视角

# 添加图例
ax.legend()

# 显示图形
plt.tight_layout()
plt.show()
