import time
import speech_recognition as sr
import pyttsx3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

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
    speak_text("The Mail App is opening in Chrome browser.")
    driver = webdriver.Chrome()
    driver.get(url)
    return driver

# Function to handle form interaction based on voice commands
def handle_form_interaction(driver):
    # Get and confirm email
    email = get_and_confirm_input("email address")
    if email:
        try:
            email_field = driver.find_element(By.CSS_SELECTOR, "#email[type='email']")
            email_field.send_keys(email)
        except Exception as e:
            print(f"Error: {e}")
            speak_text("Error encountered while typing email.")

    # Get and confirm password
    password = get_and_confirm_input("password")
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
            login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()
            speak_text("Logging you in.")
            time.sleep(3)  # Wait for login process to complete

            # Check for a specific element that appears after login to confirm success
            if is_login_successful(driver):
                speak_text("Login successful.")
                post_login_interaction(driver)
            else:
                speak_text("Login failed. Please try again.")
        except Exception as e:
            print(f"Error: {e}")
            speak_text("Error encountered while clicking login button.")
    else:
        speak_text("Login aborted.")

# Function to check if login is successful
def is_login_successful(driver):
    try:
        # Check for the logout button indicating successful login
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']")  # Adjust the selector as needed
        return True
    except NoSuchElementException:
        return False

# Function to handle post-login interactions
def post_login_interaction(driver):
    speak_text("Would you like to send an email or view emails?")
    command = recognize_speech_from_mic()
    if command:
        if "send" in command.lower():
            speak_text("You chose to send an email. Redirecting you to the compose page.")
            # Navigate to the compose page or handle sending email
            # driver.get("compose_page_url")
        elif "view" in command.lower():
            speak_text("You chose to view emails. Redirecting you to the inbox.")
            # Navigate to the inbox page or handle viewing emails
            # driver.get("inbox_page_url")
        else:
            speak_text("I didn't understand that. Please say 'send' to send an email or 'view' to view emails.")
            post_login_interaction(driver)  # Ask again

# Function to get spelling input, trim out spaces, and confirm input
def get_and_confirm_input(field_name):
    while True:
        speak_text(f"Please spell out your {field_name}.")
        input_text = get_spell_input().replace(" ", "")
        speak_text(f"You spelled {field_name} as {input_text}. Is that correct?")
        command = recognize_speech_from_mic()
        if command and "yes" in command.lower():
            return input_text
        else:
            speak_text(f"Let's try again. Please spell out your {field_name}.")

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
