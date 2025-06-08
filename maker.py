import os

project_root = os.getcwd()

structure = [
    "infra/terraform/modules/networking/main.tf",
    "infra/terraform/modules/networking/variables.tf",
    "infra/terraform/modules/storage/main.tf",
    "infra/terraform/modules/storage/variables.tf",
    "infra/terraform/modules/compute/ecr_ecs.tf",
    "infra/terraform/modules/compute/variables.tf",
    "infra/terraform/modules/ml/sagemaker_pipeline.tf",
    "infra/terraform/modules/ml/variables.tf",
    "infra/terraform/environments/dev/main.tf",
    "infra/terraform/environments/dev/terraform.tfvars",
    "infra/terraform/environments/prod/main.tf",
    "infra/terraform/environments/prod/terraform.tfvars",
    "infra/terraform/versions.tf",
    "api/main.py",
    "api/routes/question_answering.py",
    "scripts/preprocess.py",
    "scripts/train_pipeline.py",
    "ml_pipeline/rag_pipeline_definition.py",
    ".github/workflows/ci-cd.yml",
    "Dockerfile",
    "docker-compose.yml",
    "requirements.txt",
    "README.md",
    ".env.example"
]

def create_empty_structure(root, paths):
    for relative_path in paths:
        full_path = os.path.join(root, relative_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w') as f:
            pass  # create empty file

    print(f"✅ Empty structure created under: {root}")

if __name__ == "__main__":
    create_empty_structure(project_root, structure)
