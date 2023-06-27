# run server.py first
# this file is the example for the retry mechanism with asana plugin.
# enter the access_token when your plugin is using the oauth authentication.

import guidance

guidance.llm = guidance.llms.OpenAI("gpt-4", token="openai_api_key")
import plugnplai


def send_single_user_request(system_prompt, user_message):
    send_single_user_request = guidance(
        '''
        {{#system~}}
        {{system_prompt}}
        {{~/system}}

        {{#user~}}
        {{user_message}}
        {{~/user}}

        {{#assistant~}}
        {{gen 'assistant_response' temperature=0 max_tokens=300}}
        {{~/assistant}}'''
    )
    return send_single_user_request(system_prompt=system_prompt, user_message=user_message)


def api_return_message(user_message, llm_first_response, api_response):
    create_api_return_message = guidance(
        '''
        {{#user~}}
        {{user_message}}
        {{~/user}}

        {{#system~}}
        Assistant is a large language model with access to plugins.

        Assistant called a plugin in response to previous user message.
        # API REQUEST SUMMARY
        {{llm_first_response}}

        # API RESPONSE
        {{api_response}}
        {{~/system}}

        {{#assistant~}}
        {{gen 'assistant_response' temperature=0 max_tokens=300}}
        {{~/assistant}}'''
    )
    return create_api_return_message(
        user_message=user_message, llm_first_response=llm_first_response, api_response=api_response
    )


if __name__ == '__main__':

    user_inputs_query = "Create a task in Asana with the title 'Prepare presentation' and due date '2023-05-25' in workspace id 1"
    # Use the correct URL
    url_of_plugin_to_test = "https://app.asana.com"

    api_key = input("input your api key: ")

    print('\n----\n1 -> Entered Process\n')

    urls = [url_of_plugin_to_test]
    # urls.append(url_of_plugin_to_test)
    plugins = plugnplai.Plugins.install_and_activate(urls)

    print('\n----\n2 -> Plugin Prompt\n')

    print(plugins.prompt)

    print('\n----\n3 -> User Query\n')
    user_first_message = user_inputs_query
    print(user_first_message)

    assistant_first_response = send_single_user_request(system_prompt=plugins.prompt, user_message=user_first_message)

    llm_first_response = assistant_first_response['assistant_response']

    print('\n----\n4 -> Assistant First Response\n')
    print(llm_first_response)

    print('\n----\n5 -> API Call Dict\n')
    call_dict = plugnplai.parse_llm_response(llm_first_response)
    print(call_dict)


    # pass the access_token as api_key incase of the oauth technique.
    api_response = plugins.call_api(
        plugin_name=call_dict['plugin_name'], operation_id=call_dict['operation_id'], parameters=call_dict['parameters'],
        url=url_of_plugin_to_test,
        api_key=api_key
    )

    # ---------------------------------RETRY MECHANISM-----------------------------------------------------#
    # retry mechanism when access_token is expired.
    if "token has expired" in response.text:

        # ------------------------------REPLACE WITH ORIGINAL VALUES---------------------------------------#
        client_id = "client_id"
        client_secret = "client_secret"
        req_url = "authorization_token_url"
        refresh_token = "refresh_token"

        # make a request to a sever ( to a authorization_url ) with a grant type as a refresh_token.
        try:
            res = requests.post(req_url, params={"client_id":client_id, "client_secret":client_secret, "refresh_token":refresh_token, "grant_type": "refresh_token"})
        except Exception as e:
            print(f"something went wrong {e}")
            return "Something went wrong please relogin"
        token_obj = res.json()
        print(token_obj)
        api_key = token_obj["access_token"]
        api_response = plugins.call_api(
            plugin_name=call_dict['plugin_name'], operation_id=call_dict['operation_id'], parameters=call_dict['parameters'],
            url=url_of_plugin_to_test,
            api_key=api_key
        )
        

    print('\n----\n6 -> API Response\n')
    print(api_response)
