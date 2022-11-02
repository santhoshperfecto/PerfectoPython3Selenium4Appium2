from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support import expected_conditions as EC
from perfecto import PerfectoExecutionContext, TestResultFactory, TestContext, PerfectoReportiumClient
from perfecto import model
from selenium.webdriver.support.wait import WebDriverWait
from appium.options.android import UiAutomator2Options
from appium import webdriver

cloudName = "<Cloud Name>" # Ex - demo
uiautomator2_options = UiAutomator2Options()

uiautomator2_options.platform_name = "android"

perfectoOptions = {
    'securityToken': '<Your security token>',
    'scriptName': 'Appium2 Test',
    'deviceName': 'R5CT20QC2AR',
    'automationName': 'Appium',
    'appiumVersion': '2.0.0',
    'automationVersion': '1.70.1',
    'app': 'PRIVATE:ExpenseTrackerNative.apk',
    'appPackage': 'io.perfecto.expense.tracker',
    'autoLaunch': True
}

uiautomator2_options.set_capability('perfecto:options', perfectoOptions)

# Initialize the Appium driver
driver = webdriver.Remote('https://' + cloudName + '.perfectomobile.com/nexperience/perfectomobile/wd/hub', options= uiautomator2_options)
print("Driver initiation successful")

# set implicit wait time
driver.implicitly_wait(5)

wait = WebDriverWait(driver, 30)

# Reporting client
perfecto_execution_context = PerfectoExecutionContext(webdriver=driver,
                                                              tags=['Tag1', 'Tag2'],
                                                              job=model.Job('ExpenseJob', '1', 'MainBranch'),
                                                              project=model.Project('ExpenseAndroidNative', '1.0'))

reporting_client = PerfectoReportiumClient(perfecto_execution_context)
print("Reporting client created")

# Test start
reporting_client.test_start('ExpenseAndroidNativePython', TestContext(tags=['Android', 'Native']))

try:
    reporting_client.step_start("Enter Email")
    email = wait.until(EC.presence_of_element_located((MobileBy.ID, "io.perfecto.expense.tracker:id/login_email")))
    email.send_keys('test@perfecto.com')
    reporting_client.step_end()

    reporting_client.step_start("Enter Password")
    password = wait.until(EC.presence_of_element_located((MobileBy.ID, "io.perfecto.expense.tracker:id/login_password")))
    password.send_keys('test123')
    reporting_client.step_end()

    reporting_client.step_start("Click on Login")
    login = wait.until(EC.presence_of_element_located((MobileBy.ID, "io.perfecto.expense.tracker:id/login_login_btn")))
    login.click()
    actualText1 = driver.find_element(MobileBy.XPATH, "//*[@text=\"Expenses\"]").text
    reporting_client.reportium_assert('Login successful', actualText1 == "Expenses")
    reporting_client.step_end()

    reporting_client.step_start("Click on Add(+)")
    add = wait.until(EC.presence_of_element_located((MobileBy.ID, "io.perfecto.expense.tracker:id/list_add_btn")))
    add.click()
    reporting_client.step_end()

    reporting_client.step_start("Click on Head/Select")
    head = wait.until(EC.presence_of_element_located((MobileBy.ID, "io.perfecto.expense.tracker:id/input_layout_head")))
    head.click()
    reporting_client.step_end()

    reporting_client.step_start("Click on Flight")
    flight = wait.until(EC.presence_of_element_located((MobileBy.XPATH, '//*[@text="Flight"]')))
    flight.click()
    reporting_client.step_end()

    reporting_client.step_start("Enter amount")
    amount = wait.until(EC.presence_of_element_located((MobileBy.ID, "io.perfecto.expense.tracker:id/add_amount")))
    amount.send_keys('100')
    reporting_client.step_end()

    reporting_client.step_start("Click on Save and verify alert")
    save = wait.until(EC.presence_of_element_located((MobileBy.ID, "io.perfecto.expense.tracker:id/layout_buttons")))
    save.click()
    actualText2 = driver.find_element(MobileBy.XPATH, "//*[@resource-id='io.perfecto.expense.tracker:id/snackbar_text']").text
    reporting_client.reportium_assert('Verify Alert text', actualText2 == "Select Currency")

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

print('Android Native Python Test run ended')