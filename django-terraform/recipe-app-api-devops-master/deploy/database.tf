resource "aws_db_subnet_group" "main" {
  name = "${local.prefix}-main"
  subnet_ids = [
    aws_subnet.private_a.id,
    aws_subnet.private_b.id,
  ]

  tags = merge(
    local.common_tags,
    map("Name", "${local.prefix}-main")
  )
}

# Security Group: Allow to control inbound and outbound
# access allowed to a resource
resource "aws_security_group" "rds" {
  description = "Allow access to the RDS database instance"
  name        = "${local.prefix}-rds-inbound-access"
  vpc_id      = aws_vpc.main.id

  # Allow inbound access to the RDS instance
  # on port 5432
  ingress {
    protocol  = "tcp"
    from_port = 5432
    to_port   = 5432

    security_groups = [
      aws_security_group.bastion.id,
      aws_security_group.ecs_service.id
    ]
  }

  tags = local.common_tags

}

resource "aws_db_instance" "main" {
  identifier = "${local.prefix}-db"
  name       = "recipe"
  # Disk space (GB)
  allocated_storage = 20
  # AWS entry level storage type
  # SSD general purpose 2
  storage_type         = "gp2"
  engine               = "postgres"
  engine_version       = "11"
  instance_class       = "db.t2.micro"
  db_subnet_group_name = aws_db_subnet_group.main.name
  password             = var.db_password
  username             = var.db_username
  # number of days a backup should be kept 
  backup_retention_period = 0
  # true if the database should be running in multiple
  # availability zones
  multi_az = false
  # mechanism to prevent data loss
  # if a database is deleted by error
  # true to disable creating snapshot on delete
  skip_final_snapshot    = true
  vpc_security_group_ids = [aws_security_group.rds.id]

  tags = merge(
    local.common_tags,
    map("Name", "${local.prefix}-bastion")
  )
}