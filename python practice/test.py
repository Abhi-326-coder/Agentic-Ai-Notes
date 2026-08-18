# class Model:
#     def __init__(self, name):
#         self.name = name

#     def predict(self, x):
#         raise NotImplementedError

# class LinearModel(Model):
#     def __init__(self, name, weights):
#         super().__init__(name)   # call parent's __init__
#         self.weights = weights

#     def predict(self, x):
#         return sum(w * xi for w, xi in zip(self.weights, x))

# m = Model("gpt")
# model = LinearModel(20)
# print(model.predict(8))


