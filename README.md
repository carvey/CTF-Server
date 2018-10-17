# CTF Server

Socket based CTF server designed for quickly adding new problems.

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


#### TODOs
- More Problems: https://docs.google.com/document/d/e/2PACX-1vQAxmBlS6r_dV09oTRCCU0_qXpK0RbRCcpkDickraN8bS212uYju4b7gpt2KDkS5FrIN3d9FyZVwxez/pub
- Add UDP functionality to the server startup logic, and some modifications/additions will be needed tosend and receive functionality in `ProblemBase`. 
- Some instructions are sent when each user connects to a problem, but each problem could use some contextual information for instruction purposes.
	- These write ups can be built with the HTML files found in the web/ directory that is served upon server startup.
