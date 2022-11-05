# fifteythree

A tool to manage DNS records in AWS Route 53

## Requirements

* Python v3+
* [AWS SDK](https://aws.amazon.com/tools/) (specifically the boto3 
library)

On MacOS, you can use the brew package manager :  

    # Isolate your python environment with pipenv
    brew install pipenv

    # Drop into a isolated environment
    pipenv shell

    # Install AWS SDK
    pipenv install boto3

Youll also need your AWS credentials configured. Make sure your `~/.aws/credentials` file in Unix looks like this:

```
[MyProfile1]
aws_access_key_id = yourAccessId
aws_secret_access_key = yourSecretKey

[MyProfile2]
aws_access_key_id = yourAccessId
aws_secret_access_key = yourSecretKey
```
or use `aws configure` command from https://aws.amazon.com/cli/

## Example Usage

    usage: awsdns.py [-h] [--version]
                    [-ls | -g get | -a add | -r replace | -d delete | --author]
                    [--debug] [-rt record type] [-n name] [-v value] [--ttl TTL]

    optional arguments:
    -h, --help       show this help message and exit
    --version        show program's version number and exit
    -ls              list domain you own
    -g get           get all records from a domain
    -a add           add to domain
    -r replace       replace record in a domain
    -d delete        delete record a domain
    --author         print developer info
    --debug          used in tandem with -ls to print more
    -rt record type  A,AAAA,CNAME,TXT,MX,SRV,SOA,NS
    -n name          the dns record name
    -v value         the value of the dns record (ie. ip address)
    --ttl TTL        default is 3600 if this argument is not supplied

    Deleting a record requires exact values for: -rt -n -v --ttl. If any of these
    are not correct values, it will fail to delete. You can use "get" arguments to
    get all the values before attempting to delete.


## List all zones

    awsdns.py -ls

## List all records in a zone

    awsdns.py -g forgottheaddress.com

## Add a record

    # Add to forgotthe.name zone, and 'A' record w/name myhost01
    # ttl is seconds
    ./awsdns.py -a forgotthe.name -rt A -n myhost01 -v 192.168.0.1 --ttl 300

## Delete a record

    # All these flags are required as you have to match what exists in DNS
    awsdns.py -d forgotthe.name -rt A -n myhost01 -v 192.168.0.1 --ttl 300

### Limitations

Regions are not supported, instead they are automatically inherited from your aws config file.