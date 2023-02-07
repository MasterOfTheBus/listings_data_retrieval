Gets Listings stored in a s3 bucket. Generate rules that trigger on a schedule for each symbol. Name the Rule after the Symbol so that the Lambda can parse this info out of the ARN. Set the Target for the rules as the get_listings_info Lambda function

## Packaging for Deployment
run `make build` to package the dependencies into a `package.zip` archive

run `make clean` to delete the generated artifacts

## Alternatives Considered
1. Queue messages in SQS for processing later. Drawback is that message retention is 14 days and the estimate is that population would take 100+ days with free AlphaVantage API Key
2. AWS MSK. The drawback is that MSK has no free tier

The queuing options are superior because they are more flexible. A new symbol added will just need to be placed on the queue. The Rules requires adding a new symbol.