import pytest
from configparser import ConfigParser

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC, expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
import time
import attach
import Excelreader
from LogClass import BaseClass


# Sanity_MPPP360_AssociatePortal
@pytest.mark.usefixtures("setup")
class Test_Services(BaseClass):

    @pytest.mark.order(1)
    def test_Login_TC01(self):
        try:
            log = self.getLogger()
            # getLogger method is called for logging
            c = ConfigParser()
            c.read("Data.properties")
            wait = WebDriverWait(self.driver, 50)
            Associate_userName = self.driver.find_element(By.XPATH, "//input[@id='email']")
            Associate_userName.click()
            Associate_userName.send_keys(c['Section_data']['userid'])
            log.info("UserName Entered")
            Associate_Password = self.driver.find_element(By.XPATH, "//input[@id='password']")
            Associate_Password.click()
            Associate_Password.send_keys(c['Section_data']['password'])
            log.info("Password Entered")
            LOGIN = self.driver.find_element(By.XPATH, "//button[text()='Log In']")
            self.driver.execute_script("arguments[0].click()", LOGIN)
            log.info("Clicked on Log In")
            try:
                wait.until(
                    expected_conditions.visibility_of_element_located((By.XPATH, "//p[text()='Member Details']")))
                MemberDetails = self.driver.find_element(By.XPATH, "//p[text()='Member Details']")
                if MemberDetails.is_displayed:
                    log.info("Successfully landed to home page ")
            except:
                pass

        except Exception as e:
            log.error(e)
            pytest.fail(str(e), pytrace=True)
            attach(data=self.driver.get_screenshot_as_png())

    @pytest.mark.order(2)
    # searching member with mbi
    def test_SearchMbrByMBI_TC02(self):
        try:
            self.driver.implicitly_wait(20)
            log = self.getLogger()
            wait = WebDriverWait(self.driver, 40)
            wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='MBI Search']")))
            MBI = self.driver.find_element(By.XPATH,"//input[@placeholder='MBI Search']")
            self.driver.execute_script("arguments[0].click();", MBI)
            MemberData = Excelreader.excel_reader(self, "MemberData")
            log.info("Mbi " + MemberData[0]['MBI'] + " being Searched")
            wait = WebDriverWait(self.driver, 40)
            self.driver.find_element(By.XPATH,"//input[@placeholder='MBI Search']").send_keys(MemberData[0]['MBI'])
            log.info(" Mbi entered")
            # waiting for clickability of search button
            wait.until(expected_conditions.element_to_be_clickable((By.XPATH, "//button[text()='Search']")))
            Search = self.driver.find_element(By.XPATH,"//button[text()='Search']")
            self.driver.execute_script("arguments[0].click();", Search)
            mbi = self.driver.find_element(By.XPATH,"//div[1]/div/div[2]/div[1]/div[2]/p").text
            if mbi == MemberData[0]['MBI']:
                log.info(MemberData[0]['MBI'] + "  Member Searched")
        except Exception as e:
            log.info(e)
            attach(data=self.driver.get_screenshot_as_png())
            pytest.fail(e, pytrace=True)


    @pytest.mark.order(3)
    # searching  optin/optout history
    def test_SearchHistory_TC03(self):
        try:
            self.driver.implicitly_wait(20)
            log = self.getLogger()
            wait = WebDriverWait(self.driver, 40)
            wait.until(EC.visibility_of_element_located((By.XPATH, "//div[1]/div[4]/button[text()='...more']")))
            self.driver.find_element(By.XPATH, "//div[1]/div[4]/button[text()='...more']").click()
            log.info('Click on more button to check the history')
            wait.until(EC.visibility_of_element_located((By.XPATH, "//th[text()='Mpp Opt-In']")))
            History = self.driver.find_element(By.XPATH,"//table[@class='MuiTable-root table customTable css-15jeypj']").text
            log.info(History)
            close = self.driver.find_element(By.XPATH, "//h2/button[@type='button']")
            self.driver.execute_script("arguments[0].click();", close)

        except Exception as e:
            log.info(e)
            attach(data=self.driver.get_screenshot_as_png())
            pytest.fail(e, pytrace=True)

    @pytest.mark.order(4)
    # searching invoice
    def test_SearchCurrentInvoice_TC04(self):
        try:
            self.driver.implicitly_wait(20)
            log = self.getLogger()
            wait = WebDriverWait(self.driver, 40)
            wait.until(EC.visibility_of_element_located((By.XPATH, "//div[2]/div[4]/button[text()='...more']")))
            self.driver.find_element(By.XPATH, "//div[2]/div[4]/button[text()='...more']").click()
            log.info('Clicking on more button to check the current invoice')
            self.driver.find_element(By.XPATH, "//table/tbody/tr[1]/td[6]/i[@class='fa fa-angle-down']").click()
            time.sleep(3)
            try:
                time.sleep(2)
                invoice = self.driver.find_element(By.XPATH, "//td[2]/strong")
                if invoice.is_displayed():
                    invoice_text=invoice.text
                    log.info(invoice_text)
            except:
                self.error_message_or_oops()
            log.info("Current invoice  Tab Verified")

        except Exception as e:
            log.info(e)
            attach(data=self.driver.get_screenshot_as_png())
            pytest.fail(e, pytrace=True)

    @pytest.mark.order(5)
    # Checking pyment history
    def test_CheckPaymentHistory_TC05(self):
        try:
            self.driver.implicitly_wait(20)
            log = self.getLogger()
            wait = WebDriverWait(self.driver, 40)
            home = self.driver.find_element(By.XPATH,"//a[text()='Home']")
            self.driver.execute_script("arguments[0].click();", home)
            wait.until(EC.visibility_of_element_located((By.XPATH, "//div[3]/div[4]/button[text()='...more']")))
            payment_history = self.driver.find_element(By.XPATH, "//div[3]/div[4]/button[text()='...more']")
            self.driver.execute_script("arguments[0].click();", payment_history)

            log.info('Clicking on more button to check the payment history')
            payment = self.driver.find_element(By.XPATH,"//span[text()='Payment History']")
            if payment.is_displayed():
                log.info("Payment History Tab Verified")

        except Exception as e:
            log.info(e)
            attach(data=self.driver.get_screenshot_as_png())
            pytest.fail(e, pytrace=True)

    @pytest.mark.order(6)
    # Checking  prescription
    def test_CheckingPrescription_TC06(self):
        try:
            self.driver.implicitly_wait(20)
            log = self.getLogger()
            wait = WebDriverWait(self.driver, 40)
            home = self.driver.find_element(By.XPATH,"//a[text()='Home']")
            self.driver.execute_script("arguments[0].click();",home)
            wait.until(EC.visibility_of_element_located((By.XPATH, "//p[text()='View']")))
            prescription = self.driver.find_element(By.XPATH, "//p[text()='View']")
            self.driver.execute_script("arguments[0].click();", prescription)
            log.info('Clicking on view button to check the prescription details')
            drug = self.driver.find_element(By.XPATH,"//label[text()='Drug Name']")
            if drug.is_displayed():
                log.info("Prescription Tab Verified")

        except Exception as e:
            log.info(e)
            attach(data=self.driver.get_screenshot_as_png())
            pytest.fail(e, pytrace=True)

    @pytest.mark.order(7)
    # Checking  correspondence
    def test_CheckingCorrespondence_TC07(self):
        try:
            self.driver.implicitly_wait(20)
            log = self.getLogger()
            wait = WebDriverWait(self.driver, 40)
            correspondence = self.driver.find_element(By.XPATH,"//a[text()='Correspondence']")
            self.driver.execute_script("arguments[0].click();", correspondence)
            log.info('Clicking on correspondence tab')
            letter_name = self.driver.find_element(By.XPATH,"//label[text()='Letter Name']")
            if letter_name.is_displayed():
                log.info("Correspondence Tab Verified")

        except Exception as e:
            log.info(e)
            attach(data=self.driver.get_screenshot_as_png())
            pytest.fail(e, pytrace=True)

    @pytest.mark.order(8)
    # Checking oop biling forecast
    def test_CheckingOOP_BILLING_TC08(self):
        try:
            self.driver.implicitly_wait(20)
            log = self.getLogger()
            wait = WebDriverWait(self.driver, 40)
            home = self.driver.find_element(By.XPATH,"//a[text()='Home']")
            self.driver.execute_script("arguments[0].click();", home)
            wait.until(EC.visibility_of_element_located((By.XPATH, "//button[text()='OOP Billing Forecast']")))
            oop = self.driver.find_element(By.XPATH, "//button[text()='OOP Billing Forecast']")
            self.driver.execute_script("arguments[0].click();", oop)
            log.info('Clicking on oop billing forecast  button ')
            simulate = self.driver.find_element(By.XPATH,"// p[text() = 'Simulate OOP Billing Forecast']")
            self.driver.execute_script("arguments[0].click();", simulate)
            log.info('Clicking on simulate forecast  ')
            delete = self.driver.find_element(By.XPATH, "//button[text()='Del']")
            self.driver.execute_script("arguments[0].click();", delete)
            log.info('Clicking on del button to delete the existing row ')
            add = self.driver.find_element(By.XPATH, "//button[text()='Add']")
            self.driver.execute_script("arguments[0].click();", add)
            log.info('Clicking on add button to add a new row for calculation')
            MemberData = Excelreader.excel_reader(self, "MemberData")
            Year = self.driver.find_element(By.ID,"year")
            self.driver.execute_script("arguments[0].click();", Year)
            Year.send_keys(Keys.BACKSPACE * len(Year.get_attribute("value")))
            Year.send_keys(MemberData[0]['Year'])
            Date = self.driver.find_element(By.ID,"oopCostDate")
            self.driver.execute_script("arguments[0].click();", Date)
            Date.send_keys(MemberData[0]['Date'])
            cost = self.driver.find_element(By.ID, "prescriptionCost")
            self.driver.execute_script("arguments[0].click();", cost)
            cost.send_keys(MemberData[0]['OOP_Cost'])
            calculate = self.driver.find_element(By.XPATH, "//button[text()='Calculate']")
            self.driver.execute_script("arguments[0].click();", calculate)
            log.info('Clicking on calculate button  for calculation')
            try:
                table = self.driver.find_element(By.XPATH,"//div[5]/div/table")
                self.driver.execute_script("arguments[0].scrollIntoView({block:\"center\"});", table)
                if table.is_displayed():
                    log.info("Simulate Forecast Verified")
                    wait.until(EC.element_to_be_clickable((By.XPATH, "//*[local-name()='svg' and @data-testid='CloseIcon']")))
                    close = self.driver.find_element(By.XPATH,"//*[local-name()='svg' and @data-testid='CloseIcon']")
                    #self.driver.execute_script("arguments[0].click();", close)
                    close.click
                    log.info('Close the pop up')
            except:
                record = self.driver.find_element(By.XPATH,"//p[text()='No OptIn record found !']").text
                log.info(record)
                ok = self.driver.find_element(By.XPATH, "//button[text()='OK']")
                self.driver.execute_script("arguments[0].click();", ok)
                log.info('Clicking on OK button')

        except Exception as e:
            log.info(e)
            attach(data=self.driver.get_screenshot_as_png())
            pytest.fail(e, pytrace=True)

    @pytest.mark.order(9)
    # logging out
    def test_LogOut_TC09(self):
        try:
            self.driver.implicitly_wait(20)
            log = self.getLogger()
            wait = WebDriverWait(self.driver, 40)
            wait.until(EC.visibility_of_element_located((By.XPATH, "//span[@class='MuiButton-endIcon MuiButton-iconSizeMedium css-pt151d']")))
            icon = self.driver.find_element(By.XPATH,"//span[@class='MuiButton-endIcon MuiButton-iconSizeMedium css-pt151d']")
            self.driver.execute_script("arguments[0].click();", icon)
            time.sleep(3)
            wait.until(EC.element_to_be_clickable((By.XPATH, "//li[text()='Logout']")))
            logout = self.driver.find_element(By.XPATH,"//li[text()='Logout']")
            self.driver.execute_script("arguments[0].click();", logout)
            time.sleep(3)

        except Exception as e:
            log.info(e)
            attach(data=self.driver.get_screenshot_as_png())
            pytest.fail(e, pytrace=True)