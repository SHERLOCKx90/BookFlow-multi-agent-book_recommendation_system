import torch
import torch.nn as nn
import torch.optim as optim

class ActorCriticModel(nn.Module):
    def __init__(self, input_dim=3, output_dim=3):
        super(ActorCriticModel, self).__init__()
        self.fc = nn.Linear(input_dim, 128)
        self.actor = nn.Linear(128, output_dim)
        self.critic = nn.Linear(128, 1)

    def forward(self, x):
        x = torch.relu(self.fc(x))  # Removed batch norm, directly applying ReLU
        policy = torch.softmax(self.actor(x), dim=-1)
        value = self.critic(x)
        return policy, value

class ActorCriticAgent:
    def __init__(self, num_agents, lr=0.01, gamma=0.99):
        self.model = ActorCriticModel(input_dim=3, output_dim=num_agents)
        self.optimizer = optim.Adam(self.model.parameters(), lr=lr)
        self.gamma = gamma

    def select_action(self, state):
        policy, _ = self.model(state)
        action = torch.multinomial(policy, 1).item()
        return action

    def update(self, state, action, reward, next_state):
        policy, value = self.model(state)
        _, next_value = self.model(next_state)

        td_target = reward + self.gamma * next_value
        td_error = td_target - value

        # Compute actor and critic loss
        actor_loss = -torch.log(policy[0, action]) * td_error.detach()  # Use detach() to stop gradient flow
        critic_loss = td_error ** 2

        # Combine losses into a scalar
        loss = (actor_loss + critic_loss).mean()  # Ensures loss is a scalar

        # Backward propagation with gradient clipping
        self.optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)  # Clip gradients to a max norm of 1.0
        self.optimizer.step()
