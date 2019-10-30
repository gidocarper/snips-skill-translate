#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, requests, json, base64
import datetime
import random
from hermes_python.hermes import Hermes, MqttOptions


class Translator:
    def __init__(self, config):
        self.text_to_translate = None
        self.language = None
        try:
            self.azure_translate_key = config['secret']['azure_key']
        except KeyError:
            self.azure_translate_key = "XXXXXXXXXXXXXXXXXXXXX"
        try:
            self.google_wavenet_key = config['secret']['google_wavenet_key']
        except KeyError:
            self.google_wavenet_key = "XXXXXXXXXXXXXXXXXXXXX"
        try:
            self.translator_voice_gender = config['secret']['translator_voice_gender']
        except KeyError:
            self.translator_voice_gender = "FEMALE"


    def translate(self, hermes, intent_message):
        if intent_message.slots.wordToTranslate:
            self.text_to_translate = intent_message.slots.wordToTranslate.first().value

        if intent_message.slots.TranslateToLanguage:
            self.language = str(intent_message.slots.TranslateToLanguage.first().value)


        body = [{ 'text': str(self.text_to_translate) }]


        token_url = 'https://api.cognitive.microsoft.com/sts/v1.0/issueToken'
        token_body = json.dumps('{body}')
        token_headers = {
            'Content-Type': 'application/json',
            'Content-Length': str(len(token_body)),
            'Ocp-Apim-Subscription-Key': self.azure_translate_key
        }
        request = requests.post(token_url, headers=token_headers, json=token_body)

        accessToken = (request.content).decode('ascii')
        toLanguage = self.get_language_code()
        fromLanguage = 'de'

        params = u'text={}&to={}&from={}&appId=Bearer+{}'.format(str(self.text_to_translate), str(toLanguage), str(fromLanguage),
                                                                 str(accessToken))
        translateUrl = u'http://api.microsofttranslator.com/v2/Http.svc/Translate?{}'.format(str(params))

        headers = {
            'Content-type': 'application/json'
        }
        request = requests.get(translateUrl, headers=headers, json=body)

        # this sucks has anybody a better idea?
        rawTranslation = (request.content).decode('ascii')
        translation = rawTranslation.replace('<string xmlns="http://schemas.microsoft.com/2003/10/Serialization/">',
                                             '')
        translation = translation.replace('</string>', '')

        if self.google_wavenet_key:
            return self.text_to_speech(translation)
        else:
            return translation


    def text_to_speech(self, translation):
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
        }

        language = self.get_language_code()
        country = self.get_country_code()

        data = '{\'input\':{\'text\':\'' + translation + '.\'},\'voice\':{\'languageCode\':\'' + language + '-' + language + '\',\'name\':\'' + language + '-' + country + '-Wavenet-A\',\'ssmlGender\':\'' + self.translator_voice_gender + '\'},\'audioConfig\':{\'audioEncoding\':\'MP3\'}}'
        print(data);
        response = requests.post('https://texttospeech.googleapis.com/v1/text:synthesize?key=' + self.google_wavenet_key, headers=headers, data=data)
        file_content = base64.b64decode(json.loads(response.text)['audioContent'])
        filemp3 = open("resp_text.mp3", "wb")
        filemp3.write(file_content)
        filemp3.close()


    def get_language_code(self):
        switcher = {
            'Australisch': 'en',
            'Amerikanisch': 'en',
            'Belgisch': 'be',
            'Britisch': 'en',
            'Dänisch': 'da',
            'Französisch': 'fr',
            'Englisch': 'en',
            'Italienisch': 'it',
            'Japanisch': 'ja',
            'Koreanisch': 'ko',
            'Niederländisch': 'nl',
            'Norwegisch': 'nb',
            'Brasilianisch': 'pt',
            'Portugiesisch': 'pt',
            'Polnisch': 'pl',
            'Russisch': 'ru',
            'Slowakisch': 'sk',
            'Schwedisch': 'sv',
            'Spanisch': 'es',
            'Türkisch': 'tr',
            'Ukrainisch': 'uk'
        }
        return switcher.get(self.language, "fr")

    def get_country_code(self):
        switcher = {
            'Australisch': 'AU',
            'Amerikanisch': 'US',
            'Belgisch': 'BE',
            'Britisch': 'GB',
            'Dänisch': 'DK',
            'Englisch': 'GB',
            'Französisch': 'FR',
            'Italienisch ': 'IT',
            'Japanisch': 'JP',
            'Koreanisch': 'KR',
            'Niederländisch': 'NL',
            'Norwegisch': 'NO',
            'Brasilianisch': 'BR',
            'Portugiesisch': 'PT',
            'Polnisch': 'PL',
            'Russisch': 'RU',
            'Slowakisch': 'SK',
            'Schwedisch': 'SE',
            'Spanisch': 'ES',
            'Türkisch': 'TR',
            'Ukrainisch': 'UA'
        }
        return switcher.get(self.language, "fr")



    def error_response(self, data):
        response = random.choice(["Es ist leider kein Internet verfügbar.",
                                  "Ich bin nicht mit dem Internet verbunden.",
                                  "Es ist kein Internet vorhanden.",
                                  "Leider ist ein Fehler aufgetreten"])

        return response
