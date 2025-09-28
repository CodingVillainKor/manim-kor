...
with open("config.yaml") as f:
    config = yaml.safe_load(f)

models = {
    "Model1": Model1,
    "Model2": Model2,
    "Model3": Model3,
}
Model = models[config["model_name"]]

model = Model(**config["model_config"])
...