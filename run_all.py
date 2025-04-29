import os
import sys

PYTHON = r"D:\软件\Python\Python.3.10.6\python.exe"  # 你的python绝对路径

if __name__ == "__main__":
    print("=== Step 1: Cleaning and Merging Data ===")
    os.system(f'"{PYTHON}" scripts/data_processing/clean_and_merge.py')

    print("=== Step 2: Building Knowledge Graph ===")
    os.system(f'"{PYTHON}" scripts/kg_construction/build_kg.py')

    print("=== Step 3: Mapping IAM Input ===")
    os.system(f'"{PYTHON}" scripts/iam_integration/iam_mapper.py')

    print("=== All done! ===")
