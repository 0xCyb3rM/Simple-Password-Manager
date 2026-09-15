# Simple Password Manager 🔒
This was a capstone project for DECI level 3 cybersecurity track, built with python.
It acts as a simple **PoC** for **data security at rest**, applies through **hashing** and **encryption** standards

# How It Works ?
1. The User creates a **Master key** that will allow him to access other passwords
2. The Process of Creation of the Master Key ensures that you **follow strict policies**
3. The Master Key is Then Stored after hashing it with **SHA-256** to ensure it's **not recoverable** Practically
4. When he finishes the process, the program will run the second part of it that will ask him for his master key on start


# What the User does
- Once The Master key is entered, The User can:
  
  - Store his passwords , Encrypted with AES-256
  - Generate Strong Passwords
  - Save the Passwords and their URLs in a CSV file (acts as a database)
