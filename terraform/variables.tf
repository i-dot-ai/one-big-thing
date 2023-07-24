variable "env" {
  description = "The environment to deploy to."
}

variable "image_tag" {
  description = "The tag of the docker image to deploy."
}

variable "ip_securelist" {
  description = "The list of IPs to allow access to the load balancer."
}