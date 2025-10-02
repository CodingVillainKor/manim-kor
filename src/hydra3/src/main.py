import hydra
from hydra.utils import instantiate

@hydra.main(config_path="configs")
def main(config):
    m = instantiate(config.model)