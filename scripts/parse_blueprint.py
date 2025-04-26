import os
import yaml
import json
from glob import glob

# Detect blueprint
blueprint_path = os.getenv('BLUEPRINT_PATH')

if not blueprint_path:
    candidates = glob('blueprints/pipeline-blueprint.*')
    if not candidates:
        raise FileNotFoundError("No blueprint file found.")
    blueprint_path = candidates[0]

# Parse YAML or JSON
if blueprint_path.endswith(('.yaml', '.yml')):
    with open(blueprint_path, 'r') as f:
        blueprint = yaml.safe_load(f)
elif blueprint_path.endswith('.json'):
    with open(blueprint_path, 'r') as f:
        blueprint = json.load(f)
else:
    raise ValueError("Unsupported blueprint file type.")

# Set outputs
print(f"::set-output name=technology::{blueprint['technology']}")
print(f"::set-output name=build_type::{blueprint['build_type']}")
print(f"::set-output name=deployment_method::{blueprint['deployment_method']}")

branching_strategy = blueprint.get('branching_strategy', {})
allowed_branches = ",".join(branching_strategy.get('allowed_branches', []))
semantic_versioning = str(branching_strategy.get('semantic_versioning', False)).lower()

print(f"::set-output name=allowed_branches::{allowed_branches}")
print(f"::set-output name=semantic_versioning::{semantic_versioning}")