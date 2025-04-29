# 🧠 Knowledge Graph for IAM

A lightweight demo for integrating household–building–material–energy data into a Neo4j-powered knowledge graph, aiming to support data consistency validation and scenario input generation for Integrated Assessment Models (IAMs).

## 📁 Project Structure
├── data/processed/ # Cleaned CSV datasets (buildings, households, regions, etc.) ├── scripts/ # Python scripts for cleaning, graph building, IAM integration ├── run_all.py # Run all key steps in sequence ├── visualize_graph.py # Neo4j-based visualization (optional) └── requirements.txt # Python dependencies

## 🧩 Core Entities & Relations   

- `Household` —LOCATED_IN→ `Building`
- `Building` —BUILT_FROM→ `Material`
- `Building` —CONSUMES→ `EnergyUse`
- `Building` —IN_REGION→ `Region`

## 🚀 Quick Start

```bash
# Step 1: Install dependencies
pip install -r requirements.txt

# Step 2: Start Neo4j database locally

# Step 3: Run the pipeline
python run_all.py
```
# 🔍 Sample Neo4j Query

MATCH (b:Building)-[:CONSUMES]->(e:EnergyUse)
RETURN b.buildingID, e.type, e.amount

## 🎯 Motivation

This project demonstrates how to:

- ✅ Build a semantic + physical knowledge graph from CSV sources  
- 🧪 Validate consistency between housing, material, and energy data  
- 📊 Generate input tables for IAM frameworks (e.g., IMAGE, GCAM)

