docker :
	docker run -p 11667:8083 \
	--mount type=bind,readonly,source=$(PWD)/data_retrieval_mock_config.json,\
	destination=/home/StepFunctionsLocal/MockConfigFile.json \
	-e SFN_MOCK_CONFIG="/home/StepFunctionsLocal/MockConfigFile.json" \
	-d amazon/aws-stepfunctions-local

create-sm : docker
	aws stepfunctions create-state-machine --endpoint http://localhost:11667 \
	--definition file://data_retrieval.json \
	--name "DataRetrieval" --role-arn "arn:aws:iam::123456789012:role/service-role/DataRetrieval"

exec-happypath : create-sm
	aws stepfunctions start-execution --endpoint http://localhost:11667 \
	--name mockedHappyPath \
	--state-machine arn:aws:states:us-east-1:123456789012:stateMachine:DataRetrieval#HappyPath \
	--input '{"ignore_queue_all": false}'

get-results:
	aws stepfunctions get-execution-history --endpoint http://localhost:11667 \
	--execution-arn arn:aws:states:us-east-1:123456789012:execution:DataRetrieval:mockedHappyPath > execution_results.json

test :
	python -m unittest
