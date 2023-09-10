import { Stack, StackProps } from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { aws_s3 as s3} from 'aws-cdk-lib';
import { aws_lambda as lambda} from 'aws-cdk-lib';
import { aws_events as events } from 'aws-cdk-lib';
import { aws_events_targets as target } from 'aws-cdk-lib';
import { RetrievalStateMachine } from './statemachine/retrieval-state-machine';

export class FrequentRetrievalStack extends Stack {

  public retrievalFn: lambda.Function;

  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    // Define the s3 bucket for storing data
    const bucket = new s3.Bucket(this, "frequent-retrieval-bucket", {
      blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
      encryption: s3.BucketEncryption.S3_MANAGED
    });

    // TODO: use bucket or docker image .fromAsset("")
    // Define the lambda that retrieves tickers
    const tickersFn = new lambda.Function(this, 'get-tickers-function', {
      runtime: lambda.Runtime.PYTHON_3_9,
      handler: 'index.handler',
      environment: {
        "bucket": bucket.bucketName
      },
      code: lambda.Code.fromInline("def handler(event, context):\n\tprint(\"hello world\")")
    })

    // Define the lambda that retrieves individual ticker data
    this.retrievalFn = new lambda.Function(this, 'get-daily-data-function', {
      runtime: lambda.Runtime.PYTHON_3_9,
      handler: 'index.handler',
      environment: {
        "bucket": bucket.bucketName
      },
      code: lambda.Code.fromInline("def handler(event, context):\n\tprint(\"hello world\")")
    });

    // Define the cloudwatch event trigger
    const event = new events.Rule(this, 'get-tickers-trigger', {
      enabled: false, // TODO: enable
      schedule: events.Schedule.cron({minute: "0", hour: "18", weekDay: "1-5"})
    })
    event.addTarget(new target.LambdaFunction(tickersFn))

    // Define the state machine
    const statemachine = new RetrievalStateMachine(this, "FrequentRetrievalWorkflow", {
      retrievalFn: this.retrievalFn,
      stateMachineName: "FrequentRetrievalWorkflow"
    });

    // Define permissions
    bucket.grantReadWrite(tickersFn);
    bucket.grantReadWrite(this.retrievalFn);
    statemachine.stepfunction.grantStartExecution(tickersFn);
  }
}
