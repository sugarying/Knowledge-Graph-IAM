import pandas as pd

def map_for_iam():
    buildings = pd.read_csv('./data/processed/buildings.csv')
    iam_input = buildings[['BuildingID', 'EstimatedEnergyUse']]
    iam_input.to_csv('./data/processed/iam_input.csv', index=False)
    print("IAM input table saved at ./data/processed/iam_input.csv")

if __name__ == "__main__":
    map_for_iam()
