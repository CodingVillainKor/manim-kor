def run():
    config = yaml.safe_load("file.yaml")
    
    data = Dataset(config["data"])
    model = Model(config.model)
    ...