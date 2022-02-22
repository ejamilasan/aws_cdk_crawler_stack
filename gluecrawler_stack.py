
from aws_cdk import (
    core,
    aws_iam as iam,
    aws_glue as glue
)
# env variables
SOURCE_BUCKET_NAME = "sample_bucket/object"     # example: bucket_name/object
SCHEDULE_EXPRESSION = "cron(15 19 * * * *)"     # format: cron(Minutes Hours Day-of-month Month Day-of-week Year)

class GlueCrawlersStack(core.Stack):
    def __init__(
        self, scope: core.Construct, id: str, s3_bucket: str, schedule_exp: str, crawler_name: str, crawler_role_name: str, s3databasename: str, **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)
       
        s3_access_statement = iam.PolicyStatement(
            actions=["s3:*"], 
            resources=[
                "arn:aws:s3:::" + s3_bucket, 
                "{}/*".format("arn:aws:s3:::" + s3_bucket)
            ]
        )
        
        # create iam role for s3 crawler
        glue_role = iam.Role(
            self, "glue-role",
            role_name= crawler_role_name,
            assumed_by=iam.ServicePrincipal('glue.amazonaws.com'),
            inline_policies = [
                iam.PolicyDocument(
                    statements=[s3_access_statement]
                )
            ],
            managed_policies=[
                iam.ManagedPolicy.from_managed_policy_arn(
                    self, 'managed-policy',
                    managed_policy_arn='arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole'
                )
            ]
        )
        
        # create s3 crawler
        s3_crawler = glue.CfnCrawler(
            self, "test-crawler",
            role = glue_role.role_arn,
            name = crawler_name,
            database_name = s3databasename,
            schedule = glue.CfnCrawler.ScheduleProperty(
                schedule_expression = schedule_exp
            ),
            targets = {
                "s3Targets": [
                    {
                        "path": "s3://" + s3_bucket
                        
                    }
                ]
            }
        )
