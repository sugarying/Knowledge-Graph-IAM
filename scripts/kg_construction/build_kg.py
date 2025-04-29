from py2neo import Graph, Node, Relationship
import pandas as pd

def build_knowledge_graph():
    graph = Graph("bolt://localhost:7687", auth=("neo4j", "Ly19970215"))

    buildings = pd.read_csv('./data/processed/buildings.csv')
    households = pd.read_csv('./data/processed/households.csv')

    # 创建 Building 节点
    for _, row in buildings.iterrows():
        building = Node(
            "Building",
            BuildingID=row['BuildingID'],
            Material=row['Material'],
            YearBuilt=int(row['YearBuilt']),
            Area=float(row['Area']),
            EstimatedEnergyUse=float(row['EstimatedEnergyUse'])
        )
        graph.merge(building, "Building", "BuildingID")

    # 创建 Household 节点 + LOCATED_IN 关系
    for _, row in households.iterrows():
        household = Node(
            "Household",
            HouseholdID=row['HouseholdID'],
            NumPersons=int(row['NumPersons'])
        )
        graph.merge(household, "Household", "HouseholdID")

        # 匹配已存在节点（更鲁棒写法）
        household_node = graph.nodes.match("Household", HouseholdID=row['HouseholdID']).first()
        building_node = graph.nodes.match("Building", BuildingID=row['BuildingID']).first()

        if household_node and building_node:
            relation = Relationship(household_node, "LOCATED_IN", building_node)
            graph.merge(relation)
        else:
            print(f"❗未找到匹配的节点：{row['HouseholdID']} -> {row['BuildingID']}")

if __name__ == "__main__":
    build_knowledge_graph()
