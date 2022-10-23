# -*- coding: utf-8 -*-
"""SolucionTask07.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Wj3UvRF2uwEnTMakKm1Cktq8eX-Eb_jQ

**Task 07: Querying RDF(s)**
"""

# !pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2021-2022/master/Assignment4/course_materials"

"""Leemos el fichero RDF de la forma que lo hemos venido haciendo"""

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")

"""**TASK 7.1: List all subclasses of "Person" with RDFLib and SPARQL**"""

# TO DO
print()
print("TASK 7.1")
print()
print("RDFLib: ")
ns = Namespace("http://somewhere#")


def find_subclasses(sc: str) -> None:
  SubClasses = g.triples((None, RDFS.subClassOf, sc))
  if SubClasses:
    for s, p, o in SubClasses:
      print("SubClass: ", s)
      find_subclasses(s)


find_subclasses(ns.Person)

print()
print("SPARQL:")
q1 = """
PREFIX ns: <http://somewhere#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?subClass
WHERE {
    ?subClass rdfs:subClassOf/rdfs:subClassOf* ns:Person
}"""

# Visualize the results

for r in g.query(q1):
  print(r.subClass)

"""**TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**

"""

# TO DO
print()
print("----------------------------------------------------------------------")
print("TASK 7.2")
print()
print("RDFLib:")


def find_individuals(c: str) -> None:
  Individuals = g.triples((None, RDF.type, c))
  SubClasses = g.triples((None, RDFS.subClassOf, c))
  if SubClasses and Individuals:
    if Individuals:
      for s, p, o in Individuals:
        print("Individual: ", s)
    for s1, p1, o1 in SubClasses:
      find_individuals(s1)


find_individuals(ns.Person)


print()
print("SPARQL:")
print()
q2 = """
PREFIX ns: <http://somewhere#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?individual 
WHERE {
    ?subClass rdfs:subClassOf* ns:Person.
    ?individual rdf:type ?subClass.
}"""

# Visualize the results

for r in g.query(q2):
  print(r.individual)

"""**TASK 7.3: List all individuals of "Person" and all their properties including their class with RDFLib and SPARQL**

"""

# TO DO
print()
print("----------------------------------------------------------------------")
print("TASK 7.3")
print()
print("RDFLib:")
print()


def properties(i: str) -> None:
  properties = g.triples((i, None, None))
  if properties:
    for s, p, o in properties:
      for s1, p1, o1 in g.triples((p, RDF.type, None)):
        print(" ", "Property: ", p, "; Class of property: ", p1, "; Value: ", o)


def find_individuals(c: str) -> None:
  Individuals = g.triples((None, RDF.type, c))
  SubClasses = g.triples((None, RDFS.subClassOf, c))
  if SubClasses and Individuals:
    if Individuals:
      for s, p, o in Individuals:
        print("Individual: ", s)
        properties(s)
    for s1, p1, o1 in SubClasses:
      find_individuals(s1)


find_individuals(ns.Person)

print()
print("SPARQL:")
q3 = """
PREFIX ns: <http://somewhere#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?individual ?Property ?Class ?valueProperty
WHERE {
    ?subClass rdfs:subClassOf* ns:Person.
    ?individual rdf:type ?subClass.
    ?individual ?Property ?valueProperty.
    ?Property rdf:type ?Class
}"""

# Visualize the results
for r in g.query(q3):
  print(r.individual, r.Property, r.Class, r.valueProperty)