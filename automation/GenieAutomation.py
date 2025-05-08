from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver
import time


def navigate_back(driver: WebDriver):
    # el2 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,
    #                           value="new UiSelector().className(\"android.view.View\").instance(6)")
    # el2.click()
    wait = WebDriverWait(driver, 2)
    el2 = wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR,
                                                 "new UiSelector().className(\"android.view.View\").instance(6)")))

    el2.click()


def setting_up(driver: WebDriver):
    time.sleep(5)
    el1 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Continue")
    el1.click()
    el2 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Continue")
    el2.click()
    time.sleep(1)
    try:
        allow_button = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().text("Allow")')
        allow_button.click()
        time.sleep(5)
    except:
        pass
    # time.sleep(2)
    # print(driver.page_source)  # 🔍 Add this line to inspect the current screen
    try:
        skip_btn= driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Skip")
        skip_btn.click()
        print("Chanukya3")
        time.sleep(10)
    except Exception as e:
        print("Skip button not found:", e)

def send_question(driver: WebDriver, question: str):
    print(question,'qwert')
    wait = WebDriverWait(driver, 2)
    el4 = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, "//android.widget.FrameLayout//android.widget.EditText")))
    el4.click()
    print(question,'qwert1')
    el5 = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, "//android.widget.FrameLayout//android.widget.EditText")))
    el5.send_keys(question)
    print(question,'qwer2')
    el6 = wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR,
                                                 "new UiSelector().className(\"android.widget.Button\").instance(1)")))
    el6.click()
    time.sleep(2)
    print(question,'qwer3')
    el9 = driver.find_element(by=AppiumBy.XPATH,
                              value="//android.widget.FrameLayout/android.widget.LinearLayout//android.widget.ImageView[@index='2']")
    captured_text = el9.get_attribute("content-desc")
    if not captured_text or captured_text == 'null':  # try again after 3 seconds if value is null
        time.sleep(3)
        el9 = driver.find_element(by=AppiumBy.XPATH,
                                  value="//android.widget.FrameLayout/android.widget.LinearLayout//android.widget.ImageView[@index='2']")
        captured_text = el9.get_attribute("content-desc")
        if not captured_text or captured_text == 'null':  # try again after 5 seconds if value is null
            time.sleep(5)
            el9 = driver.find_element(by=AppiumBy.XPATH,
                                      value="//android.widget.FrameLayout/android.widget.LinearLayout//android.widget.ImageView[@index='2']")
            captured_text = el9.get_attribute("content-desc")



def get_response(driver):
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((AppiumBy.XPATH, "//android.widget.ImageView[@content-desc]"))
        )

        # Get all ImageView elements with content-desc
        elements = driver.find_elements(by=AppiumBy.XPATH, value="//android.widget.ImageView[@content-desc]")

        if len(elements) >= 2:
            # Second ImageView is assumed to be the ChatGPT answer
            answer_element = elements[1]
            response_text = answer_element.get_attribute("contentDescription")
            print("[SUCCESS] ChatGPT Answer:", response_text)
            return response_text
        else:
            print("[WARN] Less than 2 response elements found. Unable to isolate answer.")
            return None

    except Exception as e:
        print("[ERROR] Failed to capture ChatGPT response:", e)
        return None





def setting_up_deepseek(driver: WebDriver):
    time.sleep(5)
    el1 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Continue")
    el1.click()
    el2 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Continue")
    el2.click()
    time.sleep(1)
    try:
        allow_button = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().text("Allow")')
        allow_button.click()
        time.sleep(3)
    except:
        pass
    try:
        skip_btn= driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Skip")
        skip_btn.click()
        time.sleep(3)
    except Exception as e:
        print("Skip button not found:", e)
    try:
        element = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Model\nChatGPT")
        element.click()
        print("Clicked on 'Model ChatGPT'")
        time.sleep(3)
    except Exception as e:
        print("Could not click 'Model ChatGPT':", e)

    try:
        deepseek_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "DeepSeek")))
        deepseek_btn.click()
        print("Clicked on the DeepSeek button")
        time.sleep(3)
    except Exception as e:
        print("Failed to click DeepSeek:", e)
    
    try:
        ok_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "OK")) )
        ok_btn.click()
        print("Clicked on the OK button")
    except Exception as e:
        print("Failed to click OK:", e)
  