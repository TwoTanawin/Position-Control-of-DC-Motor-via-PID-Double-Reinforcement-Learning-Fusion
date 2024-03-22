import gym
from stable_baselines3 import A2C
from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
import os
import time

model_dir = f"models/PPO-{int(time.time())}"
logdir = f"logs/PPO-{int(time.time())}"

if not os.path.exists(model_dir):
    os.makedirs(model_dir)

if not os.path.exists(logdir):
    os.makedirs(logdir)


env = gym.make("LunarLander-v2" , render_mode="rgb_array")

env.reset()

# model = A2C("MlpPolicy", env, verbose=1, tensorboard_log=logdir)
model = PPO("MlpPolicy", env, verbose=1, tensorboard_log=logdir)

TIMESTEPS = 10_000 
for i in range(1, 100):
    model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name="PPO")
    model.save(f"{model_dir}/{TIMESTEPS*i}")

# episodes = 10
# for ep in range(episodes):
#     obs = env.reset()
#     done = False

#     while not done:
#         env.render()  
#         obs, reward, done, info, _ = env.step(env.action_space.sample())
#         # print(reward)

env.close()