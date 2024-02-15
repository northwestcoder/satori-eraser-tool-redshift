import sys
from collections import defaultdict

from satori import satori
from satori import satori_common
from satori import satori_locations as locations
from satori import satori_datastores as datastores
from satori import satori_remediation as remediation

#db clients
from satori import satori_query_postgres as postgres
from satori import satori_query_redshift as redshift


search_string = ''
satori_tag = ''


def search(satori_tag, search_string):

    query_items = defaultdict(list)
    satori_token = satori_common.satori_auth(
        satori.satori_serviceaccount_id, 
        satori.satori_serviceaccount_key, 
        satori.apihost)

    auth_headers = {
    'Authorization': 'Bearer {}'.format(satori_token), 
    'Content-Type': 'application/json', 'Accept': 'application/json'
    }

    found_datastores = datastores.get_all_datastores(
        auth_headers, 
        satori.apihost, 
        satori.satori_account_id)


    print("Querying all Redshift Datastores Via Satori, please wait..")

    for ds_entry in found_datastores[1]:

        ds_name = ds_entry['name']
        datastore_id = ds_entry['id']
        satori_hostname = ds_entry['satoriHostname']
        satori_displayname = ds_entry['name']
        db_type = ds_entry['type']

        
        found_locations = locations.get_locations_by_datastore(auth_headers, 
                                                               satori.apihost, 
                                                               satori.satori_account_id , 
                                                               datastore_id)
        
        for location_entry in found_locations[1]:

            #reset the search results after each location
            search_results = ['','']
            remediation_response = ''

            tags = location_entry['tags']
            if tags is not None:
                for tag_item in tags:
                    if tag_item['name'] == satori_tag:

                        # for each location of type EMAIL, we build the following vars:
                        # dbname, table, column_name, schema, query-able location, full_location

                        # Need to finish databricks, for now omitting
                        if db_type in ('DATABRICKS', 'GRAPHQL', 'API_SERVER', 'OPENSEARCH'):
                            dbname =        ''
                            table =         ''
                            column_name =   ''
                        else:
                            dbname =        location_entry['location']['db']
                            table =         location_entry['location']['table']
                            column_name =   location_entry['location']['column']
                            #some DB's don't have a concept of schema
                            if db_type in ('MARIA_DB', 'ATHENA', 'MYSQL'):
                                schema = ''
                                query_location = table
                                full_location = satori_hostname + '::' + dbname + '.' + table + '.' + column_name
                            else:
                                schema = location_entry['location']['schema']
                                query_location = schema + '.' + table
                                full_location = satori_hostname + '::' + dbname + '.' + schema + '.' + table + '.' + column_name


                        sql_query = "SELECT * from {} where {} = '{}' LIMIT {};".format(query_location, column_name, search_string, satori.LIMIT)

                        # BEGIN MAIN DB CLIENT WORK
                        
                        if db_type == 'REDSHIFT' and satori.satori_username != '':
                            #print("Search Results for: " + ds_name)

                            search_results = redshift.search_for_email(
                                satori_hostname, 
                                satori.PORT_REDSHIFT, 
                                dbname, 
                                satori.satori_username, 
                                satori.satori_password, 
                                sql_query)

                            remediation_response = remediation.build_remediation(
                                query_location, 
                                column_name, 
                                search_string
                                )

                            query_items[satori_hostname + "::" + dbname].append(search_results[1])
                        
                    
                            print("____________________________________________")
                            print("\nLOCATION:")
                            print(full_location)
                            print("\nSEARCH RESULTS:")
                            print(search_results[0])
                            print("\nREMEDIATION:")
                            print(remediation_response)

    queries_formatted = ''
    for location, queries in query_items.items():
        queries_formatted += '\n' + location.split("::")[0] + '\n'
        for item in queries:
            queries_formatted += '' + str(item) + '\n'

    print("\n\nSUMMARY OF ALL THE PREVIOUSLY RUN QUERIES:\n\n")

    print(queries_formatted)

    print("Finished querying all Satori Datastore " + satori_tag + " locations for value " + search_string)

if __name__ == '__main__':

    satori_tag = str(sys.argv[1]).upper()
    search_string = sys.argv[2] 
    search(satori_tag, search_string)
