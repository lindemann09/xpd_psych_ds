from collections import OrderedDict
from json import loads

required = loads("""
{
  "@context": "https://schema.org/",
  "@type": "Dataset",
  "schemaVersion": "Psych-DS 0.1.0",
  "name": ""
}
""", object_pairs_hook=OrderedDict)

recommended = loads("""
{
  "description" : "",
  "keywords": [],
  "license" : "",
  "temporalCoverage" : "",
  "spatialCoverage" : "",
  "datePublished" : "",
  "dateCreated" : "",
  "variableMeasured": []
}
""", object_pairs_hook=OrderedDict)

optional = loads("""
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
""", object_pairs_hook=OrderedDict)

variable_required = loads("""
{
  "@type": "PropertyValue",
  "name": ""
}
""", object_pairs_hook=OrderedDict)

variable_recommended = loads("""
{
  "description": "",
  "levels": [ ]
}
""", object_pairs_hook=OrderedDict)




