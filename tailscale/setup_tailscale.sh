#!/bin/bash

# Check if Tailscale is already running
if systemctl is-active --quiet tailscaled; then
  echo "Tailscale is already running. Skipping setup."
  exit 0
fi

echo "Installing and configuring Tailscale..."

sudo apt update
sudo apt install -y tailscale
sudo systemctl enable tailscaled
sudo systemctl start tailscaled

echo "Run 'sudo tailscale up --ssh' manually to authenticate."
