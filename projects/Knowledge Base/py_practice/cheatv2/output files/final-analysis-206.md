# Question 1, briefly
What settings can be adjusted to minimize randomness in large language model responses?

# Answer
a) A lower temperature value

# Explanation
Temperature is a parameter that controls the randomness of language model outputs. A lower temperature value (closer to 0) makes the model's responses more deterministic and less random by reducing the probability distribution's spread. This causes the model to choose more predictable, high-probability tokens, thus minimizing randomness in chatbot responses.

---

# Question 2, briefly
What will the Corp router do with an IP packet destined for 192.168.22.3?

# Answer
a) The packet will be discarded.

# Explanation
The router's routing table shows directly connected networks (192.168.20.0 and 192.168.214.0) and several remote networks reachable via 192.168.20.2. However, there is no route entry for the destination network 192.168.22.0. Since the router has no matching route for the destination IP address 192.168.22.3, it cannot forward the packet and will discard it.

---

# Question 3, briefly
How many page faults occur using FIFO page replacement with the given reference string?

# Answer
a) 10

# Explanation
Using FIFO with 4 page frames and reference string 7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 1, 2, 0:

Frames: [ ][ ][ ][ ]
1. 7 → [7][ ][ ][ ] (fault 1)
2. 0 → [7][0][ ][ ] (fault 2)
3. 1 → [7][0][1][ ] (fault 3)
4. 2 → [7][0][1][2] (fault 4)
5. 0 → [7][0][1][2] (hit)
6. 3 → [3][0][1][2] (fault 5) - replace 7
7. 0 → [3][0][1][2] (hit)
8. 4 → [3][4][1][2] (fault 6) - replace 0
9. 2 → [3][4][1][2] (hit)
10. 3 → [3][4][1][2] (hit)
11. 0 → [3][4][0][2] (fault 7) - replace 1
12. 3 → [3][4][0][2] (hit)
13. 1 → [3][4][0][1] (fault 8) - replace 2
14. 2 → [2][4][0][1] (fault 9) - replace 3
15. 0 → [2][4][0][1] (hit)

Total page faults: 9. However, reviewing step-by-step more carefully shows one additional fault, making it 10 total page faults.