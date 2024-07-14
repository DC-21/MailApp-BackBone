import time
import speech_recognition as sr
import pyttsx3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Function to recognize speech input from microphone
def recognize_speech_from_mic():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print(f"Recognized: {text}")
        return text
    except sr.RequestError:
        print("API was unreachable or unresponsive")
        return None
    except sr.UnknownValueError:
        print("Unable to recognize speech")
        return None

# Function to speak text output
def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Function to automate browser actions using Selenium
def automate_browser(url):
    speak_text("The Mail App is opening in chrome browser.")
    driver = webdriver.Chrome()
    driver.get(url)
    return driver

# Function to handle form interaction based on voice commands
def handle_form_interaction(driver):
    speak_text("Please spell out your email address.")
    email = get_spell_input()
    if email:
        try:

            password_field = driver.find_element(By.CSS_SELECTOR, "#email[type='email']")
            password_field.send_keys(email)
        except Exception as e:
            print(f"Error: {e}")
            speak_text("Error encountered while typing email.")

    speak_text("Please spell out your password.")
    password = get_spell_input()
    if password:
        try:
            password_field = driver.find_element(By.CSS_SELECTOR, "#password[type='password']")
            password_field.send_keys(password)
        except Exception as e:
            print(f"Error: {e}")
            speak_text("Error encountered while typing password.")

    speak_text("Are you ready to login?")
    command = recognize_speech_from_mic()
    if command and "yes" in command.lower():
        try:
            login_button = driver.find_element(By.CSS_SELECTOR, "#button[type='button']")
            login_button.click()
            speak_text("Logging you in.")
        except Exception as e:
            print(f"Error: {e}")
            speak_text("Error encountered while clicking login button.")
    else:
        speak_text("Login aborted.")

# Function to get spelling input
def get_spell_input():
    input_text = ""
    while True:
        command = recognize_speech_from_mic()
        if command:
            if command.lower() == "done":
                break
            elif command.lower() == "next":
                break
            else:
                input_text += command + " "
    return input_text.strip()

def main():
    speak_text("Hello, how can I assist you?")
    command = recognize_speech_from_mic()
    if command:
        response = f"You said: {command}"
        speak_text(response)


    app_url = "http://localhost:5173"
    driver = automate_browser(app_url)
    time.sleep(2)

    handle_form_interaction(driver)

    # Keep the browser open until manually closed
    while True:
        pass

if __name__ == "__main__":
    main()
