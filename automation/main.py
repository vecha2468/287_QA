import os
import GenieAutomation
from Automation import run_automation

# 🔧 Fix for Appium environment detection
os.environ['ANDROID_HOME'] = '/Users/vejandlachanukya/Library/Android/sdk'
os.environ['ANDROID_SDK_ROOT'] = '/Users/vejandlachanukya/Library/Android/sdk'

if __name__ == '__main__':
    test_data_path = 'testing.xlsx'
    test_data_path_cheapest='TransportationCostFunctionSubset.xlsx'
    output_dir = './output'
    output_cheapest='./output_cheapest'
    output_file = 'test_output.xlsx'
    output_file_2='test_output_Deepseek.xlsx'


    run_automation(test_data_path_cheapest, output_cheapest, output_file,  GenieAutomation.navigate_back, GenieAutomation.setting_up, GenieAutomation.send_question, GenieAutomation.get_response)
    # run_automation(test_data_path, output_dir, output_file_2,  GenieAutomation.navigate_back, GenieAutomation.setting_up_deepseek, GenieAutomation.send_question, GenieAutomation.get_response)