# Import drission to scrap
from DrissionPage import ChromiumPage
from DrissionPage.common import By

# Other important libs
import time
import os

def main():
    # Use Chrome driver
    p = ChromiumPage()

    # Get deepl login
    p.get('https://www.deepl.com/login')
    
    # Elements
    username_location = By.ID, 'menu-login-username'
    password_location = By.ID, 'menu-login-password'
    login_location = By.ID, 'menu-login-submit'
    translation_location = By.XPATH, '//*[@id="textareasContainer"]/div[1]/section'

    # Locate it using driver 
    mail = p.ele(username_location)
    password = p.ele(password_location)
    login = p.ele(login_location)
    translation_box = p.ele(translation_location)

    # Fill fields and log in
    p.actions.click(mail).input("casandra.bru@hotmail.com")
    p.actions.click(password).input('hOl41LoW1')
    p.actions.click(login)

    # Folders name
    input_folder = "chapters"
    output_folder = "translate"

    # Check if input folder exists
    if os.path.exists(input_folder) and os.listdir(input_folder):
        # If output folder don't exists, create new
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        # Check each text file in input folder
        for filename in os.listdir(input_folder):
            # Make input path to file
            input_file_path = os.path.join(input_folder, filename)

            # Open in read mode and get text from the file
            with open(input_file_path, 'r', encoding='utf-8') as file:
                text = file.read()

            # Find and click translation box
            p.actions.click(translation_box).input(text)

            # Wait for translation
            time.sleep(5)

            # Find translated box
            translated_text_location = By.CSS_SELECTOR, "d-textarea[name='target'] div[contenteditable='true']"
            translated_text = p.ele(translated_text_location)

            # Make output path and write translated script into the file
            output_path = os.path.join(output_folder, filename)
            with open(output_path, "w", encoding='utf-8') as file:
                file.write(translated_text.text.strip())
            
            # Clear box to next iteration
            translation_box.clear()

            print("Text translated successfull!")

        # Eventually exit from the driver
        else:
            p.quit()

if __name__ == "__main__":
    main()