from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver
from datetime import datetime
from typing import Callable
import traceback

from Driver import get_driver, close_driver
from ParseMaster import read_questions
from OutputGenerator import initialize_output, save_response, finalize_output


def setup_driver(setting_up_func: Callable[[WebDriver], None], max_attempts=25):
    """Set up the driver with retries if needed.
    
    Args:
        setting_up_func: Function to set up the driver
        max_attempts: Maximum number of setup attempts
        
    Returns:
        tuple: (driver, rate_available) or (None, 0) if setup failed
    """
    driver = None
    attempts_left = max_attempts
    
    while attempts_left > 0:
        try:
            if driver:
                close_driver(driver)
            driver = get_driver()
            setting_up_func(driver)
            return driver, 15  # Return driver and rate_available
        except Exception:
            print(traceback.format_exc())
            attempts_left -= 1
    
    return None, 0  # Failed to set up driver


def save_and_exit(writer, responses, start_time, exceptions):
    """Save responses and exit with statistics."""
    save_response(writer, responses)
    end_time = datetime.now()
    diff = end_time - start_time
    avg = diff / len(responses) if responses else 0
    
    print("Failed to reset driver. Exiting.")
    print("Automation ended at " + str(end_time) + " after " + str(diff) + " seconds.")
    print("Average time per case (seconds): " + str(avg))
    print("Total cases: " + str(len(responses)))
    print("Exceptions: " + str(exceptions))
    exit(1)


def run_automation(
    test_data_path: str, 
    output_dir: str, 
    output_file: str, 
    navigate_back: Callable[[WebDriver], None], 
    setting_up: Callable[[WebDriver], None], 
    send_question: Callable[[WebDriver, str], None], 
    get_response: Callable[[WebDriver], str], 
) -> int:
    # Initialize variables
    driver = None
    questions = read_questions(test_data_path)
    responses = []
    writer = initialize_output(output_dir, output_file)
    exceptions = 0
    start_time = datetime.now()
    
    print("Starting automation at " + str(start_time) + "...")
    
    # First, set up the driver before processing any questions
    driver, rate_available = setup_driver(setting_up)
    if not driver:
        save_and_exit(writer, responses, start_time, exceptions)
    
    # Process all questions
    for i in range(0, len(questions)):
        question = questions.iloc[i]
        print(question)
        completed = False
        null_count = 0
        
        while not completed:
            # Check if we need to refresh the driver due to rate limits
            if rate_available < 1:
                if driver:
                    close_driver(driver)
                driver, rate_available = setup_driver(setting_up)
                if not driver:
                    save_and_exit(writer, responses, start_time, exceptions)
            
            try:
                # Send question and get response
                send_question(driver, question['input'])
                rate_available -= 1
                response = get_response(driver)
                navigate_back(driver)
                print(response,'response')
                
                # Handle null responses
                if (not response or response == 'null') and null_count < 5:
                    null_count += 1
                    continue
                
                # Save successful response
                responses.append({
                    'Index': question.name, 
                    'subkey': question['subkey'], 
                    'expout': question['expoutput'], 
                    'Response': response
                })
                completed = True
                
            except Exception:
                # Exception handling - reset driver and try again
                print(traceback.format_exc())
                exceptions += 1
                
                # Try to create a new driver
                driver, rate_available = setup_driver(setting_up)
                if not driver:
                    save_and_exit(writer, responses, start_time, exceptions)
    
    # All questions processed successfully
    if driver:
        close_driver(driver)
    
    save_response(writer, responses)
    
    # Print summary statistics
    end_time = datetime.now()
    diff = end_time - start_time
    avg = diff / len(responses)
    print("Done. Saved responses to " + output_file)
    print("Automation ended at " + str(end_time) + " after " + str(diff) + " seconds.")
    print("Average time per case (seconds): " + str(avg))
    print("Total cases: " + str(len(responses)))
    print("Exceptions: " + str(exceptions))
    
    return exceptions