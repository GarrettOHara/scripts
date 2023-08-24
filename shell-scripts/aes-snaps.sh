#/bin/zsh

aws --profile aes-prod \
    --region us-east-1 \
    rds describe-db-snapshots