#/bin/zsh

aws --profile se-prod \
	s3 ls s3://assets.stage.ngin.com
aws --profile se-prod \
        s3 mb s3://creative-testing-delete-me

echo "-------------------------------------------"

