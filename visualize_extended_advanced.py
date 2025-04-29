from py2neo import Graph
from pyvis.network import Network

# 连接 Neo4j
graph = Graph("bolt://localhost:7687", auth=("neo4j", "Ly19970215"))

# 创建 pyvis 图对象
net = Network(notebook=False, height="900px", width="100%", directed=True)
net.barnes_hut(gravity=-30000, central_gravity=0.3, spring_length=110, spring_strength=0.04, damping=0.09)

# 查询 Building 相关结构
query = """
MATCH (h:Household)-[:LOCATED_IN]->(b:Building)
OPTIONAL MATCH (b)-[:IN_REGION]->(r:Region)
OPTIONAL MATCH (b)-[:BUILT_FROM]->(m:Material)
OPTIONAL MATCH (b)-[:CONSUMES]->(e:EnergyUse)
RETURN h, b, r, m, e
LIMIT 300
"""

results = graph.run(query).data()

# 定义颜色映射
color_map = {
    "Low": "#bae7ff",
    "Medium": "#69c0ff",
    "High": "#0050b3"
}
urban_level_color = {
    "Urban": "#95de64",
    "Suburban": "#ffe58f",
    "Rural": "#ffccc7"
}

# 添加节点和边
for record in results:
    h = record.get("h")
    b = record.get("b")
    r = record.get("r")
    m = record.get("m")
    e = record.get("e")

    if h:
        income_color = color_map.get(h["IncomeLevel"], "#69c0ff")
        net.add_node(
            h["HouseholdID"],
            label="Household",
            title=f"HouseholdID: {h['HouseholdID']}\nIncome: {h['IncomeLevel']}\nPersons: {h['NumPersons']}",
            shape='dot',
            size=10,
            color=income_color
        )

    if b:
        net.add_node(
            b["BuildingID"],
            label="Building",
            title=f"BuildingID: {b['BuildingID']}\nArea: {b['Area']}\nYearBuilt: {b['YearBuilt']}\nEstimated Energy Use: {b['EstimatedEnergyUse']} kWh",
            shape='box',
            size=20,
            color="#ff7a45"
        )

    if r:
        urban_color = urban_level_color.get(r["UrbanLevel"], "#d3f261")
        net.add_node(
            r["RegionID"],
            label="Region",
            title=f"Region: {r['RegionName']}\nUrban Level: {r['UrbanLevel']}",
            shape='hexagon',
            size=15,
            color=urban_color
        )

    if m:
        net.add_node(
            m["Material"],
            label=f"Material\n{m['Material']}",
            title=f"Material: {m['Material']}\nThermal Conductivity: {m['ThermalConductivity']}\nCarbon Intensity: {m['CarbonIntensity']}",
            shape='ellipse',
            size=12,
            color="#ffd666"
        )

    if e:
        net.add_node(
            e["EnergyID"],
            label=f"Energy\n{e['EnergyType']}",
            title=f"Energy Type: {e['EnergyType']}\nAnnual Consumption: {e['AnnualConsumption_kWh']} kWh",
            shape='triangle',
            size=10,
            color="#5cdbd3"
        )

    # 添加边
    if h and b:
        net.add_edge(h["HouseholdID"], b["BuildingID"], label="LOCATED_IN", width=1)

    if b and r:
        net.add_edge(b["BuildingID"], r["RegionID"], label="IN_REGION", width=2)

    if b and m:
        net.add_edge(b["BuildingID"], m["Material"], label="BUILT_FROM", width=2)

    if b and e:
        net.add_edge(b["BuildingID"], e["EnergyID"], label="CONSUMES", width=2)

# 保存为HTML
net.set_options("""
var options = {
  "nodes": {
    "font": {"size": 16}
  },
  "edges": {
    "font": {"size": 12, "align": "middle"}
  },
  "layout": {
    "hierarchical": {
      "enabled": true,
      "levelSeparation": 200,
      "nodeSpacing": 200,
      "treeSpacing": 300,
      "direction": "LR",
      "sortMethod": "hubsize"
    }
  },
  "physics": {
    "enabled": false
  }
}
""")
net.show("extended_knowledge_graph_advanced.html")
print("✅ 高级版扩展知识图谱已生成：extended_knowledge_graph_advanced.html")
