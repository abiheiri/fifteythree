#!/usr/bin/env python
#
# A tool I use to mange DNS at AWS
#

import argparse, boto3, json

prog='awsdns'
version='0.1'
author='Al Biheiri (al@forgottheaddress.com)'


def list_domains():
    client = boto3.client('route53')

    response = client.list_hosted_zones(
        # Marker='string',
        # MaxItems='string',
        # DelegationSetId='string'
    )

    result = json.dumps(response, indent=4, sort_keys=True)
    print(result)




parser = argparse.ArgumentParser()



parser.add_argument('--version', action='version', version='{} {}'.format(prog, version))

group = parser.add_mutually_exclusive_group()
group.add_argument("-g", dest="get", metavar='get', help="get all records from a domain")
group.add_argument("-a", dest="add", metavar="add", help="add to domain")
group.add_argument("-r", dest="replace", metavar="replace", help="replce record in a domain")
group.add_argument("-d", dest="delete", metavar="delete", help="delete record a domain")
group.add_argument("-ls", dest="ls", action="store_true", help="list domain you own")

# parser.add_argument("-rt", dest="record", metavar="record type", choices=['A','AAAA','CNAME','TXT','MX','SRV','SOA','NS'], help="A,AAAA,CNAME,TXT,MX,SRV,SOA,NS")
# parser.add_argument("-n", dest="name", metavar="name", help="the dns record name")
# parser.add_argument("-v", dest="value", metavar="value", help="the value of the dns record (ie. ip address)")
# parser.add_argument('--ttl', type=int, default=3600, help='default is 3600 if this argument is not supplied')

args = parser.parse_args()

if args.ls:
    list_domains()

# elif args.add:
    
#     #Checking that you passed min req
#     if len(sys.argv) >= 9:
#         do_add(args.add, args.record, args.name, args.value, args.ttl)
#     else:
#         print("Arguments missing")

# elif args.replace:
#     print("not implemented yet") 
#     # #Checking that you passed min req
#     # if len(sys.argv) >= 9:
#     #     do_replace(args.replace, args.record, args.name, args.value, args.ttl)
#     # else:
#     #     print("Arguments missing")

# elif args.delete:
#     print("not implemented yet") 

# else:
#     print("You dont know what you are doing. Try using the -h flag")


