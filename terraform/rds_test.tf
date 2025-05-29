module "rds_example_complete-postgres" {
  source  = "terraform-aws-modules/rds/aws//examples/complete-postgres"
  version = "6.5.4"
}
