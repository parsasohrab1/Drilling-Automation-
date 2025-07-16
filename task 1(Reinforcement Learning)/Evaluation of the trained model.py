import numpy as np
import matplotlib.pyplot as plt
from stable_baselines3 import PPO
from gym import spaces
import gym

# تعریف محیط صنعتی (مثل قبل)
class IndustrialSystemEnv(gym.Env):
    def __init__(self):
        super(IndustrialSystemEnv, self).__init__()

        self.observation_space = spaces.Box(
            low=np.array([0, 0, 0, 0], dtype=np.float32),
            high=np.array([100, 200, 10, 1000], dtype=np.float32),
            dtype=np.float32
        )

        self.action_space = spaces.Box(
            low=np.array([-1, -1], dtype=np.float32),
            high=np.array([1, 1], dtype=np.float32),
            dtype=np.float32
        )

        self.max_steps = 200
        self.current_step = 0
        self.state = None

    def reset(self):
        self.state = np.array([
            np.random.uniform(20, 30),
            np.random.uniform(50, 60),
            np.random.uniform(0, 1),
            np.random.uniform(100, 120)
        ], dtype=np.float32)
        self.current_step = 0
        return self.state

    def step(self, action):
        self.current_step += 1
        motor_speed_adjustment, flow_adjustment = action

        temp_change = 0.5 * motor_speed_adjustment - 0.2 * flow_adjustment
        pressure_change = 0.3 * flow_adjustment + 0.1 * motor_speed_adjustment
        vibration_change = 0.4 * abs(motor_speed_adjustment) - 0.1 * flow_adjustment
        energy_change = 0.7 * abs(motor_speed_adjustment) + 0.3 * abs(flow_adjustment)

        self.state[0] += temp_change
        self.state[1] += pressure_change
        self.state[2] += vibration_change
        self.state[3] += energy_change

        self.state[0] = np.clip(self.state[0], 0, 100)
        self.state[1] = np.clip(self.state[1], 0, 200)
        self.state[2] = np.clip(self.state[2], 0, 10)
        self.state[3] = np.clip(self.state[3], 0, 1000)

        reward = self._calculate_reward()
        done = self.current_step >= self.max_steps

        return self.state, reward, done, {}

    def _calculate_reward(self):
        temp, pressure, vibration, energy = self.state
        reward = 0
        if temp > 80 or temp < 10:
            reward -= 10
        if pressure > 150:
            reward -= 15
        if vibration > 5:
            reward -= 20
        reward += (100 - energy / 10) * 0.1
        if 20 < temp < 60 and 50 < pressure < 100 and vibration < 2:
            reward += 5
        return reward

    def render(self, mode='human'):
        print(f"Step: {self.current_step}")
        print(f"Temperature: {self.state[0]:.2f} °C")
        print(f"Pressure: {self.state[1]:.2f} bar")
        print(f"Vibration: {self.state[2]:.2f} mm/s")
        print(f"Energy Consumption: {self.state[3]:.2f} kW")
        print("----------------------")

# ----------- ارزیابی مدل آموزش دیده -----------

# بارگذاری مدل PPO آموزش دیده
model = PPO.load("best_industrial_ppo_model")


# ایجاد محیط برای ارزیابی
env = IndustrialSystemEnv()

episodes = 20  # تعداد اپیزودهای ارزیابی
rewards = []

for ep in range(episodes):
    obs = env.reset()
    done = False
    total_reward = 0
    while not done:
        action, _states = model.predict(obs, deterministic=True)  # اقدام بر اساس مدل
        obs, reward, done, info = env.step(action)
        total_reward += reward
        # env.render()   # اگر می‌خوای وضعیت رو چاپ کنی، این خط رو فعال کن
    print(f"Episode {ep + 1} Reward: {total_reward:.2f}")
    rewards.append(total_reward)

# رسم نمودار پاداش‌ها
import matplotlib.pyplot as plt

plt.plot(range(1, episodes + 1), rewards, marker='o')
plt.xlabel('Episode')
plt.ylabel('Total Reward')
plt.title('Evaluation of Trained PPO Model')
plt.grid(True)
plt.show()
