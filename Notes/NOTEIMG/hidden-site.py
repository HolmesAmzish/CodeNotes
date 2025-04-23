import matplotlib.pyplot as plt
import numpy as np

# 定义节点位置
nodes = {'A': (-2, 0), 'B': (0, 0), 'C': (2, 0)}

# 定义传输范围 (简化为圆形)
radius_AB = 1.5
radius_BC = 1.5

# 创建圆形
circle_AB = plt.Circle(nodes['B'], radius_AB, color='lightblue', alpha=0.3)
circle_BC = plt.Circle(nodes['B'], radius_BC, color='lightcoral', alpha=0.3)

# 创建图形和子图
fig, ax = plt.subplots(figsize=(8, 4))

# 绘制节点
for node, pos in nodes.items():
    ax.plot(pos[0], pos[1], 'o', markersize=10, color='black')
    ax.text(pos[0], pos[1] - 0.3, f'节点{node}', ha='center')

# 绘制传输范围
ax.add_patch(circle_AB)
ax.add_patch(circle_BC)

# 绘制连接线
ax.plot([nodes['A'][0], nodes['B'][0]], [nodes['A'][1], nodes['B'][1]], '--', color='gray')
ax.plot([nodes['B'][0], nodes['C'][0]], [nodes['B'][1], nodes['C'][1]], '--', color='gray')

# 添加冲突示意
collision_x = nodes['B'][0] + 0.2
collision_y = nodes['B'][1] + 0.4
ax.text(collision_x, collision_y, '冲突!', color='red', fontsize=12, fontweight='bold')
ax.arrow(nodes['A'][0] + 0.5, nodes['A'][1] + 0.3, nodes['B'][0] - (nodes['A'][0] + 0.5) - 0.2, nodes['B'][1] - (nodes['A'][1] + 0.3) - 0.4, head_width=0.1, head_length=0.2, fc='blue', ec='blue')
ax.arrow(nodes['C'][0] - 0.5, nodes['C'][1] + 0.3, nodes['B'][0] - (nodes['C'][0] - 0.5) + 0.2, nodes['B'][1] - (nodes['C'][1] + 0.3) - 0.4, head_width=0.1, head_length=0.2, fc='green', ec='green')

# 设置坐标轴范围和标签
ax.set_xlim(-3, 3)
ax.set_ylim(-1, 1)
ax.set_xlabel("距离")
ax.set_ylabel(" ")
ax.set_title("隐藏站问题示意图")
ax.axis('off')  # 关闭坐标轴

# 显示图形
plt.grid(True)
plt.show()