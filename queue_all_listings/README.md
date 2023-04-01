Gets Listings stored in a s3 bucket and queues them up for retrieving data.

The mechanism is to store records in DyanmoDB following this schema. If new symbols need to be added, add to the end of the queue

| Symbol  | Next |
| ------------- | ------------- |
| Symbol to proces  | Next symbol to process  |


## Packaging for Deployment
run `make build` to package the dependencies into a `package.zip` archive

run `make clean` to delete the generated artifacts