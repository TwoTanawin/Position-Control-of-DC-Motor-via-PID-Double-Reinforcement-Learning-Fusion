import gym
from stable_baselines3 import A2C
from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
import os

model_dir = "/home/two-asus/Documents/computing/reinforcement/tutorial/models/A2C"


env = gym.make("LunarLander-v2" , render_mode="human")

env.reset()

model_path = f"{model_dir}/290000.zip"

model = PPO.load(model_path, env=env)

episodes = 10
for ep in range(episodes):
    obs, info = env.reset()
    done = False

    while not done:
        env.render() 
        action, _ = model.predict(obs) 
        obs, reward, done, info, _ = env.step(action)
        # print(reward)

env.close()