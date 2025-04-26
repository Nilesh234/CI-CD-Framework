import yaml
import json
import sys
import os
from typing import Dict, Any

def load_blueprint() -> Dict[str, Any]:
    """Load blueprint file from blueprints directory with fallback to empty dict."""
    try:
        if os.path.exists("blueprints/pipeline-blueprint.yaml"):
            with open("blueprints/pipeline-blueprint.yaml", "r") as f:
                return yaml.safe_load(f) or {}
        elif os.path.exists("blueprints/pipeline-blueprint.json"):
            with open("blueprints/pipeline-blueprint.json", "r") as f:
                return json.load(f) or {}
    except Exception as e:
        print(f"Error loading blueprint: {str(e)}", file=sys.stderr)
    
    print("No valid blueprint file found, using empty configuration")
    return {
        "technology": "",
        "deployment": "",
        "build_type": "full",
        "branching": {"allowed_branches": []},
        "stages": [],
        "deployment_target": {}
    }

def create_output_directory():
    """Ensure output directory exists."""
    os.makedirs("outputs", exist_ok=True)

def write_outputs(blueprint: Dict[str, Any]):
    """Write all output files with proper error handling."""
    tech_stack = blueprint.get("technology", "").lower()
    deploy_method = blueprint.get("deployment", "").lower()
    build_type = blueprint.get("build_type", "full").lower()
    allowed_branches = blueprint.get("branching", {}).get("allowed_branches", [])
    stages = blueprint.get("stages", [])
    deployment_target = blueprint.get("deployment_target", {})

    try:
        with open("output_tech.txt", "w") as f:
            f.write(tech_stack)

        with open("output_deploy.txt", "w") as f:
            f.write(deploy_method)

        with open("output_build_type.txt", "w") as f:
            f.write(build_type)

        with open("output_allowed_branches.txt", "w") as f:
            f.write("\n".join(allowed_branches))

        with open("output_stages.json", "w") as f:
            json.dump({"stages": stages}, f, indent=2)

        with open("output_deployment_target.json", "w") as f:
            json.dump(deployment_target, f, indent=2)

    except IOError as e:
        print(f"Error writing output files: {str(e)}", file=sys.stderr)
        sys.exit(1)

def main():
    create_output_directory()
    blueprint = load_blueprint()
    write_outputs(blueprint)

    # Print summary for logs
    print("\nBlueprint Processing Summary:")
    print(f"Technology: {blueprint.get('technology', 'UNSPECIFIED')}")
    print(f"Deployment: {blueprint.get('deployment', 'UNSPECIFIED')}")
    print(f"Build Type: {blueprint.get('build_type', 'full')}")
    print(f"Stages: {len(blueprint.get('stages', []))} stages configured")
    print(f"Deployment Target: {blueprint.get('deployment_target', {}).get('environment', 'UNSPECIFIED')}")

if __name__ == "__main__":
    main()