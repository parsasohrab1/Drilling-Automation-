import gym
from gym import spaces
import numpy as np
import matplotlib.pyplot as plt


class IndustrialSystemEnv(gym.Env):
    """محیط سفارشی برای شبیه‌سازی سیستم صنعتی"""

    def __init__(self):
        super(IndustrialSystemEnv, self).__init__()

        # تعریف فضای حالت (دما، فشار، ارتعاش، مصرف انرژی)
        self.observation_space = spaces.Box(
            low=np.array([0, 0, 0, 0]),
            high=np.array([100, 200, 10, 1000]),
            dtype=np.float32
        )

        # تعریف فضای عمل (تنظیم سرعت موتور، تنظیم جریان سیال)
        self.action_space = spaces.Box(
            low=np.array([-1, -1]),
            high=np.array([1, 1]),
            dtype=np.float32
        )

        # پارامترهای سیستم
        self.max_steps = 200
        self.current_step = 0
        self.state = None
        self.reset()

    def reset(self):
        """بازنشانی محیط به حالت اولیه"""
        self.state = np.array([
            np.random.uniform(20, 30),  # دما (C°)
            np.random.uniform(50, 60),  # فشار (bar)
            np.random.uniform(0, 1),  # ارتعاش (mm/s)
            np.random.uniform(100, 120)  # مصرف انرژی (kW)
        ])
        self.current_step = 0
        return self.state

    def step(self, action):
        """اجرای یک گام در محیط"""
        self.current_step += 1

        # اعمال اقدامات
        motor_speed_adjustment, flow_adjustment = action

        # شبیه‌سازی تغییرات حالت
        temp_change = 0.5 * motor_speed_adjustment - 0.2 * flow_adjustment
        pressure_change = 0.3 * flow_adjustment + 0.1 * motor_speed_adjustment
        vibration_change = 0.4 * abs(motor_speed_adjustment) - 0.1 * flow_adjustment
        energy_change = 0.7 * abs(motor_speed_adjustment) + 0.3 * abs(flow_adjustment)

        # به‌روزرسانی حالت
        self.state[0] += temp_change
        self.state[1] += pressure_change
        self.state[2] += vibration_change
        self.state[3] += energy_change

        # اعمال محدودیت‌های فیزیکی
        self.state[0] = np.clip(self.state[0], 0, 100)
        self.state[1] = np.clip(self.state[1], 0, 200)
        self.state[2] = np.clip(self.state[2], 0, 10)
        self.state[3] = np.clip(self.state[3], 0, 1000)

        # محاسبه پاداش
        reward = self._calculate_reward()

        # بررسی پایان اپیزود
        done = self.current_step >= self.max_steps

        return self.state, reward, done, {}

    def _calculate_reward(self):
        """محاسبه پاداش بر اساس KPIs"""
        temp, pressure, vibration, energy = self.state

        # پاداش منفی برای خارج شدن از محدوده ایمن
        reward = 0

        # جریمه برای دماهای بالا/پایین
        if temp > 80 or temp < 10:
            reward -= 10

        # جریمه برای فشارهای بالا
        if pressure > 150:
            reward -= 15

        # جریمه برای ارتعاشات خطرناک
        if vibration > 5:
            reward -= 20

        # پاداش برای کاهش مصرف انرژی
        reward += (100 - energy / 10) * 0.1

        # پاداش برای کار در محدوده بهینه
        if 20 < temp < 60 and 50 < pressure < 100 and vibration < 2:
            reward += 5

        return reward

    def render(self, mode='human'):
        """نمایش وضعیت سیستم"""
        print(f"Step: {self.current_step}")
        print(f"Temperature: {self.state[0]:.2f} °C")
        print(f"Pressure: {self.state[1]:.2f} bar")
        print(f"Vibration: {self.state[2]:.2f} mm/s")
        print(f"Energy Consumption: {self.state[3]:.2f} kW")
        print("----------------------")