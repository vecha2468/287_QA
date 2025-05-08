from appium import webdriver
from appium.options.android import UiAutomator2Options
from os import path
import time

def get_driver():
    desired_capabilities = {
    "platformName": "Android",
    "platformVersion": "16",  # adjust based on your emulator
    "deviceName": "emulator-5554",
    "automationName": "UiAutomator2",
    'newCommandTimeout': 3600,
        'ensureWebviewsHavePages': True,
        'connectHardwareKeyboard': True,
        'app': path.abspath('ai-chat-and-chatbot-genie-6-1-1.apk')
    }
    options = UiAutomator2Options().load_capabilities(desired_capabilities)
    driver = webdriver.Remote('http://localhost:4723', options=options)
    time.sleep(5)  # Wait for ChatGPT to load
    return driver

def close_driver(driver: webdriver.webdriver.WebDriver):
    driver.quit()
