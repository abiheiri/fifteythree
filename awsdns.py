#!/usr/bin/env python
#
# A tool I use to mange DNS at AWS
#

import sys, argparse, boto3, json

prog='awsdns'
version='0.5'
author='Al Biheiri (al@forgottheaddress.com): الحارث بحيري'

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
def list_domains(debug):
    get_domains()

    if debug:
        domain_list = json.dumps(filtered_zone_list, indent=4, sort_keys=True)
        print(domain_list)
    else:
        for item in filtered_zone_list:
            print (item.get('Name'))


# Method for filtering and targeting a specific domain/zone, based on users args
def selected_zone_id(domain):

    # Listing a specific zone - (aws route53 get-hosted-zone --id Z067920437CH29MWAVKLI)
    #zone_picked = client.get_hosted_zone (Id='Z05828351X4Y2J14RF6S5')
    #results_formatted = json.dumps(zone_picked, indent=4, sort_keys=True)
    #print (results_formatted)

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
def do_get(domain, record, name):
    
    get_domains()
    
    # pass argparse result from do_get(domain) to the function
    selected_zone_id(domain)

    #        
    # If there is a record_type and a name
    #
    if record is not None and name is not None:
        # print ("You typed both a record_type and name: ", record, name, domain)
        collected_records = client.list_resource_record_sets(
            HostedZoneId = my_zone_id,
            StartRecordName=f'{name}.{domain}',
            StartRecordType=record,
            )
        records_formatted = json.dumps(collected_records, indent=4, sort_keys=True)
        print (records_formatted)

    #        
    # elseIf there is a record_type only
    #    
    elif record is not None:
        # print ("You typed only a record_type: ", record)
        collected_records = client.list_resource_record_sets(
            HostedZoneId = my_zone_id,
            StartRecordName='*',
            StartRecordType=record,
            )
        records_formatted = json.dumps(collected_records, indent=4, sort_keys=True)
        print (records_formatted)

    else:
        # Listing all records in a zone (aws route53 list-resource-record-sets --hosted-zone-id Z067920437CH29MWAVKLI)
        collected_records = client.list_resource_record_sets(HostedZoneId = my_zone_id)
        records_formatted = json.dumps(collected_records, indent=4, sort_keys=True)
        print (records_formatted)



def do_add(domain, record, name, value, ttl):
    get_domains()

    # pass argparse result from do_get(domain) to the function
    selected_zone_id(domain)


    print ("Zone Name: ", domain)
    print ("Zone Id: g", my_zone_id)

    trigger = client.change_resource_record_sets(
        HostedZoneId=my_zone_id,
        ChangeBatch={
            'Comment': 'Changed by: awdns.py',
            'Changes': [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': f'{name}.{domain}',
                        'Type': record,
                        'TTL': ttl,
                        'ResourceRecords': [{ "Value": value}]
                    }
                },
            ]
        }
    )
    print(trigger)


def do_delete(domain, record, name, value, ttl):
    get_domains()

    # pass argparse result from do_get(domain) to the function
    selected_zone_id(domain)


    print ("Zone Name: ", domain)
    print ("Zone Id: g", my_zone_id)

    trigger = client.change_resource_record_sets(
        HostedZoneId=my_zone_id,
        ChangeBatch={
            'Comment': 'Deleted by: awdns.py',
            'Changes': [
                {
                    'Action': 'DELETE',
                    'ResourceRecordSet': {
                        'Name': f'{name}.{domain}',
                        'Type': record,
                        'TTL': ttl,
                        'ResourceRecords': [{ "Value": value}]
                    }
                },
            ]
        }
    )
    print(trigger)


def parse_args(args):
    parser = argparse.ArgumentParser(
        epilog='''
        Deleting a record requires exact values for: -rt -n -v --ttl. If any of these are not correct values, it will fail to delete.
        You can use "get" arguments to get all the values before attempting to delete.
        '''
    )

    parser.add_argument('--version', action='version', version='{} {}'.format(prog, version))

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-ls", dest="ls", action="store_true", help="list domain you own")
    

    group.add_argument("-g", dest="get", metavar='get', help="get all records from a domain")
    group.add_argument("-a", dest="add", metavar="add", help="add to domain")
    group.add_argument("-r", dest="replace", metavar="replace", help="replace record in a domain")
    group.add_argument("-d", dest="delete", metavar="delete", help="delete record a domain")
    group.add_argument("--author", dest="author", action="store_true", help="print developer info")

    parser.add_argument("--debug", dest="debug", default=None, action="store_true", help="used in tandem with -ls to print more")
    parser.add_argument("-rt", dest="record", default=None, metavar="record type", choices=['A','AAAA','CNAME','TXT','MX','SRV','SOA','NS'], help="A,AAAA,CNAME,TXT,MX,SRV,SOA,NS")
    parser.add_argument("-n", dest="name", default=None, metavar="name", help="the dns record name")
    parser.add_argument("-v", dest="value", metavar="value", help="the value of the dns record (ie. ip address)")
    parser.add_argument('--ttl', type=int, default=3600, help='default is 3600 if this argument is not supplied')
    

    args = parser.parse_args()



    if args.ls:
        list_domains(args.debug)

    elif args.get:
        do_get(args.get, args.record, args.name)

    # Add or Replace a record run the same function
    elif args.add or args.replace:
        do_add(args.add, args.record, args.name, args.value, args.ttl)

    elif args.delete:
        do_delete(args.delete, args.record, args.name, args.value, args.ttl)

    elif args.author:
        print (author)

    else:
        print("run ", sys.argv[0], "-h" )


if __name__ == "__main__":
    parse_args(sys.argv[1:])
