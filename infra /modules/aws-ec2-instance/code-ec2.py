import pulumi
import pulumi_aws as aws

# Specify the desired AMI (Amazon Machine Image)
# This can vary based on region and this AMI specifies Amazon Linux 2
ami = 'ami-0c55b159cbfafe1f0'

# Specify the instance type (e.g., t2.micro, t3.medium)
instance_type = 't2.micro'

# Create a security group
secgroup = aws.ec2.SecurityGroup('secgroup',
    description='Enable SSH access',
    ingress=[
        # Security group rule that allows SSH inbound traffic 
        # from any IPv4 IP address.
        aws.ec2.SecurityGroupIngressArgs(
            protocol='tcp',
            from_port=22,
            to_port=22,
            cidr_blocks=["0.0.0.0/0"],
        ),
    ],
)

# Create an EC2 instance
instance = aws.ec2.Instance('instance',
    # The AMI to use for the instance
    ami=ami,
    # The type of instance to start
    instance_type=instance_type,
    # Associate the security group created earlier with the instance
    vpc_security_group_ids=[secgroup.id],
    # The user_data for cloud-init script, could be used to install
    # software or run maintenance tasks on instance startup
    user_data="""#!/bin/bash
    echo "Welcome to Mitti - Engineering!" > /home/ec2-user/mitti.txt""",
)

# Export the public IP of the instance
pulumi.export('public_ip', instance.public_ip)