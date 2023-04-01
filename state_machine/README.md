## Local Testing

### Setup
Summarized from the [docs](https://docs.aws.amazon.com/step-functions/latest/dg/sfn-local.html)

Pull the Docker image
`docker pull amazon/aws-stepfunctions-local`

Run the downloaded docker image
`docker run -p 8083:8083 amazon/aws-stepfunctions-local`

If you have an env file, specify it by
`docker run -p 8083:8083 --env-file aws-stepfunctions-local-credentials.txt amazon/aws-stepfunctions-local`

### Running
With a mocked config file, run docker and pass the file

```
docker run -p 8083:8083 
--mount type=bind,readonly,source={absolute path to mock config file},destination=/home/StepFunctionsLocal/MockConfigFile.json 
-e SFN_MOCK_CONFIG="/home/StepFunctionsLocal/MockConfigFile.json" amazon/aws-stepfunctions-local
```

Create the State Machine in AWS CLI

```
aws stepfunctions create-state-machine \
    --endpoint http://localhost:8083 \
    --cli-input-json {FileName for step functions definition} \
    --name "LambdaSQSIntegration" --role-arn "arn:aws:iam::123456789012:role/service-role/LambdaSQSIntegration"
```

Start an execution of the state machine. The #Happy path definition designates a test case
to run from the mocked config.

```
aws stepfunctions start-execution \
    --endpoint http://localhost:8083 \
    --name executionWithHappyPathMockedServices \
    --state-machine arn:aws:states:us-east-1:123456789012:stateMachine:LambdaSQSIntegration#HappyPath
```

Get the execution history to verify results

```
aws stepfunctions get-execution-history \
    --endpoint http://localhost:8083 \
    --execution-arn arn:aws:states:us-east-1:123456789012:execution:LambdaSQSIntegration:executionWithHappyPathMockedServices
```

## TODO
* Create a script that runs the above steps repeatably and asserts the results
* Create Mock Config