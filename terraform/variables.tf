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

variable "email_backend_type" {
  description = "The email backend type for the app to use"
  type        = string
}

variable "required_learning_time" {
  description = "The required learning time the user has to complete"
  type        = number
}

variable "send_verification_email" {
  description = "Whether to send a verification email the user on signup"
  type        = bool
}

variable "port" {
  description = "The port for the app to serve over"
  type        = number
}

variable "region" {
  description = "The region this instance is deployed to"
  type        = string
}

variable "debug" {
  description = "Whether the build is debug"
  type        = string
}

variable "min_autoscaling_capacity" {
  description = "The minimum number of tasks to run"
  type        = number
}

variable "max_autoscaling_capacity" {
  description = "The maximum number of tasks to run"
  type        = number
}
