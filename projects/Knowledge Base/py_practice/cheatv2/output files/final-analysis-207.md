# Question 1: WAN Configuration
Which commands could be configured on the gateway router to allow Internet access to the entire network?

# Answer
a) 1 only

# Explanation
To allow Internet access to the entire network, a default route needs to be configured. Command 1 (ip route 0.0.0.0 0.0.0.0 206.143.5.2) creates a default route pointing all traffic to the ISP's gateway (206.143.5.2). This is the standard way to provide Internet access for all devices on the internal network.

The other commands relate to RIP routing configuration which is not necessary for basic Internet access in this scenario. Command 4 is syntactically incorrect as "default" is not a valid parameter for the network command in RIP configuration mode.

# Question 2: Safe Sequence - I
Which out of the following is/are a safe sequence?

# Answer
c) <P3, P2, P1, P4, P5>

# Explanation
To determine the safe sequence, we need to check if each process in the sequence can complete execution based on available resources.

First, let's calculate the available resources:
- Total instances: R1=10, R2=7, R3=5
- Allocated instances: R1=8, R2=6, R3=3
- Available instances: R1=2, R2=1, R3=2

Next, calculate the need for each process (Maximum - Allocation):
- P1: <4, 2, 1>
- P2: <4, 0, 0>
- P3: <0, 0, 1>
- P4: <1, 0, 0>
- P5: <0, 1, 1>

Checking sequence <P3, P2, P1, P4, P5>:
1. P3 needs <0, 0, 1> and available is <2, 1, 2> - P3 can execute
   After P3 completes: Available becomes <4, 2, 2>
2. P2 needs <4, 0, 0> and available is <4, 2, 2> - P2 can execute
   After P2 completes: Available becomes <5, 4, 3>
3. P1 needs <4, 2, 1> and available is <5, 4, 3> - P1 can execute
   After P1 completes: Available becomes <6, 5, 4>
4. P4 needs <1, 0, 0> and available is <6, 5, 4> - P4 can execute
   After P4 completes: Available becomes <7, 7, 5>
5. P5 needs <0, 1, 1> and available is <7, 7, 5> - P5 can execute

This sequence allows all processes to complete, making it safe. Options a) and b) contain repeated processes which is invalid, and option d) cannot proceed as P5 cannot execute first due to insufficient available resources.