env = "prod"
ip_securelist = [
  "51.149.8.0/25",    # CO
  "51.149.10.6/32",   # CO
  "147.161.140.0/23", # No10
  "147.161.142.0/23", # No10
  "147.161.144.0/23", # No10
  "147.161.166.0/23", # No10
  "147.161.224.0/23", # No10
  "147.161.236.0/23", # No10
  "165.225.16.0/23",  # No10
  "165.225.80.0/22",  # No10
  "165.225.196.0/23", # No10
  "165.225.198.0/23", # No10
  "81.144.180.0/24",  # No10 desktop
]
record_prefix = ""
email_backend_type = "GOVUKNOTIFY"
required_learning_time = 420
port = 8055
region="eu-west-2"
debug = true
min_autoscaling_capacity = 20
max_autoscaling_capacity = 200
rds_instance_class = "db.r6g.2xlarge"
rds_instances = {
  one = {}
  two = {}
  three = {}
  four = {}
  five = {}
}
rds_autoscaling_min_capacity = 5
rds_autoscaling_max_capacity = 10