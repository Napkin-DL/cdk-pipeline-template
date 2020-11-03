#!/usr/bin/env python3

import configparser
from aws_cdk import core

from pipeline_stack.cdk_pipeline_stack import CdkPipelineStack as pipeline

config = configparser.ConfigParser()
config.read('app.cfg')
app = core.App()

pipeline(app, config['app']['stack_name'], 
    env={
        'account': config['app']['account'],
        'region': config['app']['region']
    },
    pipeline_config={
        'pipeline_name': config['pipeline']['pipeline_name'],
        'github_oauth_token': config['pipeline']['github_oauth_token'],
        'github_owner': config['pipeline']['github_owner'],
        'github_repo': config['pipeline']['github_repo'],
        'github_branch': config['pipeline']['github_branch'],
        'stage_account': config['app']['account'],
        'stage_region': config['app']['region']
    })

app.synth()
