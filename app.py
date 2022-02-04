#!/usr/bin/env python3

# import modules
import os
from aws_cdk import core


from gluecrawler_stack import GlueCrawlersStack

app = core.App()
gluecrawler_stack = GlueCrawlersStack(
    app,
    "glue-crawler-stack"
)

app.synth()
