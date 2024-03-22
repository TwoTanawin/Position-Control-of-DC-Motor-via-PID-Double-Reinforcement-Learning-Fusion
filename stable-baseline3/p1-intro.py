import gym
from stable_baselines3 import A2C
from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor


env = gym.make("LunarLander-v2" , render_mode="rgb_array")

env.reset()

# print('smaple action', env.action_space.sample())

# print('observation space shape', env.observation_space.shape)

# print('sample obervation', env.observation_space.sample())

# model = A2C("MlpPolicy", env, verbose=1)
model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=10_000)

episodes = 10
for ep in range(episodes):
    obs = env.reset()
    done = False

    while not done:
        env.render()  
        obs, reward, done, info, _ = env.step(env.action_space.sample())
        # print(reward)

env.close()