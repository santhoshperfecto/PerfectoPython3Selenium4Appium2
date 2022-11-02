from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from perfecto import PerfectoExecutionContext, TestResultFactory, TestContext, PerfectoReportiumClient
from perfecto import model
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.wait import WebDriverWait

cloudName = "<Cloud Name>" # EX - demo

chrome_options = ChromeOptions()

chrome_options.platform_name = "Windows"
chrome_options.browser_version = 'latest'

perfectoOptions = {
    'securityToken': '<Your security token>',
    'platformVersion': '11'
}

chrome_options.set_capability('perfecto:options', perfectoOptions)

# Initialize the Selenium driver
driver = webdriver.Remote('https://' + cloudName + '.perfectomobile.com/nexperience/perfectomobile/wd/hub', options= chrome_options)
print("Driver initiation successful")

# set implicit wait time
driver.implicitly_wait(5)

driver.maximize_window()
wait = WebDriverWait(driver, 30)

# Reporting client
perfecto_execution_context = PerfectoExecutionContext(webdriver=driver,
                                                              tags=['Tag1', 'Tag2'],
                                                              job=model.Job('ExpenseJob', '1', 'MainBranch'),
                                                              project=model.Project('ExpenseWindowsChrome', '1.0'))

reporting_client = PerfectoReportiumClient(perfecto_execution_context)
print("Reporting client created")

# Test start
reporting_client.test_start('ExpenseWindowsChromePython', TestContext(tags=['Windows', 'Chrome']))

try:
    reporting_client.step_start("Navigate to URL")
    driver.get("http://expensetracker.perfectomobile.com")
    reporting_client.step_end()

    reporting_client.step_start("Enter Email")
    email = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='login_email']/input")))
    email.send_keys('test@perfecto.com')
    reporting_client.step_end()

    reporting_client.step_start("Enter Password")
    password = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='login_password']/input")))
    password.send_keys('test123')
    reporting_client.step_end()

    reporting_client.step_start("Click on Login")
    login = wait.until(EC.presence_of_element_located((By.NAME, "login_login_btn")))
    login.click()

    reporting_client.step_start("Click on Logout")
    driver.find_element(By.NAME, "log-out").click()
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

print('Windows Chrome Python Test run ended')