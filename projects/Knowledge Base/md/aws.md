# Install and configure AWS CLI
- After installing AWS CLI, run `aws configure`. Here, enter the IAM user acces key and secret keys.

- use `aws configure list` to list default IAM user

- store the IAM user in `~/.aws/credentials` file as:

[default]
aws_access_key_id=<access key>
aws_secret_access_key=<secret key>
