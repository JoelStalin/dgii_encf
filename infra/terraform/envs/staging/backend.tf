terraform {
  backend "s3" {
    bucket         = "getupnet-terraform"
    key            = "staging/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "getupnet-terraform-locks"
    encrypt        = true
  }
}
