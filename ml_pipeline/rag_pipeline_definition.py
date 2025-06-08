import os
from sagemaker.workflow.pipeline import Pipeline
from sagemaker.workflow.steps import ProcessingStep, TrainingStep
from sagemaker.processing import ScriptProcessor
from sagemaker.estimator import Estimator
from sagemaker.model_registry import ModelPackageGroup
from sagemaker.workflow.model_step import RegisterModel


def get_pipeline_definition():
    region = os.getenv("AWS_DEFAULT_REGION")
    role = os.getenv("SM_PIPELINE_ROLE_ARN")
    bucket = os.getenv("S3_ARTIFACT_BUCKET")

    # Processing step
    processor = ScriptProcessor(
        image_uri=os.getenv("PROCESSOR_IMAGE_URI"),
        command=["python3"],
        role=role,
        instance_count=1,
        instance_type="ml.m5.xlarge"
    )
    process_step = ProcessingStep(
        name="PreprocessDocuments",
        processor=processor,
        inputs=[...],
        outputs=[...],
        code="scripts/preprocess.py"
    )

    # Training step
    estimator = Estimator(
        image_uri=os.getenv("TRAINING_IMAGE_URI"),
        role=role,
        instance_count=1,
        instance_type="ml.c5.xlarge",
        output_path=f"s3://{bucket}/models/"
    )
    train_step = TrainingStep(
        name="TrainRAGModel",
        estimator=estimator,
        inputs={
            "training_data": process_step.properties.Outputs[0].S3Output.S3Uri
        }
    )

    # Model registration
    model_group = ModelPackageGroup(
        name=os.getenv("SM_MODEL_PACKAGE_GROUP"),
        role_arn=role
    )
    register_step = RegisterModel(
        name="RegisterRAGModel",
        estimator=estimator,
        model_package_group_name=os.getenv("SM_MODEL_PACKAGE_GROUP"),
        content_types=["application/json"],
        response_types=["application/json"],
        inference_instances=["ml.m5.large"],
        transform_instances=["ml.m5.large"],
        model_data=train_step.properties.ModelArtifacts.S3ModelArtifacts
    )

    pipeline = Pipeline(
        name=os.getenv("SM_PIPELINE_NAME"),
        steps=[process_step, train_step, register_step],
        sagemaker_session=None  # autodiscover via boto3
    )
    return pipeline.definition()