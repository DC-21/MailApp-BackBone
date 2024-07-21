import time
import speech_recognition as sr
import pyttsx3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
            time.sleep(6)  # Wait for login process to complete

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
        # Check for the element indicating successful login (adjust selector as needed)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
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
            driver.get("http://localhost:5173/compose")
            time.sleep(2)  # Wait for the page to load
            send_email(driver)
        elif "view" in command.lower():
            speak_text("You chose to view emails. Redirecting you to the inbox.")
            driver.get("http://localhost:5173/home")
            time.sleep(2)  # Wait for the page to load
            view_emails(driver)
        else:
            speak_text("I didn't understand that. Please say 'send' to send an email or 'view' to view emails.")
            post_login_interaction(driver)  # Ask again

# Function to handle sending an email
def send_email(driver):
    # Get and confirm recipient email
    recipient = get_and_confirm_input("recipient email address")
    if recipient:
        try:
            recipient_field = driver.find_element(By.CSS_SELECTOR, "#recipient[type='email']")
            print(f"Entering recipient: {recipient}")
            recipient_field.send_keys(recipient)
        except Exception as e:
            print(f"Error: {e}")
            speak_text("Error encountered while typing recipient email.")

    # Get and confirm email subject
    subject = get_input_phrase("email subject")
    if subject:
        try:
            subject_field = driver.find_element(By.CSS_SELECTOR, "#subject[type='text']")
            print(f"Entering subject: {subject}")
            subject_field.send_keys(subject)
        except Exception as e:
            print(f"Error: {e}")
            speak_text("Error encountered while typing subject.")

    # Get and confirm email body
    body = get_input_phrase("email body")
    if body:
        try:
            body_field = driver.find_element(By.ID, "content")
            print(f"Entering body: {body}")
            body_field.send_keys(body)
        except Exception as e:
            print(f"Error: {e}")
            speak_text("Error encountered while typing email body.")

    # Send the email
    try:
        send_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        send_button.click()
        speak_text("Email sent successfully.")
        
        # Wait for a response indicating email sent successfully
        wait_for_email_response(driver)
        
    except Exception as e:
        print(f"Error: {e}")
        speak_text("Error encountered while sending email.")

def wait_for_email_response(driver):
    speak_text("Waiting for response...")
    # Example: You can check for a success message or element indicating the email was sent successfully
    # In this example, let's wait for a few seconds as a placeholder
    time.sleep(5)

    speak_text("What would you like to do next? Say 'send' to send another email or 'view' to view emails.")
    command = recognize_speech_from_mic()
    if command:
        if "send" in command.lower():
            # **Modification here** - No redirection, user stays on the compose page
            speak_text("You chose to send another email.")
        elif "view" in command.lower():
            speak_text("You chose to view emails. Redirecting you to the inbox.")
            driver.get("http://localhost:5173/home")
        else:
            speak_text("I didn't understand that. Please say 'send' to send another email or 'view' to view emails.")
            wait_for_email_response(driver)

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

# Function to get input phrases like subject and body
def get_input_phrase(field_name):
    while True:
        speak_text(f"Please say your {field_name}.")
        input_text = recognize_speech_from_mic()
        if input_text:
            speak_text(f"You said your {field_name} is {input_text}. Is that correct?")
            command = recognize_speech_from_mic()
            if command and "yes" in command.lower():
                return input_text
            else:
                speak_text(f"Let's try again. Please say your {field_name}.")

def parse_email_number_from_word(text):
    # Define a mapping of text numbers to numeric values
    text_to_number = {
        "first": 1,
        "second": 2,
        "third": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eigh": 8,
        "nine": 9,
        "ten": 10
        # Add more mappings as needed
    }

    # Convert the text to lowercase to handle case insensitivity
    text = text.lower().strip()
    
    # Return the corresponding number if found in the mapping, otherwise None
    return text_to_number.get(text, None)
def view_emails(driver):
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table.min-w-full"))
        )
    except Exception as e:
        print(f"Error: {e}")
        speak_text("Error encountered while loading emails.")
        return

    while True:
        emails = driver.find_elements(By.CSS_SELECTOR, "tbody tr")
        if not emails:
            speak_text("No emails found.")
            break
        
        for index, email in enumerate(emails):
            email_id = index + 1
            email_from = email.find_element(By.CSS_SELECTOR, "td:nth-child(2)").text
            email_subject = email.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text
            content = email.find_element(By.CSS_SELECTOR, "td:nth-child(4)").text
            
            # Prompt the user if they want the content read aloud
            speak_text(f"Email {email_id}: From {email_from}, Subject {email_subject}. Do you want to read the content?")
            
            user_response = recognize_speech_from_mic()
            if user_response and 'yes' in user_response.lower():
                # Read out the content if user says 'yes'
                speak_text(f"Content {content}")
            else:
                # Skip to the next email if user says 'no'
                speak_text("Skipping to the next email.")
                continue
        
        # Ask the user if they want to read more emails
        speak_text("Do you want to read more emails? Say 'yes' to continue or 'no' to stop.")
        continue_response = recognize_speech_from_mic()
        if not continue_response or 'yes' not in continue_response.lower():
            speak_text("Exiting email reading.")
            break
def read_email_content(driver):
    try:
        # Wait for the modal to appear
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".fixed .bg-white"))
        )
        speak_text("Reading the email content.")
        
        # Extract email details
        from_text = driver.find_element(By.CSS_SELECTOR, ".bg-white .font-bold + span").text
        subject_text = driver.find_element(By.CSS_SELECTOR, ".bg-white .font-bold + span + div + span + span").text
        content_text = driver.find_element(By.CSS_SELECTOR, ".bg-white .font-bold + span + div + div").text

        # Read the email content aloud
        speak_text(f"From: {from_text}")
        speak_text(f"Subject: {subject_text}")
        speak_text(f"Content: {content_text}")
        
        # Inform the user that reading is done
        speak_text("Done reading the email. Closing the email view.")
        
        # Close the modal
        close_button = driver.find_element(By.CSS_SELECTOR, ".bg-white button")
        close_button.click()
        
    except Exception as e:
        print(f"Error: {e}")
        speak_text("Error encountered while reading the email content.")

# Function to parse the email number from the recognized speech command
def parse_email_number(command):
    words_to_numbers = {
        "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
        "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10
    }
    for word, number in words_to_numbers.items():
        if word in command.lower():
            return number
    try:
        return int(command.strip())
    except ValueError:
        return None

# Main function to start the interaction
def main():
    speak_text("Starting the Mail App.")
    driver = automate_browser("http://localhost:5173")
    handle_form_interaction(driver)

if __name__ == "__main__":
    main()
