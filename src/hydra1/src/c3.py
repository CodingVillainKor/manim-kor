import hydra

@hydra.main(config_path="configs")
def run(config):
    print(config["data"])
    print(config.model)

if __name__ == "__main__":
    run()