# Snips-Translate from German to another languages
This skill makes [Snips.ai](https://snips.ai/) translate you german text into. 
You need a azure key from Microsoft for TextTranslation from [Azures](https://portal.azure.com).
You find the textTranslation in Cognitive Services

## Installation
**Important:** The following instructions assume that [Snips](https://snips.gitbook.io/documentation/snips-basics) is
already configured and running on your device. [SAM](https://snips.gitbook.io/getting-started/installation) should
also already be set up and connected to your device and your account.

1. In the German [skill store](https://console.snips.ai/) add the
skill `Translate` (by mcitar; [this]()) to your *German* assistant.

2. Go to Google sign in or up and get your self an api key for text to speech translations https://cloud.google.com/docs/authentication/api-keys#creating_an_api_key

3. Go to the [Azures](https://portal.azure.com) website and create an account or if you already have one.

3. In "Alle Dienste" go to the section "KI Machinelearning" and add a new key.

4. In the console execute the following command:
    ```bash
    sam install assistant
    ```
    You will be asked to enter your azure key:
    - `azure_key`
        Here you (copy and) paste the key you generated before.
    This data is stored on your device.
    
5. To update the values simply run
    ```bash
    sam install skills
    ```
    
6. enter your azure key and google key if you get asked for it (you can update this later in the config.ini files).
 
### Example sentences
- *hey snips, bitte übersetzen [ein Wort] auf Franzözisch*

## Todo
- this is not yet working... WIP
