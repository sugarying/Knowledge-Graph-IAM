# AI-KG-for-IAM

This project demonstrates how to construct a small Knowledge Graph integrating Dutch household and building data, and export it for use in Integrated Assessment Models (IAM).

## Project Structure

- `data/processed/`: Cleaned CSV datasets
- `scripts/data_processing/clean_and_merge.py`: Data cleaning script
- `scripts/kg_construction/build_kg.py`: Neo4j KG construction
- `scripts/iam_integration/iam_mapper.py`: IAM input extraction
- `run_all.py`: One-click running

## Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Make sure your Neo4j is running locally on `bolt://localhost:7687`, username `neo4j`, password `password`.

Run the full pipeline:

```bash
python run_all.py
```
