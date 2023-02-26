# ---DEPRECATED---

Compares against the number of requests made in a day and returns whether rate has been reached.

AlphaVantage has 500 requests in a day and 5 requests in a minute limit.
get_listings_info lambda makes 5 requests at a time so check requests in a day

## Packaging for Deployment
run `make build` to package the dependencies into a `package.zip` archive

run `make clean` to delete the generated artifacts

run `make test` to run unit tests