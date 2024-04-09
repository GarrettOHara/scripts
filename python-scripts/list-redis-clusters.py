import boto3
import json

regions = ["us-east-1", "us-east-2", "us-west-1", "us-west-2"]
profiles = ["se-prod", "se-staging"]

config = {
    "se-prod": [],
    "se-staging": [],
}
domains = []

for profile in profiles:
    print(f"{profile} account")
    for region in regions:
        session = boto3.Session(profile_name=profile, region_name=region)
        client = session.client("es")
        print(f"{region} region")

        response = client.list_domain_names(EngineType="OpenSearch")["DomainNames"]
        print(json.dumps(response, indent=4, default=str))
        if len(response) > 0:
            print("PRINTING ITEMS")
            for item in response:
                print(item)
                domains.append(item["DomainName"])

        response = client.list_domain_names(EngineType="Elasticsearch")["DomainNames"]
        print(json.dumps(response, indent=4, default=str))
        if len(response) > 0:
            print("PRINTING ITEMS")
            for item in response:
                print(item)
                domains.append(item["DomainName"])

        print("LIST:")
        print(domains)
        print("\n\n")
        config[profile].append(domains[:])
        domains.clear()

print(config)
for key, value in config.items():
    print(key + ":\n")
    filename = f"{key}.txt"

    f = open(filename, "w")
    for item in value:
        for i in item:
            print(i)
            f.write(i + "\n")
    f.close()
