import os
import boto3
from ml_pipeline.rag_pipeline_definition import get_pipeline_definition


def start_sagemaker_pipeline():
    pipeline_name = os.getenv("SM_PIPELINE_NAME")
    sm = boto3.client("sagemaker", region_name=os.getenv("AWS_DEFAULT_REGION"))

    definition = get_pipeline_definition()

    try:
        sm.create_pipeline(
            PipelineName=pipeline_name,
            RoleArn=os.getenv("SM_PIPELINE_ROLE_ARN"),
            PipelineDefinition=definition
        )
        print(f"Created pipeline {pipeline_name}")
    except sm.exceptions.PipelineAlreadyExistsException:
        print(f"Pipeline {pipeline_name} exists, updating definition.")
        sm.update_pipeline(
            PipelineName=pipeline_name,
            PipelineDefinition=definition
        )

    execution = sm.start_pipeline_execution(PipelineName=pipeline_name)
    print(f"Started execution: {execution['PipelineExecutionArn']}")


if __name__ == "__main__":
    start_sagemaker_pipeline()