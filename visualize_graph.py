from py2neo import Graph
from pyvis.network import Network

# 连接 Neo4j 图数据库
graph = Graph("bolt://localhost:7687", auth=("neo4j", "Ly19970215"))

# 创建 pyvis 图对象
net = Network(notebook=False, height="700px", width="100%", directed=True)
net.force_atlas_2based()

# 查询 Household-LOCATED_IN->Building 关系
query = """
MATCH (h:Household)-[r:LOCATED_IN]->(b:Building)
RETURN h.HouseholdID AS hid, h.NumPersons AS np, b.BuildingID AS bid
LIMIT 100
"""

results = graph.run(query).data()

# 添加节点和边
for record in results:
    hid = record["hid"]
    bid = record["bid"]
    np = record["np"]

    net.add_node(hid, label=hid, title=f"Household\nPersons: {np}", shape='dot', color="#69c0ff")
    net.add_node(bid, label=bid, title="Building", shape='box', color="#ff7a45")
    net.add_edge(hid, bid, label="LOCATED_IN")

# 保存为HTML
net.show("household_building_graph.html")
print("✅ 图谱已保存为 household_building_graph.html")
