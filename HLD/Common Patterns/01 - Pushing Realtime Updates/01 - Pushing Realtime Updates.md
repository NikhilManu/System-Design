# Pushing Realtime Updates

## Problem

Consider Google Docs. When one user types a character, all other users viewing the document need to see change suddenly. Here we cant have the users polling the server for updates every few ms without crushing the infrastructure

## Solution

When system requires real-time updates, push notification etc, the solution requires two distinct pieces:

* how do we get updates from server to the client?
* how do we get updates from the source to the server?

### Client-Server Connection Protocols

Real-time systems frequently need persistent connections or clever polling strategies to enable servers to push updates to clients.

Below are the topics which will be discussed
* Networking
* Simple Polling
* Long Polling
* Server Sent Events(SSE)
* Websockets
* WebRTC