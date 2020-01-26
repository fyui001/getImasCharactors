from SPARQLWrapper import SPARQLWrapper, JSON
from config import db_conf as db_conf
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

        SELECT ?name ?nameKana ?age ?bust ?waist ?hip ?color ?actor ?title
        WHERE {
            ?x rdfs:label ?name.
            ?x imas:nameKana ?nameKana.
            ?x foaf:age ?age.
            ?x imas:Bust ?bust.
            ?x imas:Waist ?waist.
            ?x imas:Hip ?hip.
            ?x imas:Color ?color.
            ?x imas:cv ?actor.
            ?x imas:Title ?title.
            FILTER (isLiteral(?actor)).
        }
    """)

    sql = "INSERT INTO `{table_name}` (name, nameKana, age, bust, hip, waist, color, voice_actor, title) VALUES".format(table_name=db_conf.TABLE)

    sparql.setReturnFormat(JSON)
    sparql_data = sparql.query().convert()
    imas_characters = []
    value_lists = []
    db_data = mod.get(db_conf.TABLE)
    if (len(db_data) != 0):
        mod.truncate(db_conf.TABLE)

    #insert文を作る
    for row in sparql_data['results']['bindings']:
        if row['name']['type'] == 'literal':

            if row['name']['value'] in {'双葉杏', '佐藤心'}:
                row['bust']['value'] = 0
                row['hip']['value'] = 0
                row['waist']['value'] = 0
            if row['name']['value'] == '安部菜々':
                row['age']['value'] = 17

            sql += "('{name}', '{nameKana}', {age}, {bust}, {hip}, {waist}, '{color}', '{actor}', '{title}'),".format(
                        name=row['name']['value'],
                        nameKana=row['nameKana']['value'],
                        age=row['age']['value'],
                        bust=row['bust']['value'],
                        hip=row['hip']['value'],
                        waist=row['waist']['value'],
                        color=row['color']['value'],
                        actor=row['actor']['value'],
                        title=row['title']['value']
                    )
    sql = sql.rstrip(',')
    sql += ';'
    mod.insert(sql)

    '''
        MEMO: 差分更新してやるやつを実装したほうがきれいかなぁ
        声優だけ撮ってきてた時の差分更新してるやつ
        if set(db_data) != set(imas_characters):
            for row in list(set(imas_characters) - set(db_data)):
                value_lists.append("('{name}')".format(name=row))

            values = ','.join(value_lists)
            sql = "INSERT INTO `{table_name}` (name) VALUE {values};".format(values=values, table_name=db_conf.TABLE)
            mod.insert(sql)
    '''

if __name__ == '__main__':
    main()
