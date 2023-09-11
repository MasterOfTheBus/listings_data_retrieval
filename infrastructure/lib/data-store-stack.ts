import { Stack, StackProps } from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { aws_dynamodb as ddb } from 'aws-cdk-lib';
import { IGrantable } from 'aws-cdk-lib/aws-iam';

export interface DataStoreStackProps extends StackProps {
  lockTableGrantees: [IGrantable];
  countTableGrantees: [IGrantable];
}

export class DataStoreStack extends Stack {
  constructor(scope: Construct, id: string, props: DataStoreStackProps) {
    super(scope, id, props);

    // Define the ddb table for the distributed locking
    const lockTable = new ddb.TableV2(this, "DistributedLockTable", {
      tableName: "DistributedLockTable",
      partitionKey: { name: 'lock', type: ddb.AttributeType.STRING } // TODO: work with distributed lock client
    });

    // Define the ddb table for count tracking
    const countTable = new ddb.TableV2(this, "CountTable", {
      tableName: "CountTable",
      partitionKey: { name: 'type', type: ddb.AttributeType.STRING }
    });

    // Grant permissions
    // props.lockTableGrantees.forEach(grantee => {
    //   lockTable.grantReadWriteData(grantee);
    // })
    
    // props.countTableGrantees.forEach(grantee => {
    //   countTable.grantReadWriteData(grantee);
    // })
  }
}
