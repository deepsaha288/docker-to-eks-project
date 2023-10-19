import boto3
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize a Boto3 EKS client
eks_client = boto3.client('eks', region_name='us-east-1')

# Read cluster configuration from environment variables
cluster_name = os.environ.get('EKS_CLUSTER_NAME')
role_arn = os.environ.get('EKS_ROLE_ARN')
subnet_ids = os.environ.get('EKS_SUBNET_IDS').split(',')
k8s_version = os.environ.get('EKS_K8S_VERSION')

if not all([cluster_name, role_arn, subnet_ids, k8s_version]):
    print("Please set the required environment variables.")
    exit(1)

# Create the EKS cluster
response = eks_client.create_cluster(
    name=cluster_name,
    roleArn=role_arn,
    resourcesVpcConfig={
        'subnetIds': subnet_ids,
    },
    version=k8s_version,
)

# Wait for the cluster to be created (this might take a few minutes)
eks_client.get_waiter('cluster_created').wait(name=cluster_name)

# Check the cluster status
cluster_info = eks_client.describe_cluster(name=cluster_name)
print(f"Cluster status: {cluster_info['cluster']['status']}")
