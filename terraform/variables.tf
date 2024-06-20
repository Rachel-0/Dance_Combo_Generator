variable "app-key" {
  description = "Name of the SSH key pair"
  type        = string
}

variable "~/.ssh/app-key.pub" {
  description = "Path to the SSH public key file"
  type        = string
}
