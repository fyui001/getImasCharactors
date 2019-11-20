from SPARQLWrapper import SPARQLWrapper, JSON
import modules as mod

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
    sparql_data = sparql.query().convert()
    db_data = mod.get()
    voice_actor_lists = []
    value_lists = []

    for row in sparql_data['results']['bindings']:
        if row['name']['type'] == 'literal':
            voice_actor_lists.append(row['name']['value'])

    if set(db_data) != set(voice_actor_lists):
        for row in list(set(voice_actor_lists) - set(db_data)):
            value_lists.append("('{name}')".format(name=row))

        values = ','.join(value_lists)
        sql = "INSERT INTO `voice_actors` (name) VALUE {values};".format(values=values)
        mod.insert(sql)

if __name__ == '__main__':
    main()
