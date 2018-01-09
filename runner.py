from tensorforce.agents import PPOAgent, DQNAgent, DDQNAgent

# parameters specific to MemoryAgents
#         batch_size=32,
#         memory=None,
#         first_update=10000,
#         update_frequency=4,
#         repeat_update=1,
#         # parameters specific to dqn-agents
#         target_sync_frequency=10000,
#         target_update_weight=1.0,
#         double_q_model=False,
#         huber_loss=None

#
agent = PPOAgent(
    states_spec=dict(type='float', shape=(2,)), # shape - wymiar/przestrzen
    actions_spec=dict(shape=(2,), type='float', min_value=-1, max_value=1),
    network_spec=[
        dict(type='dense', size=64),
        dict(type='dense', size=64),

    ],

    batch_size=100,

    # step_optimizer=dict(
    #     type='adam',
    #     learning_rate=1e-4
    # )
)

# Get new data from somewhere, e.g. a client to a web app


state = [0,0]

while True:
    # # Poll new state from client
    #
    # # Get prediction from agent, execute
    action = agent.act(state)
    print(action)
    state = action
    if 0 < action[0] < 1 and 0 < action[1] <1:
        reward = 100
    else:
        reward = 1
    #
    # # Add experience, agent automatically updates model according to batch size
    agent.observe(reward=reward, terminal=False)

