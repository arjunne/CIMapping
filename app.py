#!/usr/bin/env python3

from aws_cdk import core

from ci_cdk.ci_cdk_stack import CiCdkStack


app = core.App()
CiCdkStack(app, "ci-cdk")

app.synth()
