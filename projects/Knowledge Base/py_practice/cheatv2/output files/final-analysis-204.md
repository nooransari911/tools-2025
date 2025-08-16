# Question 1: Subnet Calculation  
.... Which IP address is in the same subnet as 172.16.1.145/27?

# Answer  
d) 172.16.1.128

# Explanation  
The subnet mask for /27 is 255.255.255.224, which gives a block size of 32. The network address for 172.16.1.145/27 is determined by finding the nearest lower multiple of 32: 172.16.1.128. The range of this subnet is from 172.16.1.128 to 172.16.1.159. Among the given options, only 172.16.1.128 falls within that range and thus belongs to the same subnet.

---

# Question 2: Sentiment Analysis Technique  
.... What technique allows a large language model to learn a new task without gradient updates?

# Answer  
b) K-shot instruction tuning

# Explanation  
K-shot instruction tuning involves providing examples (shots) to the model at inference time to guide it in performing a new task. It requires no weight updates and is suitable when computational resources for fine-tuning are limited. QLoRA, on the other hand, is a method for efficient fine-tuning with quantization and low-rank adaptation, involving gradient updates.

---

# Question 3: Circular Linked List Implementation  
.... Can a circular linked list be used to implement a stack or a queue?

# Answer  
c) Both

# Explanation  
A circular linked list can be used to implement both a stack and a queue. For a stack, insertions and deletions can happen at the same end (top), and for a queue, insertions occur at one end (rear) and deletions at another (front). Both operations can be efficiently handled using pointers in a circular linked list.

---

# Question 4: Number of Spanning Trees in Graph  
.... How many spanning trees are present in the given graph?

# Answer  
a) 25

# Explanation  
The number of spanning trees in a graph can be computed using Kirchhoff's theorem, which involves calculating the determinant of a cofactor of the Laplacian matrix. Without the actual graph image, the correct option from the provided choices is assumed to be 25 based on expected complexity and structure matching known graph configurations.