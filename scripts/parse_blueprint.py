import yaml
import json
import sys
import os

def load_blueprint():
    if os.path.exists("blueprints/pipeline-blueprint.yaml"):
        with open("blueprints/pipeline-blueprint.yaml", "r") as f:
            return yaml.safe_load(f)
    elif os.path.exists("blueprints/pipeline-blueprint.json"):
        with open("blueprints/pipeline-blueprint.json", "r") as f:
            return json.load(f)
    else:
        print("No blueprint file found!")
        sys.exit(1)

def main():
    blueprint = load_blueprint()

    # Read basic fields
    tech_stack = blueprint.get("technology", "").lower()
    deploy_method = blueprint.get("deployment", "").lower()
    build_type = blueprint.get("build_type", "full").lower()

    # Branching rules
    branching = blueprint.get("branching", {})
    allowed_branches = branching.get("allowed_branches", [])

    # Stages
    stages = blueprint.get("stages", {})

    # Deployment target details
    deployment_target = blueprint.get("deployment_target", {})
    environment = deployment_target.get("environment", "")
    cloud_provider = deployment_target.get("cloud_provider", "")
    region = deployment_target.get("region", "")
    service = deployment_target.get("service", "")
    deployment_tool = deployment_target.get("deployment_method", "")

    # Save outputs for other jobs to read
    with open("output_tech.txt", "w") as f:
        f.write(f"{tech_stack}")

    with open("output_deploy.txt", "w") as f:
        f.write(f"{deploy_method}")

    with open("output_build_type.txt", "w") as f:
        f.write(f"{build_type}")

    with open("output_allowed_branches.txt", "w") as f:
        for branch in allowed_branches:
            f.write(f"{branch}\n")

    with open("output_stages.json", "w") as f:
        json.dump(stages, f)

    with open("output_deployment_target.json", "w") as f:
        json.dump(deployment_target, f)

    print(f"Tech Stack: {tech_stack}")
    print(f"Deployment: {deploy_method}")
    print(f"Build Type: {build_type}")
    print(f"Branching: {branching}")
    print(f"Stages: {stages}")
    print(f"Deployment Target: {deployment_target}")

if __name__ == "__main__":
    main()