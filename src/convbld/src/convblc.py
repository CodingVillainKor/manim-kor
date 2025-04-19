import torch.nn as nn

class Conv1dBLC(nn.Conv1d):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def forward(self, x):
        # x.shape : B, L, C
        x = x.transpose(1, 2) # B, C, L
        x = super().forward(x)
        x = x.transpose(1, 2)

        return x