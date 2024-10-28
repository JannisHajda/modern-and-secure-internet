# Setting Up a WireGuard VPN Connection and Packet Capture Analysis

![WireGuard Logo](https://www.wireguard.com/img/wireguard.svg)

## Introduction

WireGuard is an increasingly popular VPN protocol known for its speed,
simplicity, and security. Unlike traditional protocols like OpenVPN, which can
be complex and resource-heavy, WireGuard has a streamlined codebase of about
4.000 lines, making it easier to audit for vulnerabilities. It often delivers
significantly faster performance than OpenVPN while employing advanced
cryptography for robust security. It uses modern cryptographic algorithms such
as ChaCha20 for encryption, Curve25519 for key exchange, and Poly1305 for
message authentication, which collectively enhance data security and
performance.

Additionally, WireGuard employs a cryptokey routing mechanism that associates
public keys with specific IP addresses, streamlining the authentication process
and making it easier to manage connections. This design not only enhances
security but also minimizes the attack surface, making WireGuard a robust choice
for users seeking privacy and efficiency in their online activities.

Furthermore, WireGuard extensive formal verification to ensure the security of
its protocol, cryptography, and implementation. Key efforts include symbolic
verification using the Tamarin model, which confirms properties such as
correctness, strong key agreement, and resistance to various attacks.
Additionally, computational proofs have been conducted in both the eCK and ACCE
models, demonstrating properties like forward secrecy and mutual authentication.
The protocol also incorporates verified implementations of Curve25519 through
projects like HACL* and Fiat-Crypto, further enhancing its security framework.

## Assignment Overview

In this assignment, you will set up a WireGuard VPN connection to a test server
server and analyzing the network packets exchanged during the connection.
You should be using Jupyter Notebook to document the setup process, capture
packets, and visualize the data for analysis.

*See enclosed sample Jupyter Notebook*

### Objectives

-   Understand the configuration of WireGuard VPN.
-   Capture and analyze network packets using Python libraries.
-   Visualize packet data to identify key attributes and behaviors.
-   Document the entire process in a Jupyter Notebook.

## Assignment Structure

1. **WireGuard Setup (30%) **
   - **Objective:** Configure a WireGuard VPN connection to your server or a
     test server (available WireGuard test servers).
   - **Deliverables:**
     - Jupyter Notebook section documenting:
       - Installation steps for WireGuard on both server and client.
       - Key generation and configuration files.
       - Commands to start the WireGuard service.
     - Example code snippets for automating the setup process using Python.

2. **Packet Capture (30%) **
   - **Objective:** Capture network packets during the WireGuard connection
     establishment.
   - **Deliverables:**
     - Use Scapy or tcpdump to capture packets.
     - Include commands for capturing packets in your Jupyter Notebook.
     - Save captured packets in PCAP format for analysis.

3. **Data Analysis and Visualization (40%) **
   - **Objective:** Analyze and visualize the captured packet data.
   - **Deliverables:**
     - Use Python libraries (e.g., Pandas, Matplotlib) to read and analyze packet data.
     - Create visualizations that highlight key aspects of the packet flow
       (e.g., source/destination IPs, packet types).
     - Document findings in the Jupyter Notebook with appropriate markdown explanations.

## Submission Guidelines

- **Format:** All code and documentation should be contained within a **single**
  Jupyter Notebook file.
- **Due Date:** 01.11.2024
- **Submission Method:** Submit via Moodle

## Resources

- [Jupyter Notebook: An open-source web application that allows you to create and share documents containing live code, equations, visualizations, and narrative text](https://jupyter.org/)
- [Matplotlib: A comprehensive library for creating static, animated, and interactive visualizations in Python](https://matplotlib.org/stable/contents.html)
- [Pandas: A fast, powerful, flexible, and easy-to-use open-source data analysis and manipulation library for Python](https://pandas.pydata.org/pandas-docs/stable/)
- [Scapy: A powerful Python library for packet manipulation and analysis](https://scapy.readthedocs.io/en/latest/)
- [WireGuard Formal Verification](https://www.wireguard.com/formal-verification/)
- [WireGuard: A fast and modern VPN that uses state-of-the-art cryptography](https://www.wireguard.com/)
- [Wireshark: A widely-used network protocol analyzer that provides a graphical interface for analyzing network traffic](https://www.wireshark.org/)
- [python-wireguard: A Python wrapper for controlling WireGuard connections](https://pypi.org/project/python-wireguard/)
- [tcpdump: A command-line packet analyzer tool for capturing network traffic](https://www.tcpdump.org/)
- [wireguard-py: A Cython library for managing WireGuard configurations in Python](https://pypi.org/project/wireguard-py/)
