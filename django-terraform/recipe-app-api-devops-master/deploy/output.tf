# See in the console the output of the database address
# can be used to configure or debug the server

output "db_host" {
  value = aws_db_instance.main.address
}

output "bastion_host" {
  value = aws_instance.bastion.public_dns
}

output "api_endpoint" {
  value = aws_route53_record.app.fqdn
}