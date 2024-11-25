# Task 1: Reading and Reasoning
#### Why is it difficult to develop and deploy/adopt new transport protocols?
- difficult to develop and deploy new transport protocols due to widespread deployment of middleboxes (firewalls, NATs, proxies, etc.)
- middleboxes often inspect and modify packets beyond the IP header
- middleboxes are often not updated frequently, leading to ossification of the network
- new protocol must account for unpredictable and varying middlbebox behavior, which can strip, modify or block new protocol features

#### How does QUIC overcome the ossification issue? Why does it use UDP? What features and benefits does it provider over TCP?
- QUIC encrypts the transport headers, making it hard for middleboxes to inspect and modify packets
- uses UDP as underlying protocol as most middleboxes allow UDP traffic to pass through 
- operates in user space, allowing for rapid deployment and updates
- features and benefits over TCP:
    - Reduced Handshake Latency: Combines cryptographic and transport handshakes, enabling 0-RTT connections on repeat handshakes.
    - Stream Multiplexing: Eliminates head-of-line blocking by multiplexing multiple streams in a single connection.
    - Connection Migration: Supports connection continuity across IP address changes using connection IDs.
    - Improved Loss Recovery: Uses unique packet numbers and explicit acknowledgments for more accurate and efficient loss detection.
    - Built-in Security: QUIC inherently supports encryption, reducing risks of tampering and eavesdropping.
    - Enhanced Performance: Reduces latency and rebuffer rates, especially for applications like video streaming and web browsing​
