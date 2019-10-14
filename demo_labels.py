from xpd_psych_ds import psych_ds as ds

d = ds.DataSet(name="Dataset Demo")

variables = []
v = ds.Variable(name="Gender")
v.update("description", "The gender of the person")
v.update("levels", [ds.LevelDescription(1, "Female"),
                    ds.LevelDescription(2, "Male"),])

variables.append(v)

v = ds.Variable(name="Colour")
v.update("description", "The color of the stimulus")
v.update("levels", [ds.LevelDescription(0, "Red"),
                    ds.LevelDescription(1, "Green"),])

variables.append(v)
d.update("variableMeasured", variables)

print(d)
