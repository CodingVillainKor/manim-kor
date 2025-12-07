import torch
import torch.nn as nn
from accelerate import Accelerator

class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.linear = nn.Linear(4, 4)

    def forward(self, x):
        out = self.linear(x)
        print(out.dtype)
        return out

def main():
    accelerator = Accelerator()

    model = Model()
    model = accelerator.prepare(model)

    input_data = torch.randn(4, 4).to(accelerator.device)

    output = model(input_data)
    print("Outside:", output.dtype)

if __name__ == "__main__":
    main()