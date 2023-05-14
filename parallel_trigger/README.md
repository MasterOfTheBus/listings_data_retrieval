Gets Listings stored in a s3 bucket and triggers lambdas to retrieve data.

The mechanism is to send events to SNS topic. There is a lambda listening to the topic.

Return the payload for the next iteration to pull from
```
{
    "listings": []
}
```


## Packaging for Deployment
run `make build` to package the dependencies into a `package.zip` archive

run `make clean` to delete the generated artifacts