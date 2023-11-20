""" Imports """
from botocore.vendored import requests
from rds import rds_client as rds

def send_slack_message(msg, slack_webook_path="/lambda/db-reloads-slack-webook"):
    """
    Send notifications programmatically to Slack.

    Parameters
    ----------
    msg: string
        Message to be sent in Slack channel. Markdown supported, refer to
        Slack formatting link: https://api.slack.com/reference/surfaces/formatting

    Returns
    -------
    int
        The status code of the request.
    """
    try:
        ssm_client = rds.instantiate_boto3_client(client_type="ssm")
        slack_webook_object   = ssm_client.get_parameter(Name=slack_webook_path, WithDecryption=True)
        slack_webook_url      = slack_webook_object["Parameter"]["Value"]
        res = requests.post(
            slack_webook_url,
            json={"text": str(msg)},
            headers={"Content-Type": "application/json"}
        )

        res.raise_for_status()
    except requests.exceptions.HTTPError as error:
        print(f"Request Error, message not delivered:\n{error}")
    except requests.exceptions.ConnectionError as error:
        print(f"Error Connecting:\n{error}")
    except requests.exceptions.Timeout:
        # Maybe set up for a retry, or continue in a retry loop
        print(f"Request Timeout:\n{error}")
    except requests.exceptions.RequestException as error:
        print(f"Bad Request to Slack:\n{error}")
        raise

    print(f"Response:\n{res.status_code}\n{res.text}")
    return res.status_code

if __name__ == "__main__":
    send_slack_message("test")
