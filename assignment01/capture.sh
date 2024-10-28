#!/bin/bash

# Start tcpdump on en0 for the external IP and the WireGuard internal IP
echo "Starting tcpdump on en0 for external and VPN internal IP..."
sudo tcpdump -i en0 host 89.58.29.203 or host 10.0.0.1 -w en0_traffic.pcap &
TCPDUMP_EN0_PID=$!                 # Store the PID of tcpdump on en0

# Start continuous ping to 10.0.0.1 in the background
ping 10.0.0.1 > /dev/null & # Log output to a file for reference
PING_PID=$!                 # Store the PID of the ping process to manage it

# Wait a moment to capture initial pings on en0
sleep 10

# Bring up the WireGuard interface
echo "Starting WireGuard interface..."
sudo wg-quick up wg0

# Start tcpdump on utun5 (the WireGuard interface) to capture decrypted traffic
echo "Starting tcpdump on utun5 to capture VPN traffic..."
sudo tcpdump -i utun5 -w utun5_traffic.pcap &
TCPDUMP_WG0_PID=$!                 # Store the PID of tcpdump on utun5

# Wait 10 seconds with ping running on WireGuard
sleep 10

# Stop the ping process to observe automatic handshakes
echo "Pausing the ping process for 30 seconds..."
kill $PING_PID
sleep 30

# Resume pinging for 10 seconds
echo "Resuming the ping process..."
ping 10.0.0.1 > /dev/null &
PING_PID=$!
sleep 10

# Stop tcpdump on utun5
echo "Stopping tcpdump on utun5..."
sudo kill $TCPDUMP_WG0_PID

# Bring down the WireGuard interface
echo "Stopping WireGuard interface..."
sudo wg-quick down wg0

# Stop the ping process again and wait an additional 10 seconds to observe final traffic
echo "Letting ping process run for 10 more seconds..."
sleep 10
kill $PING_PID

# Stop tcpdump on en0
echo "Stopping tcpdump on en0..."
sudo kill $TCPDUMP_EN0_PID

echo "Capture complete. PCAP files saved as en0_traffic.pcap and utun5_traffic.pcap"
