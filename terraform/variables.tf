variable "env" {
  description = "The environment to deploy to."
  type        = string
}

variable "image_tag" {
  description = "The tag of the docker image to deploy."
  type        = string
}

variable "ip_securelist" {
  description = "The list of IPs to allow access to the load balancer."
  type        = list(string)
}

variable "record_prefix" {
  description = "The prefix to use for the route53 records"
  type        = string
}
