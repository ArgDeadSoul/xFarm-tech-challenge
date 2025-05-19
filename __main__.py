import json
import pulumi
import pulumi_aws as aws

# S3 bucket
bucket = aws.s3.BucketV2('xfarm-tech-chal-upload-bucket', force_destroy=True) # Force destroy to help cleanup process only

# IAM
lambda_role = aws.iam.Role("lambda-exec-role",
    assume_role_policy=json.dumps({
        "Version": "2012-10-17",
        "Statement": [{
            "Action": "sts:AssumeRole",
            "Effect": "Allow",
            "Principal": {
                "Service": "lambda.amazonaws.com"
            }
        }]
    })
)

aws.iam.RolePolicyAttachment("lambda-basic-exec",
    role=lambda_role.name,
    policy_arn="arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
)

aws.iam.RolePolicy("lambda-s3-read", 
    role=lambda_role.name,
    policy=bucket.arn.apply(lambda arn: json.dumps({
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Action": ["s3:GetObject"],
            "Resource": f"{arn}/*"
        }]
    }))
)

# Lambda
lambda_func = aws.lambda_.Function("processCsv",
    role=lambda_role.arn,
    runtime="python3.9",
    handler="handler.handler",
    code=pulumi.AssetArchive({
        ".": pulumi.FileArchive("./lambda")
    }),
    timeout=10
)

# Allow S3 to invoke the Lambda
lambda_permission = aws.lambda_.Permission("s3-invoke-lambda",
    action="lambda:InvokeFunction",
    function=lambda_func.name,
    principal="s3.amazonaws.com",
    source_arn=bucket.arn
)

# S3 Event Notification
aws.s3.BucketNotification("bucketNotification",
    bucket=bucket.id,
    lambda_functions=[{
        "lambda_function_arn": lambda_func.arn,
        "events": ["s3:ObjectCreated:*"]
    }],
    opts=pulumi.ResourceOptions(depends_on=[lambda_permission])
)

# Export outputs
pulumi.export("bucket_name", bucket.bucket)
pulumi.export("lambda_name", lambda_func.name)