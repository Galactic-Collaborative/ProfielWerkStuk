from classes.environment import circuitEnv
from tf_agents.environments import utils

environment = circuitEnv()
utils.validate_py_environment(environment, episodes=100)