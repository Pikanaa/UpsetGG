import re
import json
import sys
from graphqlclient import GraphQLClient
from operator import itemgetter

##ENTER YOUR API KEY HERE
authToken = 'YOUR_API_KEY'

if(authToken == 'YOUR_API_KEY'):
    authToken = input('Paste your api key or add your smash.gg API key in the .py file if you don\'t want to bother with it everytime.\n')

class HorsIntervalle(Exception):
    pass

page = 1
perPage = 100
apiVersion = 'alpha'
liste = []
placements = []

client = GraphQLClient('https://api.smash.gg/gql/' + apiVersion)
client.inject_token('Bearer ' + authToken)

tournament = input("Tournament? (part between smash.gg/tournament/ and the following /)\n")
query = '''
    query tournaments($slug: String) {
        tournament(slug:$slug) {
            events{
                id
                name
                videogame {
                    id
                    name
                }
                phases{
                    seeds(query: {
                        perPage: 100
                    }) {
                        pageInfo{
                            totalPages
                        }
                    }
                }
            }
        }
    }
'''
var = dict(
{
    "slug":tournament
})

try:
    result = client.execute(query,var)
except Exception:
    input('Cannot connect to smash.gg, make sure your internet connection is working or that your API key is correct.')
    exit()
resData = json.loads(result)

i = 1
if(resData['data']['tournament'] == None):
    input("Tournament not recognized, try again")
    exit()
    
print("\nEvents:")
for event in resData['data']['tournament']['events']:
    print(str(i) + "- " + event['name'] + " | " + event['videogame']['name'])
    i+=1

event = 0
while True:
    try:
        event = int(input("\nWhich event are you interested in?\n"))
        if (event < 1) or (event >= i):
            raise HorsIntervalle
        break
    except (HorsIntervalle, ValueError):
        print("Enter the id of the event you're interested in using the list above.")

id = resData['data']['tournament']['events'][event-1]['id']
nbPages = 1
for phase in resData['data']['tournament']['events'][event-1]['phases']:
    if phase['seeds']['pageInfo']['totalPages'] > nbPages:
        nbPages = phase['seeds']['pageInfo']['totalPages']

print("Retrieving data... (this might take a while based on the number of participants)")

for page in range(1,nbPages+1):
    query = '''
        query seeds($id: ID, $page: Int, $perPage: Int) {
            event(id:$id) {
                standings(query: {
                    perPage: $perPage,
                    page: $page
                }){
                    nodes{
                        placement
                        entrant{
                            name
                            seeds{
                                phase{
                                    phaseOrder
                                }
                                seedNum
                            }
                        }
                    }
                }
            }
        }
    '''
    var = dict(
    {
        "id":id,
        "page": page,
        "perPage": perPage
    })

    result = client.execute(query,var)
    resData = json.loads(result)

    if 'errors' in resData:
        print('Error:')
        print(resData['errors'])
    else:
        for player in resData['data']['event']['standings']['nodes']:
            name = player['entrant']['name']
            placement = player['placement']
            i = 0
            while player['entrant']['seeds'][i]['phase']['phaseOrder'] != 1:
                i+=1
            seed = player['entrant']['seeds'][i]['seedNum']
            liste.append([name,seed,placement,0])

for entry in liste:
    if entry[2] not in placements:
        placements.append(entry[2])

for entry in liste:
    i = 0
    while i < len(placements) and placements[i] <= entry[1]:
        i += 1
    expected = i-1
    actual = placements.index(entry[2])
    entry[3] = expected-actual

liste = sorted(liste,key=itemgetter(2,1))
liste = sorted(liste,key=itemgetter(3),reverse=True)
print("\nName\tSeed".expandtabs(30),"\tResult\tPerf")
for entry in liste:
    sign = ''
    if(entry[3]>0):
        sign = '+'
    elif(entry[3]==0):
        sign = '±'
    print((entry[0]+'\t'+str(entry[1])).expandtabs(30),'\t'+str(entry[2])+'\t'+sign+str(entry[3]))

input("\nPress ENTER to leave the program.")
