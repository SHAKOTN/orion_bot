def parse_slack_output(slack_rtm_output):

    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:

        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                user_id = output["user"]
                user = slack_client.api_call(
                    'users.info',
                    user=user_id
                )
                username = user['user']['name']
                return (
                    output['text'].split(AT_BOT)[1].strip().lower(),
                    output['channel'],
                    username
                )
    return None, None, None