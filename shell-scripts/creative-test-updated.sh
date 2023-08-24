#/bin/zsh
echo "Querying for Assumed role..."
echo "-------------------------------------------"
aws sts get-caller-identity --profile se-prod
echo ""
echo "Running creative permissiosn test..."
echo "-------------------------------------------"
echo "Testing access on provisioned resource:\n"
aws --profile se-prod \
	s3 ls s3://assets.ngin.com/site_files/####/
aws --profile se-prod \
        s3 cp s3://assets.ngin.com/site_files/####/package.json downloaded-package.json
ls -al | grep downloaded-package.json
rm downloaded-package.json
echo "-------------------------------------------"
echo "Testing access on unprovisioned resource:\n"
zsh unprovissioned-updated.sh

