#!/usr/bin/env python
#
# A tool I use to mange DNS at AWS
#

import sys, argparse, boto3, json

prog='awsdns'
version='0.1'
author='Al Biheiri (al@forgottheaddress.com)'

client = boto3.client('route53')


# Method for retrieving the entire domains/zones you have permission on
def get_domains():
    # type=dict
    fetched_domain = client.list_hosted_zones()
    # print(type(fetched_domain))

    #Filter HTTP response and show only hosted zones (dict to list conversion)
    global filtered_zone_list
    filtered_zone_list = fetched_domain["HostedZones"]


# Method for dumping out the domain/zone list in a pretty format
def list_domains():
    get_domains()

    domain_list = json.dumps(filtered_zone_list, indent=4, sort_keys=True)
    print(domain_list)


# Method for filtering and targeting a specific domain/zone, based on users args
def selected_zone_id(domain):
    # find the 'Id:' and parse from get_domains()
    #
    # "Id": "/hostedzone/Z05828351X4Y2J14RF6S5",
    # "Name": "forgotthe.name.",
    #
    # Search for the domain and extract value of Id from the filtered_zone_list
    for item in filtered_zone_list:
        if item.get('Name') == f'{domain}.':
            val = item.get('Id')
            # print(val.replace("/hostedzone/",""))
            global my_zone_id
            # strip the value ie: "/hostedzone/Z05828351X4Y2J14RF6S5"
            my_zone_id = val.replace("/hostedzone/","")



# Method for displaying all records associated to a specific domain/zone
def do_get(domain):
    
    get_domains()
    
    # pass argparse result from do_get(domain) to the function
    selected_zone_id(domain)
            
    # Listing a specific zone - (aws route53 get-hosted-zone --id Z067920437CH29MWAVKLI)
    #zone_picked = client.get_hosted_zone (Id='Z05828351X4Y2J14RF6S5')
    #results_formatted = json.dumps(zone_picked, indent=4, sort_keys=True)
    #print (results_formatted)

    # Listing all records in a zone (aws route53 list-resource-record-sets --hosted-zone-id Z067920437CH29MWAVKLI)
    collected_records = client.list_resource_record_sets(HostedZoneId = my_zone_id)
    records_formatted = json.dumps(collected_records, indent=4, sort_keys=True)
    print (records_formatted)



def do_add(domain, record, name, value, ttl):
    get_domains()

    # pass argparse result from do_get(domain) to the function
    selected_zone_id(domain)


    print ("Zone Name: ", domain)
    print ("Zone Id: ", my_zone_id)

    client.change_resource_record_sets(
        HostedZoneId=my_zone_id,
        ChangeBatch={
            'Comment': 'Changed by: awdns.py',
            'Changes': [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': name,
                        'Type': record,
                        'TTL': ttl,
                        'ResourceRecords': [{ "Value": value}]
                    }
                },
            ]
        }
    )



parser = argparse.ArgumentParser()

parser.add_argument('--version', action='version', version='{} {}'.format(prog, version))

group = parser.add_mutually_exclusive_group()
group.add_argument("-ls", dest="ls", action="store_true", help="list domain you own")
group.add_argument("-g", dest="get", metavar='get', help="get all records from a domain")
group.add_argument("-a", dest="add", metavar="add", help="add to domain")
group.add_argument("-r", dest="replace", metavar="replace", help="replce record in a domain")
group.add_argument("-d", dest="delete", metavar="delete", help="delete record a domain")


parser.add_argument("-rt", dest="record", metavar="record type", choices=['A','AAAA','CNAME','TXT','MX','SRV','SOA','NS'], help="A,AAAA,CNAME,TXT,MX,SRV,SOA,NS")
parser.add_argument("-n", dest="name", metavar="name", help="the dns record name")
parser.add_argument("-v", dest="value", metavar="value", help="the value of the dns record (ie. ip address)")
parser.add_argument('--ttl', type=int, default=3600, help='default is 3600 if this argument is not supplied')

args = parser.parse_args()


# TODO: intelligent checking of acceptable arg passing

if args.ls:
    list_domains()

elif args.get:
    do_get(args.get)
    # print (len(sys.argv))

elif args.add:
    do_add(args.add, args.record, args.name, args.value, args.ttl)

else:
    print("nothing")
