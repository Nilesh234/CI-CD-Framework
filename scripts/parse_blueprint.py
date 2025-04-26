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
    """Load blueprint file with multiple fallback options."""
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
                print(f"Error loading {path}: {str(e)}", file=sys.stderr)
    
    print("Warning: No valid blueprint file found", file=sys.stderr)
    return {
        "technology": "unknown",
        "deployment": "none",
        "build_type": "full",
        "stages": [],
        "deployment_target": {}
    }

def write_outputs(config):
    """Write all output files with atomic writes."""
    ensure_directory(OUTPUT_DIR)
    
    outputs = {
        "output_stages.json": json.dumps({"stages": config.get("stages", [])}),
        "output_tech.txt": config.get("technology", "unknown"),
        "output_deploy.txt": config.get("deployment", "none"),
        "output_build_type.txt": config.get("build_type", "full"),
        "output_allowed_branches.txt": "\n".join(
            config.get("branching", {}).get("allowed_branches", [])
        )
    }
    
    for filename, content in outputs.items():
        try:
            temp_path = Path(OUTPUT_DIR) / f".{filename}.tmp"
            with open(temp_path, 'w') as f:
                f.write(content)
            temp_path.replace(Path(OUTPUT_DIR) / filename)
        except Exception as e:
            print(f"Failed to write {filename}: {str(e)}", file=sys.stderr)
            raise

def main():
    try:
        config = load_blueprint_file()
        write_outputs(config)
        print("Blueprint processed successfully")
    except Exception as e:
        print(f"Critical error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()