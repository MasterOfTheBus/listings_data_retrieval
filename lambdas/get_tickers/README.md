Gets Tickers from polygon.io API
1. If ticker is not active && has object in the bucket ==> remove the object
2. If ticker is active ==> trigger the step function


## Packaging for Deployment
run `make build` to package the dependencies into a `package.zip` archive

run `make clean` to delete the generated artifacts