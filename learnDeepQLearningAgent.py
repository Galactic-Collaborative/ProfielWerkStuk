import argparse
import gc
import gym
import cv2
import json
import numpy as np
from datetime import datetime
from collections import deque
from classes.DeepQNetwork.DeepQNetworkAgent import CarRacingDQNAgent


def process_state_image(state):
    state = cv2.cvtColor(state, cv2.COLOR_BGR2GRAY)
    state = state.astype(float)
    state /= 255.0
    return state

def generate_state_frame_stack_from_queue(deque):
    frame_stack = np.array(deque)
    # Move stack dimension to the channel dimension (stack, x, y) -> (x, y, stack)
    return np.transpose(frame_stack, (1, 2, 0))

RENDER                        = True
STARTING_EPISODE              = 1
ENDING_EPISODE                = 1000
SKIP_FRAMES                   = 2
TRAINING_BATCH_SIZE           = 16
SAVE_TRAINING_FREQUENCY       = 10
UPDATE_TARGET_MODEL_FREQUENCY = 5

EPSILON_DECAY = .99994

if __name__ == '__main__':
    with open("./save/model.json", "r") as f:
        total_time_frame_counter, episode = json.load(f)
        print(f"Beginning at frame {total_time_frame_counter} on episode {episode}")

    STARTING_EPISODE = episode

    env = gym.make('CarRacing-v0')
    agent = CarRacingDQNAgent(epsilon=(EPSILON_DECAY)**((total_time_frame_counter if total_time_frame_counter > 16 else 16)-16), epsilon_decay=EPSILON_DECAY, memory_size=5000)

    agent.load(f"save/current_model.h5")

    for e in range(STARTING_EPISODE, ENDING_EPISODE+1):
        init_state = env.reset()
        init_state = process_state_image(init_state)

        total_reward = 0
        negative_reward_counter = 0
        state_frame_stack_queue = deque([init_state]*agent.frame_stack_num, maxlen=agent.frame_stack_num)
        time_frame_counter = 1
        done = False
        
        while True:
            if RENDER:
                env.render()

            current_state_frame_stack = generate_state_frame_stack_from_queue(state_frame_stack_queue)
            action = agent.act(current_state_frame_stack)

            reward = 0
            for _ in range(SKIP_FRAMES+1):
                next_state, r, done, info = env.step(action)
                reward += r
                if done:
                    break

            # If continually getting negative reward 10 times after the tolerance steps, terminate this episode
            negative_reward_counter = negative_reward_counter + 1 if time_frame_counter > 100 and reward < 0 else 0

            # Extra bonus for the model if it uses full gas
            if action[1] == 1 and action[2] == 0:
                reward *= 1.5

            total_reward += reward

            next_state = process_state_image(next_state)
            state_frame_stack_queue.append(next_state)
            next_state_frame_stack = generate_state_frame_stack_from_queue(state_frame_stack_queue)

            agent.memorize(current_state_frame_stack, action, reward, next_state_frame_stack, done)

            if done or negative_reward_counter >= 25 or total_reward < 0:
                print('[{}] Episode: {}/{}, Scores(Time Frames): {}, Total Rewards(adjusted): {:.2}, Epsilon: {:.2}'.format(datetime.now(), e, ENDING_EPISODE, time_frame_counter, float(total_reward), float(agent.epsilon)))
                break
            
            gc.collect()
            if len(agent.memory) > TRAINING_BATCH_SIZE:
                agent.replay(TRAINING_BATCH_SIZE)
            time_frame_counter += 1
            total_time_frame_counter += 1

        if e % UPDATE_TARGET_MODEL_FREQUENCY == 0:
            agent.update_target_model()

        if e % SAVE_TRAINING_FREQUENCY == 0:
            agent.save('./save/trial_{}.h5'.format(e), total_time_frame_counter, e)

    print("closing environment")
    env.close()