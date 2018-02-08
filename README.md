# cfn-lbr-library
## CloudFormation custom resources

## Quickstart
Clone and install `cfn-lbr-registry`, the tool used to package and deploy the registry: https://github.com/benkehoe/cfn-lbr-registry

Then run:
```
$ make build
$ make deploy
```
You'll have a stack name LBR-Registry, with the Lambda ARNs exported to use in your other stacks.
