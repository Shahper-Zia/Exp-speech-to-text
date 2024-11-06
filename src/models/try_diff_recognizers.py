import speech_recognition as sr

def try_all_recognizers(audio_data):
    recognizer = sr.Recognizer()
    results = {}

    # 1. Google Speech Recognition (Free)
    try:
        text = recognizer.recognize_google(audio_data)
        results['Google (Free)'] = text
    except sr.RequestError as e:
        results['Google (Free)'] = f"Error: {str(e)}"
    except sr.UnknownValueError:
        results['Google (Free)'] = "Unable to recognize speech"

    # # 2. Google Cloud Speech (Paid - Requires API Key)
    # try:
    #     text = recognizer.recognize_google_cloud(
    #         audio_data,
    #         credentials_json='your-google-cloud-credentials.json',
    #         language='en-US'
    #     )
    #     results['Google Cloud'] = text
    # except sr.RequestError as e:
    #     results['Google Cloud'] = f"Error: {str(e)}"
    # except sr.UnknownValueError:
    #     results['Google Cloud'] = "Unable to recognize speech"

    # 3. Wit.ai (Free - Requires API Key)
    try:
        text = recognizer.recognize_wit(
            audio_data,
            key="LGUJMGK64BDJUGBUDAFPEXDICAAKVX7J"
        )
        results['Wit.ai (Free)'] = text
    except sr.RequestError as e:
        results['Wit.ai (Free)'] = f"Error: {str(e)}"
    except sr.UnknownValueError:
        results['Wit.ai (Free)'] = "Unable to recognize speech"

    # # 4. Microsoft Azure (Paid - Requires API Key)
    # try:
    #     text = recognizer.recognize_azure(
    #         audio_data,
    #         key="YOUR-AZURE-KEY",
    #         location="westus",  # Azure region
    #         language="en-US"
    #     )
    #     results['Azure'] = text
    # except sr.RequestError as e:
    #     results['Azure'] = f"Error: {str(e)}"
    # except sr.UnknownValueError:
    #     results['Azure'] = "Unable to recognize speech"

    # # 5. IBM Watson (Paid - Requires API Key)
    # try:
    #     text = recognizer.recognize_ibm(
    #         audio_data,
    #         username="IBM-USERNAME",
    #         password="IBM-PASSWORD"
    #     )
    #     results['IBM Watson'] = text
    # except sr.RequestError as e:
    #     results['IBM Watson'] = f"Error: {str(e)}"
    # except sr.UnknownValueError:
    #     results['IBM Watson'] = "Unable to recognize speech"

    # 6. Sphinx (Offline)
    try:
        text = recognizer.recognize_sphinx(audio_data)
        results['Sphinx (Offline)'] = text
    except sr.RequestError as e:
        results['Sphinx (Offline)'] = f"Error: {str(e)}"
    except sr.UnknownValueError:
        results['Sphinx (Offline)'] = "Unable to recognize speech"

    # # 7. Houndify (Paid - Requires API Key)
    # try:
    #     text = recognizer.recognize_houndify(
    #         audio_data,
    #         client_id="HOUNDIFY-CLIENT-ID",
    #         client_key="HOUNDIFY-CLIENT-KEY"
    #     )
    #     results['Houndify'] = text
    # except sr.RequestError as e:
    #     results['Houndify'] = f"Error: {str(e)}"
    # except sr.UnknownValueError:
    #     results['Houndify'] = "Unable to recognize speech"

    # # 8. Amazon Transcribe (Paid - Requires AWS Credentials)
    # try:
    #     text = recognizer.recognize_amazon(
    #         audio_data,
    #         region="us-west-2",
    #         aws_access_key_id="AWS-ACCESS-KEY",
    #         aws_secret_access_key="AWS-SECRET-KEY"
    #     )
    #     results['Amazon'] = text
    # except sr.RequestError as e:
    #     results['Amazon'] = f"Error: {str(e)}"
    # except sr.UnknownValueError:
    #     results['Amazon'] = "Unable to recognize speech"

    return results

def record_and_transcribe():
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source, duration=2)
        
        print("Please speak something...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=15)
            print("Processing audio with multiple services...")
            
            results = try_all_recognizers(audio)
            
            print("\nResults from different services:")
            print("-" * 50)
            for service, result in results.items():
                print(f"{service}: {result}")
                
        except sr.WaitTimeoutError:
            print("No speech detected within timeout period")
        except Exception as e:
            print(f"An error occurred: {str(e)}")