# Snips-Translate from German to another languages
This skill makes [Snips.ai](https://snips.ai/) translate you german text into. 
You need a azure key from Microsoft for TextTranslation from [Azures](https://portal.azure.com).
You find the textTranslation in Cognitive Services

## Installation
**Important:** The following instructions assume that [Snips](https://snips.gitbook.io/documentation/snips-basics) is
already configured and running on your device. [SAM](https://snips.gitbook.io/getting-started/installation) should
also already be set up and connected to your device and your account.

1. to be able to hear the translated texts you need to:
    ```bash
    install sudo apt-get install mpg321
    ```
2. Go to Google sign in or up and get your self an api key for text to speech translations https://cloud.google.com/docs/authentication/api-keys#creating_an_api_key

3. Go to the [Azures](https://portal.azure.com) website and create an account or if you already have one.

    3. Go to "Alle Dienste" go to the section "KI Machinelearning" and add a new key.

4. In Snips' German [skill store](https://console.snips.ai/) add the
skill `Translate` (by mcitar; [this]()) to your *German* assistant.

5. Now you can install the skill with sam in your console
    ```bash
    sam install assistant [your project id]
    ```
6. During the installation qou will be asked to enter your azure and google key:
    - `azure_key` enter your azures key
    - `google_wavenet_key` enter your google key
    - `translator_voice_gender` (enter FEMALE OR MALE, notice not all languages have a mal voice )
    This data is stored on your device only. If you missed it you can change the values in the /var/lib/snips/skills/snips-skill-translate/config.ini file
    
7. Sometimes snipes gives you a permission error, if that happens just follow SAM's hint.
    ```bash
    chmod +x /var/lib/snips/skills/snips-skill-translate/action-translate.py
    sudo systemctl restart snips-skill-server
    ```
    
8. To update the values simply run
    ```bash
    sam install skills
    ```
    if the skill doens't get updated delete the skill first with
    
    ```bash
    sudo rm -rf /var/lin/snips/skills/snips-skill-translate/
    ```
   
 
### Example sentences
- *hey snips, bitte übersetzen [ein Wort] auf Franzözisch*
- *hey snips, übersetzen auf Norwegisch*
- *hey snips, übersetzen auf Englisch*
- *hey snips, übersetzen*


## Todo
- this is "work in process" some languages don't work like russian and ukrain. 
possible language should be:
Australisch
Amerikanisch
Belgisch
Dänisch
Französisch
Englisch
Italienisch
Japanisch
Koreanisch
Niederländisch
Norwegisch
Brasilianisch
Portugiesisch
Polnisch
Russisch
Slowakisch
Schwedisch
Spanisch
Türkisch
Ukrainisch
