import torch.optim

config = {"optim": "Adam"} # string
optim_name = config["optim"]

optim_class = getattr(torch.optim, optim_name)
print(optim_class)
