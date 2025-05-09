from graphviz import Digraph

def draw_decision_tree():
    dot = Digraph(comment='手续费计算判定树', format='png')
    dot.attr(rankdir='TB')  # 从上到下绘制

    # 根节点
    dot.node('A', '交易总金额')
    
    # 分支1：<1000
    dot.node('B', '<1000?')
    dot.edge('A', 'B')
    
    # 分支1.1：是
    dot.node('C', '每股售价')
    dot.edge('B', 'C', label='是')
    
    # 分支1.1.1：<14
    dot.node('D', '<14?')
    dot.edge('C', 'D')
    dot.node('E', '基本手续费=8.4%')
    dot.edge('D', 'E', label='是')
    
    # 分支1.1.2：14-25
    dot.node('F', '14-25?')
    dot.edge('C', 'F')
    dot.edge('F', 'E', label='是')
    dot.node('G', '基本手续费=8.4%')  # 与E相同
    dot.edge('F', 'G', label='否')
    dot.edge('G', 'E')  # 合并到E
    
    # 分支1.1.3：股数是否100倍数？
    dot.node('H', '股数是否100倍数？')
    dot.edge('C', 'H')
    dot.node('I', '附加手续费=5%/2%/1%')
    dot.edge('H', 'I', label='是')
    dot.node('J', '附加手续费=9%/6%/4%')
    dot.edge('H', 'J', label='否')
    
    # 分支1.2：否（1000-10000）
    dot.node('R', '1000-10000?')
    dot.edge('B', 'R', label='否')
    dot.node('S', '基本手续费=5%+34')
    dot.edge('R', 'S', label='是')
    
    # 分支1.3：>10000
    dot.node('T', '基本手续费=4%+134')
    dot.edge('R', 'T', label='否')  # 注意：这里逻辑有误，应直接连接B→T
    
    # 修正逻辑：>10000的分支应从A直接连接
    dot.node('T', '基本手续费=4%+134')
    dot.edge('A', 'T', style='dashed', label='>10000?')  # 重新连接
    
    # 合并附加手续费逻辑
    dot.node('K', '附加手续费')
    dot.edge('I', 'K', label='5%/2%/1%')
    dot.edge('J', 'K', label='9%/6%/4%')
    
    # 最终手续费计算
    dot.node('Q', '最终手续费=总金额×(基本手续费+附加手续费)')
    dot.edge('E', 'Q', style='invis')  # 连接所有基本手续费到Q
    dot.edge('G', 'Q', style='invis')
    dot.edge('S', 'Q', style='invis')
    dot.edge('T', 'Q', style='invis')
    dot.edge('K', 'Q')
    
    # 保存并渲染
    dot.render('fee_decision_tree', view=True)

draw_decision_tree()
