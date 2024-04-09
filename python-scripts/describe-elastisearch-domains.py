import boto3

regions = ["us-east-1", "us-east-2", "us-west-1", "us-west-2"]
profiles = ["se-prod", "se-staging"]
domain_list = []

# Strip all the lines in the elastisearch domain file
for profile in profiles:
    with open(f"{profile}.txt") as file:
        domain_list = [line.rstrip() for line in file]

    # list domains
    print(f"\n\n\n\n\nWe are now searching {profile}")
    for region in regions:
        session = boto3.Session(profile_name=profile, region_name=region)
        client = session.client("es")
        print(f"{region} region")

        for domain in domain_list:
            response = client.describe_elasticsearch_domains(DomainNames=[domain])[
                "DomainStatusList"
            ]
            if len(response) > 0:
                response = response[0]
                print(response["DomainName"])
                print(response["ARN"])
                if "Endpoint" in response:
                    print(response["Endpoint"])
                if "Endpoints" in response:
                    print(response["Endpoints"]["vpc"])
                print("\n")

            else:
                print(f"No clusters in {region} in account {profile}")
        print("\n")
    print("\n\n")
