# CTF Server

Questions are designed to be taken on by those in the C Programming class who are able to finish the core set of problems before the course has ended.

#### Usage:
```
python3 server.py
```

#### Problem Structure
- Problems must extend the `ProblemBase` class
- Problems must implement a `handle` method to interact with user data
- Problems should send a flag using the `send_flag` method
- For a problem to be made available to users, it must be placed in the `tcp_problems` dictionary in the problems.py file. 
	- The server expects this dictionary to contain tcp ports as the keys, and problem class references as the values
