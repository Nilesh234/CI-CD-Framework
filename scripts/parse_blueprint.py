#!/usr/bin/env python3
import os
import sys
import json
import yaml
from pathlib import Path

OUTPUT_DIR = "outputs"
BLUEPRINT_DIR = "blueprints"

def ensure_directory(path):
    """Ensure directory exists, create if not."""
    Path(path).mkdir(parents=True, exist_ok=True)

def load_blueprint_file():
    """Load blueprint file with validation."""
    blueprint_paths = [
        Path(BLUEPRINT_DIR) / "pipeline-blueprint.yaml",
        Path(BLUEPRINT_DIR) / "pipeline-blueprint.json",
        Path("pipeline-blueprint.yaml"),
        Path("pipeline-blueprint.json")
    ]
    
    for path in blueprint_paths:
        if path.exists():
            try:
                content = path.read_text()
                if path.suffix == '.yaml':
                    return yaml.safe_load(content) or {}
                return json.loads(content) or {}
            except Exception as e:
                sys.stderr.write(f"Error loading {path}: {str(e)}\n")
                sys.exit(1)
    
    sys.stderr.write("Error: No valid blueprint file found\n")
    sys.exit(1)

def write_outputs(config):
    """Write all output files with validation."""
    ensure_directory(OUTPUT_DIR)
    
    required_outputs = {
        "output_stages.json": json.dumps({
            "stages": config.get("stages", ["lint", "test", "build"])
        }),
        "output_tech.txt": config.get("technology", "unknown"),
        "output_deploy.txt": config.get("deployment", "none"),
        "output_build_type.txt": config.get("build_type", "full")
    }
    
    for filename, content in required_outputs.items():
        try:
            output_path = Path(OUTPUT_DIR) / filename
            output_path.write_text(content)
        except Exception as e:
            sys.stderr.write(f"Failed to write {filename}: {str(e)}\n")
            sys.exit(1)

def main():
    config = load_blueprint_file()
    write_outputs(config)
    print("Blueprint processed successfully")

if __name__ == "__main__":
    main()