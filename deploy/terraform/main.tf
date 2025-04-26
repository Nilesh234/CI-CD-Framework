provider "aws" {
  region = var.region
}

resource "aws_s3_bucket" "sample_bucket" {
  bucket = "${var.project_name}-bucket"
  acl    = "private"
}
