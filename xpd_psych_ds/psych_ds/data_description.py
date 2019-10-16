from . import PSYCH_DS_VERSION
from .thing import Thing

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
        self.add_recommended("levels", [])


class Person(Thing):

    def __init__(self, name):
        super().__init__(type="Person")
        self.add_required("name", name)


class LevelDescription(Thing):

    def __init__(self, name, description):
        super().__init__(type="CategoryCode")

        self.add_required("codeValue", name)
        self.add_required("description", description)


"""
optional data_set

{
  "creator": [
  {
	"@type": "Person",
     "name": ""
  }
  ],
  "citation" : "",
  "funder" : [""],
  "url" : [""]
}
"""