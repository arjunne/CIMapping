from aws_cdk import (
    core,
    aws_iam as iam,
    aws_s3 as s3,
    aws_lambda as lambda_,
    aws_events_targets as targets,
    aws_logs as logs
    )
import os


class CiCdkStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here

        #Get bucket

        environmentvar = dict()
        environmentvar['host']='bolt://ec2-3-80-161-226.compute-1.amazonaws.com:7687'
        environmentvar['password']='1Ncorrect'

        lambda_role = iam.Role(self,
            'ci-role',
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies= [
                iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess")
            ]
        )

        layer_requirements = lambda_.LayerVersion(self,'cdk-layer-requirements',    
                            code=lambda_.Code.from_asset("./layer"),
                            compatible_runtimes=[lambda_.Runtime.PYTHON_3_6,
                                                lambda_.Runtime.PYTHON_3_7,
                                                lambda_.Runtime.PYTHON_3_8],
                            description="Layer for python packages",
                            layer_version_name="layer"
                            )

        ci_lambda = lambda_.Function(self, 'ci',
                    code=lambda_.InlineCode(code=' ').from_asset("./src/"),
                    function_name='CIMapping',
                    description="Lambda that process files and creates nodes",
                    handler="ci.lambda_handler",
                    role=lambda_role,
                    environment=environmentvar,
                    memory_size=128,
                    timeout=core.Duration.seconds(60),
                    runtime=lambda_.Runtime.PYTHON_3_8,
                    retry_attempts=1,
                    layers=[layer_requirements],
                    log_retention=logs.RetentionDays.ONE_WEEK
                    )
        