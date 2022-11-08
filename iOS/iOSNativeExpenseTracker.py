import time
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support import expected_conditions as EC
from perfecto import PerfectoExecutionContext, TestResultFactory, TestContext, PerfectoReportiumClient
from perfecto import model
from selenium.webdriver.support.wait import WebDriverWait
from appium.options.ios import XCUITestOptions
from appium import webdriver

cloudName = "<Cloud Name>" # Ex - demo

xcuitest_options = XCUITestOptions()

xcuitest_options.platform_name = "iOS"

perfectoOptions = {
    'securityToken': '<Your security token>',
    'scriptName': 'Appium2 Test',
    'deviceName': '00008030-000354201A50802E',
    'automationName': 'Appium',
    'appiumVersion': 'latest',
    'automationVersion': '3.59.0',
    'app': 'PRIVATE:InvoiceApp1.0.ipa',
    'bundleId': 'io.perfecto.expense.tracker',
    'autoLaunch': True,
    'iOSResign': True
}

xcuitest_options.set_capability('perfecto:options', perfectoOptions)

# Initialize the Selenium driver
driver = webdriver.Remote('https://' + cloudName + '.perfectomobile.com/nexperience/perfectomobile/wd/hub', options= xcuitest_options)
print("Driver initiation successful")

# set implicit wait time
driver.implicitly_wait(5)

wait = WebDriverWait(driver, 30)

# Reporting client
perfecto_execution_context = PerfectoExecutionContext(webdriver=driver,
                                                              tags=['Tag1', 'Tag2'],
                                                              job=model.Job('ExpenseJob', '1', 'MainBranch'),
                                                              project=model.Project('ExpenseiOSNative', '1.0'))

reporting_client = PerfectoReportiumClient(perfecto_execution_context)
print("Reporting client created")

# Test start
reporting_client.test_start('ExpenseiOSNativePython', TestContext(tags=['iOS', 'Native']))

try:
    reporting_client.step_start("Enter Email")
    email = wait.until(EC.presence_of_element_located((MobileBy.NAME, "login_email")))
    email.send_keys('test@perfecto.com')
    reporting_client.step_end()

    reporting_client.step_start("Enter Password")
    password = wait.until(EC.presence_of_element_located((MobileBy.NAME, "login_password")))
    password.send_keys('test123')
    reporting_client.step_end()

    reporting_client.step_start("Click on Login")
    login = wait.until(EC.presence_of_element_located((MobileBy.NAME, "login_login_btn")))
    login.click()
    actualText1 = driver.find_element(MobileBy.XPATH,"//*[@label='Expenses']").text
    reporting_client.reportium_assert('Login successful', actualText1 == "Expenses")
    reporting_client.step_end()

    reporting_client.step_start("Click on Add(+)")
    add = wait.until(EC.presence_of_element_located((MobileBy.NAME, "list_add_btn")))
    add.click()
    reporting_client.step_end()

    reporting_client.step_start("Click on Head/Select")
    head = wait.until(EC.presence_of_element_located((MobileBy.NAME, "edit_head")))
    head.click()
    reporting_client.step_end()

    reporting_client.step_start("Click on Flight")
    flight = wait.until(EC.presence_of_element_located((MobileBy.XPATH, "//*[@value='- Select -']")))
    flight.send_keys("Flight")
    reporting_client.step_end()

    reporting_client.step_start("Enter amount")
    amount = wait.until(EC.presence_of_element_located((MobileBy.NAME, "edit_amount")))
    amount.send_keys('100')
    reporting_client.step_end()

    reporting_client.step_start("Click on Save and verify alert")
    save = wait.until(EC.presence_of_element_located((MobileBy.NAME, "add_save_btn")))
    save.click()
    time.sleep(3)
    # Execute script method to find text
    params = {'content': 'Please enter valid category'}
    driver.execute_script('mobile:text:find', params);
    reporting_client.step_end()

    reporting_client.test_stop(TestResultFactory.create_success())

except Exception as e:
    print("in Exception")
    reporting_client.test_stop(TestResultFactory.create_failure(str(e)))
    print(e)
finally:
    try:
        print("In final block")
        driver.quit()
        # Retrieve the URL of the Single Test Report, can be saved to your execution summary and used to download the report at a later point
        report_url = reporting_client.report_url()
        print("Test report URL: ", report_url)

    except Exception as e:
        print(e)

print('iOS Native Python Test run ended')
