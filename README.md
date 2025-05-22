# 🌐 Multi-Client TCP Chat Server

[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue?style=flat-square&logo=python)](https://www.python.org/)  
[![Threads](https://img.shields.io/badge/threading-enabled-brightgreen?style=flat-square)]  
[![License: MIT](https://img.shields.io/badge/license-MIT-lightgrey?style=flat-square)](LICENSE)

> A lightweight, multi-threaded TCP chat server in Python—built for learning sockets, threading, and clean protocol design!

---

## 🚀 Key Features

- **🏃 Concurrency**  
  Each client runs in its own thread for seamless, simultaneous chats.

- **📑 Structured Commands**  
  - `JOIN <username>` – enter the chat  
  - `MESG <text>` – broadcast to everyone  
  - `BCST <user> <text>` – send a private message  
  - `QUIT` – exit cleanly

- **🗃️ Per-User Logs**  
  Every user’s session is saved to `logs/<username>.log` for debugging & replay.

- **🤝 Graceful Handling**  
  Disconnects and errors are caught so other clients stay connected.

---

## 🛠️ Installation & Setup

1. **Clone & enter**  
   ```bash
   git clone https://github.com/emileymynhier1/Multi-Client-TCP-Chat-Server.git
   cd Multi-Client-TCP-Chat-Server
