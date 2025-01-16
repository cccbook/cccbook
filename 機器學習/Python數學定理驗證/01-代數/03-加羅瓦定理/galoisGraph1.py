import networkx as nx
import matplotlib.pyplot as plt

# 創建一個群結構的示意圖
G = nx.Graph()

# 假設這是加羅瓦群的一些操作
G.add_edges_from([(1, 2), (2, 3), (3, 1)])

# 繪製群結構圖
nx.draw(G, with_labels=True, font_weight='bold', node_size=1000)
plt.title("Group Structure of G")
plt.show()
