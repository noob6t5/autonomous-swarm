# Strictly used Just for educational Purpose **I  repeat Stickly used to conquer Curious Mind Not to harm Any systems,Anybody**

# Autonomous Defensive Swarm Simulation

## Overview
This project simulates an **autonomous defensive swarm** tasked with protecting a central asset against adaptive attackers and decoys. The simulation demonstrates the effects of **leader-based vs leaderless coordination**, **pressure-adaptive responses**, and **symmetry-breaking strategies** on mission success.  

Key insights:
- **Coordination diversity**, not raw agent count, drives survivability under deceptive conditions.
- Leader-based coordination can accelerate response but is sensitive to leader loss.
- Randomized mutation and adaptive behavior improve overall swarm resilience.

The project includes:
- Agent-based simulation environment (`SwarmEnv`)
- Evaluation functions for win rate and average mission time
- Visualization of defenders, attackers, decoys, and leader dynamics
- Adjustable parameters for pressure, attack success, and agent behavior


<img width="618" height="465" alt="Screenshot_2026-01-04_18-48-52" src="https://github.com/user-attachments/assets/9e246e9f-4b82-4e6a-9df6-cabfcc091842" />

<img width="591" height="501" alt="Screenshot_2026-01-04_18-48-27" src="https://github.com/user-attachments/assets/a7b09666-8eeb-47ad-b113-ce52858aa65f" />

<img width="617" height="477" alt="Screenshot_2026-01-04_18-48-03" src="https://github.com/user-attachments/assets/ca392dbb-1ff4-4f41-8831-f4f4651e36df" />

---

## Installation
Requires Python 3 and Matplotlib.

```bash
pip install matplotlib
git clone https://github.com/noob6t5/autonomous-swarm && cd autonomous-swarm
python3 autonomous.py
```

 This model operates at the decision layer, making it applicable across domains:

 - Autonomous drones   
 -  Cyber defense agents    
 - Sensor fusion networks  
 - Distributed intrusion detection

