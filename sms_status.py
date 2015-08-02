'''
Sends a status sms message when pipeline completes.
Uses sinch sms to send messages
https://www.sinch.com/tutorials/sending-sms-python/
Requires number to send to and sinch account key  and secret.
'''
import yaml
import os
import time
from sinchsms import SinchSMS


def main(sms_config, message='PEPR pipeline complete'):
    assert os.path.isfile(sms_config['config_file']), "SMS config file not present"
    sinch_config_file = file(sms_config['config_file'], 'r')
    sinch_params = yaml.load(sinch_config_file)

    assert sinch_params
    assert sinch_params['app_key']
    assert sinch_params['app_secret']
    app_key = sinch_params['app_key']
    app_secret = sinch_params['app_secret']

    assert sms_config['number']
    number = sms_config['number']

    client = SinchSMS(app_key, app_secret)
    assert client

    print("Sending '%s' to %s" % (message, number))
    response = client.send_message(number, message)
    message_id = response['messageId']

    check_response = client.check_status(message_id)
    while check_response['status'] != 'Successful':
        print check_response['status']
        time.sleep(1)
        check_response = client.check_status(message_id)

    print check_response['status']
