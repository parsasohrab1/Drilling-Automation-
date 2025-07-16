import torch
import torch.nn as nn
import torch.optim as optim
from torch.distributions import Normal
import numpy as np
from collections import deque
import random


class ActorCritic(nn.Module):
    """شبکه عصبی Actor-Critic برای PPO"""

    def __init__(self, state_dim, action_dim):
        super(ActorCritic, self).__init__()

        # لایه‌های مشترک
        self.shared_layers = nn.Sequential(
            nn.Linear(state_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU()
        )

        # بخش Actor
        self.actor_mean = nn.Linear(64, action_dim)
        self.actor_logstd = nn.Parameter(torch.zeros(1, action_dim))

        # بخش Critic
        self.critic = nn.Linear(64, 1)

    def forward(self, state):
        """محاسبه میانگین و انحراف معیار اقدامات و مقدار حالت"""
        shared = self.shared_layers(state)

        # محاسبه اقدامات
        mean = self.actor_mean(shared)
        logstd = self.actor_logstd.expand_as(mean)
        std = torch.exp(logstd)

        # محاسبه مقدار حالت
        value = self.critic(shared)

        return mean, std, value


class PPO:
    """پیاده‌سازی الگوریتم PPO"""

    def __init__(self, state_dim, action_dim):
        self.policy = ActorCritic(state_dim, action_dim)
        self.optimizer = optim.Adam(self.policy.parameters(), lr=3e-4)

        # پارامترهای PPO
        self.gamma = 0.99
        self.eps_clip = 0.2
        self.K_epochs = 10
        self.buffer = deque(maxlen=2048)

    def select_action(self, state):
        """انتخاب اقدام بر اساس سیاست فعلی"""
        state = torch.FloatTensor(state).unsqueeze(0)
        with torch.no_grad():
            mean, std, _ = self.policy(state)

        dist = Normal(mean, std)
        action = dist.sample()
        log_prob = dist.log_prob(action)

        return action.squeeze(0).numpy(), log_prob.squeeze(0).numpy()

    def update(self):
        """به‌روزرسانی سیاست با استفاده از داده‌های بافر"""
        if len(self.buffer) < 512:  # حداقل اندازه بافر برای به‌روزرسانی
            return

        # تبدیل بافر به تانسورها
        states = torch.FloatTensor(np.array([t[0] for t in self.buffer]))
        actions = torch.FloatTensor(np.array([t[1] for t in self.buffer]))
        old_log_probs = torch.FloatTensor(np.array([t[2] for t in self.buffer]))
        rewards = torch.FloatTensor(np.array([t[3] for t in self.buffer]))
        next_states = torch.FloatTensor(np.array([t[4] for t in self.buffer]))
        dones = torch.FloatTensor(np.array([t[5] for t in self.buffer]))

        # محاسبه بازده‌های تخفیف‌دار
        with torch.no_grad():
            _, _, values = self.policy(states)
            _, _, next_values = self.policy(next_states)
            targets = rewards + (1 - dones) * self.gamma * next_values
            advantages = targets - values

        # نرمال‌سازی مزیت‌ها
        advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)

        # به‌روزرسانی سیاست در K_epochs
        for _ in range(self.K_epochs):
            # محاسبه احتمالات جدید
            means, stds, values = self.policy(states)
            dists = Normal(means, stds)
            new_log_probs = dists.log_prob(actions)

            # محاسبه نسبت احتمالات
            ratios = torch.exp(new_log_probs - old_log_probs)

            # محاسبه ضررهای PPO
            surr1 = ratios * advantages
            surr2 = torch.clamp(ratios, 1 - self.eps_clip, 1 + self.eps_clip) * advantages
            policy_loss = -torch.min(surr1, surr2).mean()

            value_loss = 0.5 * (targets - values).pow(2).mean()

            # محاسبه آنتروپی برای تشویق اکتشاف
            entropy_loss = -dists.entropy().mean()

            # بهینه‌سازی
            loss = policy_loss + 0.5 * value_loss + 0.01 * entropy_loss
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

        # پاکسازی بافر
        self.buffer.clear()

    def save_model(self, path):
        """ذخیره مدل آموزش دیده"""
        torch.save(self.policy.state_dict(), path)

    def load_model(self, path):
        """بارگذاری مدل از فایل"""
        self.policy.load_state_dict(torch.load(path))