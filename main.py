from SPARQLWrapper import SPARQLWrapper, JSON

def main():
    sparql = SPARQLWrapper("https://sparql.crssnky.xyz/spql/imas/query")
    sparql.setQuery("""
        PREFIX rdfs:  <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX schema: <http://schema.org/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX imas: <https://sparql.crssnky.xyz/imasrdf/URIs/imas-schema.ttl#>
        PREFIX imasrdf: <https://sparql.crssnky.xyz/imasrdf/RDFs/detail/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX math: <http://www.w3.org/2005/xpath-functions/math#>
        PREFIX xsd: <https://www.w3.org/TR/xmlschema11-2/#>

        SELECT ?name
        WHERE {
            ?x imas:cv ?name
        }
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    print(results)


if __name__ == '__main__':
    main()
