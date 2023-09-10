import { Stack, StackProps } from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { aws_s3 as s3} from 'aws-cdk-lib';
import { aws_lambda as lambda} from 'aws-cdk-lib';
import { aws_events as events } from 'aws-cdk-lib';
import { aws_events_targets as target } from 'aws-cdk-lib';
import { aws_secretsmanager as secretsmanager } from 'aws-cdk-lib';
import { RetrievalStateMachine } from './statemachine/retrieval-state-machine';
import { DockerizedLambda } from './lambda/dockerized-lambda';

export class FrequentRetrievalStack extends Stack {

  public retrievalFn: lambda.Function;

  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    // Define the s3 bucket for storing data
    const bucket = new s3.Bucket(this, "frequent-retrieval-bucket", {
      blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
      encryption: s3.BucketEncryption.S3_MANAGED
    });

    // Define the state machine
    const statemachine = new RetrievalStateMachine(this, "FrequentRetrievalWorkflow", {
      retrievalFn: this.retrievalFn,
      stateMachineName: "FrequentRetrievalWorkflow"
    });

    // Define the secrets manager secret
    const secret = new secretsmanager.Secret(this, "keysSecrets", {
      secretName: "ApiKeys"
    });

    // Define the lambda that retrieves tickers
    const tickersLambda = new DockerizedLambda(this, 'get-tickers-function', {
      lambdaId: 'GetTickersLambda',
      repoName: 'GetTickersLambdaRepo',
      environment: {
        "stateMachineArn": statemachine.stepfunction.stateMachineArn,
        "secretName": secret.secretName
      }
    });

    // Define the lambda that retrieves individual ticker data
    const retrievalLambda = new DockerizedLambda(this, 'get-daily-data-function', {
      lambdaId: 'GetDailyDataLambda',
      repoName: 'GetDailyDataLambdaRepo',
      environment: {
        "bucket": bucket.bucketName
      }
    });
    this.retrievalFn = retrievalLambda.lambdaFn;

    // Define the cloudwatch event trigger
    const event = new events.Rule(this, 'get-tickers-trigger', {
      enabled: false, // TODO: enable
      schedule: events.Schedule.cron({minute: "0", hour: "18", weekDay: "1-5"})
    })
    event.addTarget(new target.LambdaFunction(tickersLambda.lambdaFn))

    // Define permissions
    bucket.grantReadWrite(tickersLambda.lambdaFn);
    bucket.grantReadWrite(this.retrievalFn);
    statemachine.stepfunction.grantStartExecution(tickersLambda.lambdaFn);
    secret.grantRead(tickersLambda.lambdaFn);
    secret.grantRead(this.retrievalFn);
  }
}
