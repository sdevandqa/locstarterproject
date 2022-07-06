# Getting Started

# Overview:
A starting point for simple load tests using https://locust.io/. Single user and multi-user authentication starter code for small projects.

# PIP Packages:
- pip install locust
- pip install json

# Test Running Examples:
- locust -f .\single_user_locust_file.py --host=http://my_target_url -> This will spin up the web UI for locust and allow you to configure tests from the web UI.
- locust -f .\multi_user_locust_file.py --host=http://my_target_url --headless -u 2 -> This will set the host and spawn two users.

Further reference: https://locust.io/