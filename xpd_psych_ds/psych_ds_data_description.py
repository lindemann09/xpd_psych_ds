from .thing import Thing

PSYCH_DS_VERSION = "0.1.0"

class DataSet(Thing):

    def __init__(self, name):
        super().__init__(type="dataset")
        #required
        self.add_required("@context", "https://schema.org/")
        self.add_required("schemaVersion", "Psych-DS {}".format(PSYCH_DS_VERSION))
        self.add_required("name", name)

        self.add_multiple_recommended([
                     ("description",  ""),
                     ("keywords", []),
                     ("license", ""),
                     ("temporalCoverage", ""),
                     ("spatialCoverage", ""),
                     ("datePublished", ""),
                     ("dateCreated", ""),
                     ("variableMeasured", [])
                    ])


class Variable(Thing):

    def __init__(self, name):
        super().__init__(type="PropertyValue")

        self.add_required("name", name)
        self.add_recommended("description", "")
        self.add_recommended("levels", "")


class Person(Thing):

    def __init__(self, name):
        super().__init__(type="Person")
        self.add_required("name", name)


class LevelDescription(Thing):

    def __init__(self, name, description):
        super().__init__(type="CategoryCode")

        self.add_required("codeValue", name)
        self.add_required("description", description)
