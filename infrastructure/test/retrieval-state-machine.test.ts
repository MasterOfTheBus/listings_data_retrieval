import * as cdk from 'aws-cdk-lib';
import { Template } from 'aws-cdk-lib/assertions';

import { FrequentRetrievalStack } from "../lib/frequent-retrieval-stack";

// TODO: Probably could be a better test defined
test('State Machine Graph', () => {
    const app = new cdk.App();
    const retrievalStack = new FrequentRetrievalStack(app, "TestStack");
    const template = Template.fromStack(retrievalStack);

    const resources = template.findResources("AWS::StepFunctions::StateMachine");
    expect(resources['RetrievalStateMachine']).not.toBeNull();
});