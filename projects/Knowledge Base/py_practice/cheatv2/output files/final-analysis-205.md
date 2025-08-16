# Question 1: WAN Configuration
Which commands could be configured on the gateway router to allow Internet access to the entire network?

# Answer
a) 1 only

# Explanation
The correct command is "ip route 0.0.0.0 0.0.0.0 206.143.5.2" which creates a default route to the ISP router. This single static route is sufficient to allow Internet access for the entire network. The other options shown are not complete or relevant - option 2 shows only "router rip" without complete configuration, and there's no option 4 visible. Only the default route configuration in option 1 is needed and sufficient.

---

# Question 2: Middleware in RESTful API
Which tasks can be handled by middleware in a RESTful API?

# Answer
a) Authentication, b) Caching, c) Versioning of API

# Explanation
Middleware in RESTful APIs can handle all of these tasks: Authentication (validating user credentials and permissions), Caching (storing responses to reduce server load and improve performance), and Versioning of API (managing different API versions). The correct answer would include all three options, though the multiple choice format suggests selecting individual options rather than "all of the above."

---

# Question 3: Authentication Practices for RESTful APIs
Which of the following authentication practices is not recommended for RESTful APIs?

# Answer
a) Using session-based authentication

# Explanation
Session-based authentication is not recommended for RESTful APIs because it violates the stateless principle of REST. REST APIs should be stateless, meaning each request should contain all the information needed to process it. Session-based authentication requires the server to maintain session state, which creates scalability and complexity issues. Token-based authentication (option b) is recommended as it's stateless and self-contained.

---

# Question 4: Stack Operations
What is the final state of the stack after performing the given operations?

# Answer
d) [44, 12, 28]

# Explanation
Starting with empty stack, the operations proceed as follows:
- Push(78): [78]
- Pop(): []
- Push(44): [44]
- Push(12): [44, 12]
- Push(18): [44, 12, 18]
- Pop(): [44, 12]
- Push(19): [44, 12, 19]
- Pop(): [44, 12]
- Pop(): [44]
- Push(12): [44, 12]
- Push(28): [44, 12, 28]