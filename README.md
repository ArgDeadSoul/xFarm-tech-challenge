# S3 to Lambda

## Architecture

This project sets up:
- An S3 bucket to receive uploads
- A Lambda function (Python) triggered by S3 `ObjectCreated` events
- IAM permissions for secure access
- All defined in Pulumi (Python)

![Architecture](./diagram.png)

## Deployment Instructions

### 0. Prerequisites

- Python 3.8+
- Pulumi CLI
- AWS CLI (`aws configure` setup)

### 1. Clone the Repository

```bash
git clone https://github.com/ArgDeadSoul/xFarm-tech-challenge.git
cd xFarm-tech-challenge
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure AWS Credentials
For Linux/macOS:
```
export AWS_ACCESS_KEY_ID=your_access_key_id
export AWS_SECRET_ACCESS_KEY=your_secret_access_key
export AWS_REGION=us-east-1
```

For Windows:
```
$Env:AWS_ACCESS_KEY_ID="your_access_key_id"
$Env:AWS_SECRET_ACCESS_KEY="your_secret_access_key"
$Env:AWS_REGION="us-east-1"
```

### 4. Deploy infraestructure
```
pulumi stack init dev
pulumi up
```

### 5. CI/CD [Optional]
All pushes to the main branch trigger a pipeline to deploy using pulumi. The default stack is `dev` for simplicity. Pipelines in `.github/workflows`

### 6. Destroy infraestructure
If triggerd manually use:
```
pulumi destroy
```
If the CI/CD pipeline was used you can use the workflow `.github/workflows/destroy.yml`.

To delete the stack use 
```
pulumi stack rm dev
```


## Deployment Process

- As I never used pulumi i had to do a little research on the tool. 
- Installed pulumi and made necessary accounts for the demo. 
- Created a pulumi project and used AI to help me format the project fast and effectivly.
- Created a simple python script for the lambda
- In AWS:
   - Created IAM role for pulumi access
   - Created an access token for said user (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
- In pulumi:
   - Created an access token (PULUMI_ACCESS_TOKEN)
- This tokens will be used for the pulumi and CI/CD. Stored them as repository secrets
- Deployed infraestructure using pulumi with no much problems
- Tested application
- Created a simple Github Actions pipeline to deploy infraestructure using pulumi
- Created a simple Github Actions pipeline to destroy infraestructure using pulumi
- Tested pipelines and application
- Documented process in README
