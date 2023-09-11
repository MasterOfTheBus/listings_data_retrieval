import { Duration } from "aws-cdk-lib";
import { Construct } from "constructs";
import { aws_stepfunctions as stepfunction } from "aws-cdk-lib";
import { aws_stepfunctions_tasks as tasks } from "aws-cdk-lib";
import { aws_lambda as lambda } from "aws-cdk-lib";

export interface RetrievalStateMachineProps {
    retrievalFn: lambda.Function;
    stateMachineName?: string;
  }

export class RetrievalStateMachine extends Construct {

  public stepfunction: stepfunction.StateMachine;

  constructor(scope: Construct, id: string, props: RetrievalStateMachineProps) {
    super(scope, id);

    // Define the states
    const lambdaState = new tasks.LambdaInvoke(this, "Invoke Retrieval Lambda", {
      lambdaFunction: props.retrievalFn,
      payload: stepfunction.TaskInput.fromJsonPathAt("$.ticker")
    });
    const waitMinute = new stepfunction.Wait(this, "WaitMinute", {
      time: stepfunction.WaitTime.duration(Duration.minutes(1))
    });
    const waitNextDay = new stepfunction.Wait(this, "WaitNextDay", {
      time: stepfunction.WaitTime.timestampPath("$.waitUntil")
    })
    const succeed = new stepfunction.Succeed(this, "Finished");
    
    // Define the choice state
    const choice = new stepfunction.Choice(this, "Choice");
    const waitMinuteCondition = stepfunction.Condition.stringEquals("$.result", "waitMinute");
    const waitDayCondition = stepfunction.Condition.stringEquals("$.result", "waitDay");
    const choiceDefinition = choice
      .when(waitMinuteCondition, waitMinute)
      .when(waitDayCondition, waitNextDay)
      .otherwise(succeed);

    // Define the graph of the states
    lambdaState.next(choiceDefinition);

    // Define the state machine
    this.stepfunction = new stepfunction.StateMachine(this, "RetrievalStateMachine", {
      definitionBody: stepfunction.DefinitionBody.fromChainable(lambdaState),
      stateMachineName: props.stateMachineName
    });
  }
}