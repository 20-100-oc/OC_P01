import csv
import json
import requests



def get_api_response_curl_version(text, api_key):
    '''
    Sends some texts to Azur API with Curl,
    get back the languages the texts are written in
    '''

    use_powershell = True   # True if using Powershell, False if using cmd
    
    curl_path = 'curl.exe'
    api_url = 'https://api.cognitive.microsofttranslator.com/detect?api-version=3.0'
    location = 'francecentral'
    
    
    line_1 = '-H "Content-Type: application/json; charset=UTF-8"'
    line_2 = '-H "Ocp-Apim-Subscription-Key: ' + api_key + '"'
    line_3 = '-H "Ocp-Apim-Subscription-Region: ' + location + '"'
    line_4 = '-d "[{\'Text\':\'' + text + '\'}]"'
    
    command = f'"{curl_path}" -X POST "{api_url}" {line_1} {line_2} {line_3} {line_4}'
    if use_powershell:
        command = '&' + command
    print(command)




def format_response(response, labels_path):

    model_to_y_test = {}

    with open(labels_path, 'r') as f:
        reader = csv.reader(f, delimiter  = ';')
        header = next(reader)
        
        for row in reader:
            model_to_y_test[row[2]] = row[0]

    guesses = []

    for res in response:
        guess = res['language']
        try:
            guess = model_to_y_test[guess]
        except:
            print('Guesse error:', guess)
        guesses.append(guess)

    return guesses




def get_api_response(text_list, api_key):
    ''' 
    Sends some text to Azure API, 
    get back the language the text is written in
    '''    

    api_url = 'https://api.cognitive.microsofttranslator.com/detect'
    location = 'francecentral'
    
    params = {'api-version': '3.0'}
    
    headers = {
        'Ocp-Apim-Subscription-Key': api_key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json; charset=UTF-8'
        }
    
    # formating the list of text
    body = [{'text': text} for text in text_list]
    
    request = requests.post(api_url, params=params, headers=headers, json=body)
    response = request.json()
    
    return response




def guess_language(text_list, api_key, labels_path):

    response = get_api_response(text_list, api_key)
    formated_response = format_response(response, labels_path)
    return formated_response




if __name__ == '__main__':

    labels_path = 'G:\OpenClassrooms\projet 1\P1_marzo_vincent\P1_01_scripts\Dataset project 1 AI Engineer\labels.csv'
    api_key = input('Enter API access key:\n')
    
    
    text = 'Bien le bonjour.'
    get_api_response_curl_version(text, api_key)
    

    text_list = [
                 'Passe-moi le thé',
                 'My tailor is rich', 
                 'Esto no es inglés'
                ]
    
    #response = get_api_response(text_list, api_key)
    #print(response, '\n')
    #formated_response = format_response(response, labels_path)
    #print(formated_response)
    
    #final_guesses = guess_language(text_list, api_key, labels_path)
    #print(final_guesses)
    
