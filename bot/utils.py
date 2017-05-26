from settings import AT_BOT


def parse_slack_output(slack_client, slack_rtm_output):
    text_parser = (
        lambda out:
        out['text'].split(AT_BOT)[1].strip().lower()
    )

    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:

        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                user_id = output["user"]
                username = slack_client.get_user_name(
                    user_id
                )
                return (
                    text_parser(output),
                    output['channel'],
                    username
                )
    return None, None, None


def command_handler():
    pass