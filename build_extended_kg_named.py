from py2neo import Graph, Node, Relationship
import pandas as pd

# 连接 Neo4j
graph = Graph("bolt://localhost:7687", auth=("neo4j", "Ly19970215"))

# 读取数据
buildings = pd.read_csv('./data/processed/extended_buildings.csv')
households = pd.read_csv('./data/processed/extended_households.csv')
regions = pd.read_csv('./data/processed/extended_regions.csv')
materials = pd.read_csv('./data/processed/extended_materials.csv')
energy = pd.read_csv('./data/processed/extended_energy.csv')

# 创建 Region 节点
for _, row in regions.iterrows():
    region = Node("Region",
                  RegionID=row["RegionID"],
                  RegionName=row["RegionName"],
                  UrbanLevel=row["UrbanLevel"],
                  name=row["RegionName"])
    graph.merge(region, "Region", "RegionID")

# 创建 Material 节点
for _, row in materials.iterrows():
    material = Node("Material",
                    Material=row["Material"],
                    ThermalConductivity=row["ThermalConductivity"],
                    CarbonIntensity=row["CarbonIntensity"],
                    name=row["Material"])
    graph.merge(material, "Material", "Material")

# 创建 Building 节点
for _, row in buildings.iterrows():
    building = Node("Building",
                    BuildingID=row["BuildingID"],
                    Area=row["Area"],
                    YearBuilt=row["YearBuilt"],
                    EstimatedEnergyUse=row["EstimatedEnergyUse"],
                    RegionID=row["RegionID"],
                    Material=row["Material"],
                    name=row["BuildingID"])
    graph.merge(building, "Building", "BuildingID")

    # 建立与 Region 的关系
    region = graph.nodes.match("Region", RegionID=row["RegionID"]).first()
    if region:
        graph.merge(Relationship(building, "IN_REGION", region))

    # 建立与 Material 的关系
    material = graph.nodes.match("Material", Material=row["Material"]).first()
    if material:
        graph.merge(Relationship(building, "BUILT_FROM", material))

# 创建 Household 节点及其关系
for _, row in households.iterrows():
    household = Node("Household",
                     HouseholdID=row["HouseholdID"],
                     NumPersons=row["NumPersons"],
                     IncomeLevel=row["IncomeLevel"],
                     name=row["HouseholdID"])
    graph.merge(household, "Household", "HouseholdID")

    building = graph.nodes.match("Building", BuildingID=row["BuildingID"]).first()
    if building:
        graph.merge(Relationship(household, "LOCATED_IN", building))

# 创建 EnergyUse 节点及其关系
for _, row in energy.iterrows():
    energy_node = Node("EnergyUse",
                       EnergyID=row["EnergyID"],
                       EnergyType=row["EnergyType"],
                       AnnualConsumption_kWh=row["AnnualConsumption_kWh"],
                       name=row["EnergyType"])
    graph.merge(energy_node, "EnergyUse", "EnergyID")

    building = graph.nodes.match("Building", BuildingID=row["BuildingID"]).first()
    if building:
        graph.merge(Relationship(building, "CONSUMES", energy_node))

print("✅ 知识图谱构建完成，所有节点已添加 name 属性用于可视化显示")
