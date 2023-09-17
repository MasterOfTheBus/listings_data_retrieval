import { Construct } from "constructs";
import {  aws_lambda as lambda } from "aws-cdk-lib";
import { aws_ecr as ecr } from "aws-cdk-lib";
import { RemovalPolicy } from "aws-cdk-lib";

export interface DockerizedLambdaProps {
    lambdaId: string;
    repoName: string;
    environment: { [key: string]: string; };
  }

export class DockerizedLambda extends Construct {

  // public lambdaFn: lambda.Function;

  constructor(scope: Construct, id: string, props: DockerizedLambdaProps) {
    super(scope, id);

    // Define the ECR Repository for the docker image
    const repository = new ecr.Repository(this, "LambdaRepository", {
        autoDeleteImages: true,
        removalPolicy: RemovalPolicy.DESTROY,
        repositoryName: props.repoName
    });
    repository.addLifecycleRule({ maxImageCount: 2 });

    // // Define the Lambda
    // this.lambdaFn = new lambda.Function(this, props.lambdaId, {
    //     runtime: lambda.Runtime.PYTHON_3_9,
    //     handler: 'index.handler',
    //     environment: props.environment,
    //     code: lambda.Code.fromEcrImage(repository)
    // });
    
  }
}