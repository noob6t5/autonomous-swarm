import random
import math
import matplotlib.pyplot as plt

# ---------------- CONFIG ----------------
WORLD = 100
N_DEF = 12
N_ATK = 8
N_DECOY = 3

LEADER_BASED = True

DETECTION_RADIUS = 5
ATTACK_SUCCESS_RADIUS = 4

PRESSURE_ATTACK = 18
PRESSURE_RELAX = 6
PRESSURE_DECAY = 0.95

ATTACKER_KILL_PROB = 0.06
LEADER_KILL_PROB = 0.002

MAX_STEPS = 600
# ---------------------------------------


class Agent:
    def __init__(self, x, y, role):
        self.x = x
        self.y = y
        self.role = role

    def move_toward(self, tx, ty, speed):
        dx, dy = tx - self.x, ty - self.y
        dist = math.hypot(dx, dy) + 1e-6
        self.x += speed * dx / dist
        self.y += speed * dy / dist
        self.x = max(0, min(WORLD, self.x))
        self.y = max(0, min(WORLD, self.y))

    def wander(self, speed):
        self.x += random.uniform(-speed, speed)
        self.y += random.uniform(-speed, speed)
        self.x = max(0, min(WORLD, self.x))
        self.y = max(0, min(WORLD, self.y))


class SwarmEnv:
    def __init__(self):
        self.phase = "STEALTH"
        self.pressure = 0

        # Initialize defenders
        self.defenders = [
            Agent(random.uniform(40, 60), random.uniform(40, 60), "DEF")
            for _ in range(N_DEF)
        ]
        self.leader = self.defenders[0] if LEADER_BASED else None

        # Initialize attackers
        self.attackers = [
            Agent(random.uniform(0, 20), random.uniform(0, 20), "ATK")
            for _ in range(N_ATK)
        ]

        # Decoys
        self.decoys = [
            Agent(random.uniform(0, 20), random.uniform(0, 20), "DEC")
            for _ in range(N_DECOY)
        ]

    def centroid(self, agents):
        x = sum(a.x for a in agents) / len(agents)
        y = sum(a.y for a in agents) / len(agents)
        return x, y

    def step(self):
        # ---- Phase logic ----
        if self.pressure > PRESSURE_ATTACK:
            self.phase = "ATTACK"
        elif self.pressure < PRESSURE_RELAX:
            self.phase = "STEALTH"

        def_cx, def_cy = self.centroid(self.defenders)
        atk_cx, atk_cy = self.centroid(self.attackers + self.decoys)

        # ---- Defenders ----
        followers = [d for d in self.defenders if d != self.leader]

        if LEADER_BASED and self.leader:
            self.leader.move_toward(atk_cx, atk_cy, 0.6)
            for f in followers:
                f.move_toward(self.leader.x, self.leader.y, 0.5)
        else:
            for d in self.defenders:
                d.move_toward(def_cx, def_cy, 0.4)

        # ---- Attackers ----
        for a in self.attackers[:]:
            if self.phase == "STEALTH":
                a.wander(0.3)
            else:
                a.move_toward(def_cx, def_cy, 0.9)

        # ---- Decoys ----
        for d in self.decoys:
            d.wander(0.6)

        # ---- Detection & Attrition ----
        for a in self.attackers[:]:
            detected = False
            for d in self.defenders:
                if math.hypot(a.x - d.x, a.y - d.y) < DETECTION_RADIUS:
                    detected = True
                    self.pressure += 1
                    if random.random() < ATTACKER_KILL_PROB:
                        self.attackers.remove(a)
                    break
            if not detected:
                self.pressure -= 0.3

        # ---- Leader vulnerability ----
        if LEADER_BASED and self.leader and random.random() < LEADER_KILL_PROB:
            self.defenders.remove(self.leader)
            if self.defenders:
                self.leader = random.choice(self.defenders)
            else:
                self.leader = None

        # ---- Pressure decay ----
        self.pressure = max(0, self.pressure * PRESSURE_DECAY)

    def defense_lost(self):
        # Attackers penetrate core
        for a in self.attackers:
            if math.hypot(a.x - 50, a.y - 50) < ATTACK_SUCCESS_RADIUS:
                return True
        return False

    def defense_won(self):
        return len(self.attackers) == 0


def visualize():
    env = SwarmEnv()
    plt.ion()
    fig, ax = plt.subplots()

    for t in range(MAX_STEPS):
        env.step()
        ax.clear()
        ax.set_xlim(0, WORLD)
        ax.set_ylim(0, WORLD)

        # Core
        ax.scatter(50, 50, c="green", s=200, marker="X", label="Protected Core")

        # Defenders
        ax.scatter(
            [d.x for d in env.defenders],
            [d.y for d in env.defenders],
            c="blue",
            s=50,
            label="Defenders",
        )

        # Leader
        if LEADER_BASED and env.leader:
            ax.scatter(
                env.leader.x,
                env.leader.y,
                c="cyan",
                s=140,
                edgecolors="black",
                label="Leader",
            )

        # Attackers
        color = "red" if env.phase == "ATTACK" else "orange"
        ax.scatter(
            [a.x for a in env.attackers],
            [a.y for a in env.attackers],
            c=color,
            s=50,
            label=f"Attackers ({env.phase})",
        )

        # Decoys
        ax.scatter(
            [d.x for d in env.decoys],
            [d.y for d in env.decoys],
            c="yellow",
            s=30,
            label="Decoys",
        )

        ax.set_title(f"Autonomous Defensive Swarm | Pressure: {int(env.pressure)}")
        ax.legend(loc="upper right")
        plt.pause(0.05)

        # Mission end
        if env.defense_won():
            ax.set_title("DEFENSE SUCCESS")
            plt.pause(2)
            break
        if env.defense_lost():
            ax.set_title("DEFENSE FAILED")
            plt.pause(2)
            break

    plt.ioff()
    plt.show()


if __name__ == "__main__":
    visualize()
