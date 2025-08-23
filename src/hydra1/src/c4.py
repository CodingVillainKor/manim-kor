import hydra

@hydra.main(config_path="configs")
def run(config):
    data_config = config.data
    if config.model.get("pretrained"):
        ...
    else:
        ...

if __name__ == "__main__":
    run()