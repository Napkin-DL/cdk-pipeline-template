from aws_cdk import core
from aws_cdk import aws_codepipeline as codepipeline
from aws_cdk import aws_codepipeline_actions as cpactions
from aws_cdk import pipelines

from .app_stage import AppStage

class CdkPipelineStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, pipeline_config: dict, **kwargs):
        super().__init__(scope, id, **kwargs)

        source_artifact = codepipeline.Artifact()
        cloud_assembly_artifact = codepipeline.Artifact()

        pipeline = pipelines.CdkPipeline(self, 'CdkPipeline', 
            cloud_assembly_artifact=cloud_assembly_artifact,
            pipeline_name=pipeline_config['pipeline_name'],            
            source_action=cpactions.GitHubSourceAction(
                # https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-codepipeline-actions.GitHubSourceActionProps.html
                action_name='GithubAction',
                output=source_artifact,
                oauth_token=core.SecretValue.secrets_manager(pipeline_config['github_oauth_token']),
                # https://docs.aws.amazon.com/ko_kr/codepipeline/latest/userguide/welcome.html
                owner=pipeline_config['github_owner'],
                repo=pipeline_config['github_repo'],
                branch=pipeline_config['github_branch'],
                trigger=cpactions.GitHubTrigger.POLL),
            synth_action=pipelines.SimpleSynthAction(
                source_artifact=source_artifact,
                cloud_assembly_artifact=cloud_assembly_artifact,
                install_command='npm install -g aws-cdk && pip install -r requirements.txt',
                synth_command='cdk synth'
            )
        )

        pipeline.add_application_stage(AppStage(self, 'Prod', env={
            'account': pipeline_config['stage_account'],
            'region': pipeline_config['stage_region']
        }))