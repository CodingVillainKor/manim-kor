import torch.nn as nn

from .convblc import ConvBLC

class Model(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1d = ConvBLC(3, 6, 3)
        self.linear = nn.Linear(6, 5)

    def forward(self, x):
        h = self.conv1d(x)
        y = self.linear(h)

        return y