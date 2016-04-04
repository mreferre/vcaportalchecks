aws dynamodb create-table --table-name VcaPortalChecks \
		--attribute-definitions AttributeName=status,AttributeType=S \
	                            AttributeName=timestamp,AttributeType=N \
	    --key-schema AttributeName=status,KeyType=HASH \
	                 AttributeName=timestamp,KeyType=RANGE \
	    --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1
