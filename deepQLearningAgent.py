from __future__ import absolute_import, division, print_function
import os

import pyglet
from gym.envs.box2d.car_racing import CarRacing

from classes.car import Car
from classes.circuit import circuit
from classes.Vector import Vector2D
from classes.environment import circuitEnv

import gym
import base64
import tempfile
import numpy as np
import pyglet
import tensorflow as tf

from tf_agents.agents.dqn import dqn_agent
from tf_agents.drivers import dynamic_step_driver
from tf_agents.environments import tf_py_environment
from tf_agents.environments import suite_gym
from tf_agents.eval import metric_utils
from tf_agents.metrics import tf_metrics
from tf_agents.networks import q_network
from tf_agents.policies import random_tf_policy
from tf_agents.replay_buffers import tf_uniform_replay_buffer
from tf_agents.trajectories import trajectory
from tf_agents.utils import common


#Hypervariables
tempdir = os.getenv("TEST_TMPDIR", tempfile.gettempdir())


#Hyperparamters
num_iterations = 20000

initial_collect_steps = 100  
collect_steps_per_iteration = 1
replay_buffer_max_length = 100000 

batch_size = 64 
learning_rate = 1e-3
log_interval = 200 

num_eval_episodes = 10
eval_interval = 1000 

save_interval = 2000

train_env = tf_py_environment.TFPyEnvironment(circuitEnv())
eval_env = tf_py_environment.TFPyEnvironment(circuitEnv())

print(train_env.time_step_spec())

fc_layers_params = (100,)
q_net = q_network.QNetwork(
    train_env.observation_spec(),
    train_env.action_spec(),
    fc_layer_params=fc_layers_params
)

optimizer = tf.compat.v1.train.AdamOptimizer(learning_rate=learning_rate)
train_step_counter = tf.Variable(0)

agent = dqn_agent.DqnAgent(
    train_env.time_step_spec(),
    train_env.action_spec(),
    q_network=q_net,
    optimizer=optimizer,
    td_errors_loss_fn=common.element_wise_squared_loss,
    train_step_counter=train_step_counter,
    epsilon_greedy=0.99
)
agent.initialize()


eval_policy = agent.policy
collect_policy = agent.collect_policy
random_policy = random_tf_policy.RandomTFPolicy(
    train_env.time_step_spec(),
    train_env.action_spec()
)


replay_buffer = tf_uniform_replay_buffer.TFUniformReplayBuffer(
    data_spec = agent.collect_data_spec,
    batch_size=train_env.batch_size,
    max_length=replay_buffer_max_length,
)

def compute_avg_return(environment, policy, num_episodes=10):
  print("Computing Average Return...")

  total_return = 0.0
  for _ in range(num_episodes):

    time_step = environment.reset()
    episode_return = 0.0

    while not time_step.is_last():
      action_step = policy.action(time_step)
      time_step = environment.step(action_step.action)
      episode_return += time_step.reward
      environment.render('human')
    total_return += episode_return

  avg_return = total_return / num_episodes
  return avg_return.numpy()[0]

def collect_step(environment, policy, buffer):
  time_step = environment.current_time_step()
  action_step = policy.action(time_step)
  next_time_step = environment.step(action_step.action)
  traj = trajectory.from_transition(time_step, action_step, next_time_step)

  # Add trajectory to the replay buffer
  buffer.add_batch(traj)

  # Draw the current situation
  environment.render('human')


def collect_data(env, policy, buffer, steps):
  for _ in range(steps):
    collect_step(env, policy, buffer)
  
collect_data(train_env, random_policy, replay_buffer, initial_collect_steps)

dataset = replay_buffer.as_dataset(
    num_parallel_calls=3,
    sample_batch_size=batch_size,
    num_steps=2,
    single_deterministic_pass=True
).prefetch(3)
iterator = iter(dataset)

### TRAINING THE AGENT ###
global_step = tf.compat.v1.train.get_or_create_global_step()
checkpoint_dir = os.path.join(tempdir, 'checkpoint')
train_checkpointer = common.Checkpointer(
    ckpt_dir=checkpoint_dir,
    max_to_keep=5,
    agent=agent,
    policy=agent.policy,
    replay_buffer=replay_buffer,
    global_step=global_step
)

# Reset the train step
agent.train_step_counter.assign(0)

# Evaluate the agent's policy once before training.
avg_return = compute_avg_return(eval_env, agent.policy, num_eval_episodes)
returns = [avg_return]

train_checkpointer.initialize_or_restore()
global_step = tf.compat.v1.train.get_global_step()

while True:
  # Collect a few steps using collect_policy and save to the replay buffer.
  collect_data(train_env, agent.collect_policy, replay_buffer, collect_steps_per_iteration)

  # Sample a batch of data from the buffer and update the agent's network.
  experience, unused_info = next(iterator)
  train_loss = agent.train(experience).loss

  step = agent.train_step_counter.numpy()

  if step % log_interval == 0:
    print('step = {0}: loss = {1}'.format(step, train_loss))

  if step % eval_interval == 0:
    print("Computing average return -- Please wait")
    avg_return = compute_avg_return(eval_env, agent.policy, num_eval_episodes)
    print('step = {0}: Average Return = {1}'.format(step, avg_return))
    returns.append(avg_return)
  
  #if step % save_interval == 0:
  #  train_checkpointer.save(global_step)
    