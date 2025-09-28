...
with open("config.yaml") as f:
    config = yaml.safe_load(f)
model_config = config["model"]

model = Model(
    dim=model_config["dim"],
    depth=model_config["depth"]
)
...