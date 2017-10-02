#coding: utf-8
from selenium import webdriver
from selenium.webdriver.support.ui import Select
# from selenium.webdriver.support.ui import WebDriverWait
import time
import pandas as pd
from sqlalchemy import create_engine
from re import findall


class UATRobot(object):
    def __init__(self, url):
        self.engine = create_engine('oracle://xxxx@xxxxx.CN.INFRA:xxxx')
        self.browser = webdriver.Chrome()
        self.browser.get(url)
        self.browser.find_element_by_tag_name("button").click()
        self.Amount_Term_Selector(42000, 30)
  
        # self.browser.find_element_by_xpath('//*[@id="product-selection-continue"]').click()

    def Amount_Term_Selector(self, amount, term):
        if amount <= 11000 and amount > 3000:
            offset_bar = (amount - 2000) / 1000 * 17
        elif amount > 11000 and amount <= 20000:
            offset_bar = (amount - 2000) / 1000 * 16
        elif amount > 20000 and amount <= 40000:
            offset_bar = (amount - 2000) / 1000 * 15.5
        elif amount > 40000:
            offset_bar = (amount - 2000) / 1000 * 15.2
        offset_term_x = 150 * term / 6 if term < 24 else 150 * (term-24) / 6
        offset_term_y = 120 if term > 24 else 60
        actionChains = webdriver.ActionChains(self.browser)
        option=self.browser.find_element_by_xpath('//*[@id="progresscur"]')
        actionChains.move_to_element_with_offset(option, offset_bar, 0).click().perform()
        option=self.browser.find_element_by_xpath('//*[@id="product-selection-form"]/div[1]/div[5]/div[2]/img')
        actionChains.move_to_element_with_offset(option,offset_term_x,offset_term_y).click().perform()    

    def fill_prepage(self, name, id, phone='1234567'):
        self.browser.find_element_by_xpath('//*[@id="name"]').send_keys(name)
        self.browser.find_element_by_xpath('//*[@id="phone"]').send_keys(phone)
        self.browser.find_element_by_xpath('//*[@id="idNum"]').send_keys(id)
        # Bankcard information
        self.browser.find_element_by_xpath('//*[@id="bankCard"]').send_keys('0000000000000000000')
        province = Select(self.browser.find_element_by_xpath('//*[@id="bankIssuingProvince"]'))
        province.select_by_visible_text("Tianjin")
        time.sleep(2)
        city = Select(self.browser.find_element_by_xpath('//*[@id="bankIssuingCity"]'))
        city.select_by_visible_text("Tianjin")
        time.sleep(2)
        bank = Select(self.browser.find_element_by_xpath('//*[@id="branchBanks"]'))
        bank.select_by_visible_text("xxxx")
        # SMS Verification and click button
        self.browser.find_element_by_xpath('//*[@id="divSwitchSamePhoneNumber"]').click()
        self.browser.find_element_by_xpath('//*[@id="btnSendVerificationCode"]').click()
        self.browser.find_element_by_xpath('//*[@id="verificationCode"]').send_keys('12345')
        self.browser.find_element_by_xpath('//*[@id="btnSubmit"]').click()

    def fill_1BOD(self, idfront, idback, email, marital_status='Single', career='Service', loan='Consumption'):
        self.browser.find_element_by_xpath('//*[@id="idCardFrontInput"]').send_keys(idfront)
        self.browser.find_element_by_xpath('//*[@id="idCardBackInput"]').send_keys(idback)
        # Fill in current address
        province = Select(self.browser.find_element_by_xpath('//*[@id="province"]'))
        province.select_by_visible_text("Beijing")
        time.sleep(2)
        city = Select(self.browser.find_element_by_xpath('//*[@id="city"]'))
        city.select_by_visible_text("Beijing")
        time.sleep(2)
        district = Select(self.browser.find_element_by_xpath('//*[@id="district"]'))
        district.select_by_visible_text("Chaoyang District")
        self.browser.find_element_by_xpath('//*[@id="town"]').send_keys('current town')
        self.browser.find_element_by_xpath('//*[@id="street"]').send_keys('current street')
        self.browser.find_element_by_xpath('//*[@id="houseNum"]').send_keys('current houseNum')
        self.browser.find_element_by_xpath('//*[@id="apartment"]').send_keys('current apartmentNum')
        # Fill in personal information
        self.browser.find_element_by_xpath('//*[@id="email"]').send_keys(email)
        married = Select(self.browser.find_element_by_xpath('//*[@id="individualStatus"]'))
        married.select_by_visible_text(marital_status)
        time.sleep(2)
        occupation = Select(self.browser.find_element_by_xpath('//*[@id="occupation"]'))
        occupation.select_by_visible_text(career)
        time.sleep(2)
        self.browser.find_element_by_xpath('//*[@id="salary"]').send_keys('8000')
        purpose = Select(self.browser.find_element_by_xpath('//*[@id="loanUsage"]'))
        purpose.select_by_visible_text(loan)
        # Fill in family information
        self.browser.find_element_by_xpath('//*[@id="relativeName"]').send_keys('Usain Bolt')
        relation = Select(self.browser.find_element_by_xpath('//*[@id="relationship"]'))
        relation.select_by_visible_text('Mother')
        self.browser.find_element_by_xpath('//*[@id="relativePhoneShow"]').send_keys('12345678909')
        # Click Button
        self.browser.find_element_by_xpath('//*[@id="btnNext"]').click()

    def fill_2BOD(self, education='University', apart_status='Rented', len='Under a year', industry='real estate', company='state owned'):
        # Fill in supplementary information
        edu = Select(self.browser.find_element_by_xpath('//*[@id="education"]'))
        edu.select_by_visible_text(education)
        apart = Select(self.browser.find_element_by_xpath('//*[@id="apartmentStatus"]'))
        apart.select_by_visible_text(apart_status)
        month = Select(self.browser.find_element_by_xpath('//*[@id="residenceMonth"]'))
        month.select_by_visible_text(len)
        self.browser.find_element_by_xpath('//*[@id="householdIncome"]').send_keys('10000')
        self.browser.find_element_by_xpath('//*[@id="monthlyExpenses"]').send_keys('1000')
        self.browser.find_element_by_xpath('//*[@id="childrenNum"]').send_keys('0')
        self.browser.find_element_by_xpath('//*[@id="areaCodeOfHomePhone"]').send_keys('020')
        self.browser.find_element_by_xpath('//*[@id="homePhone"]').send_keys('88888888')
        # Fill in supplementary contact
        self.browser.find_element_by_xpath('//*[@id="secondaryContactsName"]').send_keys('King')
        relation = Select(self.browser.find_element_by_xpath('//*[@id="secondaryContactsRelationship"]'))
        relation.select_by_visible_text('colleague')
        self.browser.find_element_by_xpath('//*[@id="secondaryContactsPhoneShow"]').send_keys('13800000001')
        # Fill in employment information
        self.browser.find_element_by_xpath('//*[@id="unitName"]').send_keys('company name')
        self.browser.find_element_by_xpath('//*[@id="areaCodeOfEmployer"]').send_keys('020')
        self.browser.find_element_by_xpath('//*[@id="unitTelephone"]').send_keys('88888887')
        indust = Select(self.browser.find_element_by_xpath('//*[@id="industry"]'))
        indust.select_by_visible_text(industry)
        time.sleep(2)
        comp = Select(self.browser.find_element_by_xpath('//*[@id="unitCharacter"]'))
        comp.select_by_visible_text(company)
        self.browser.find_element_by_xpath('//*[@id="department"]').send_keys('position')
        self.browser.find_element_by_xpath('//*[@id="entryTime"]').click()
        self.browser.find_element_by_xpath('/html/body/div[2]/div[4]/table/tbody/tr/td/span[1]').click()
        total = Select(self.browser.find_element_by_xpath('//*[@id="workingAge"]'))
        total.select_by_visible_text('1-2 year')
        # Fill in employer's address
        province = Select(self.browser.find_element_by_xpath('//*[@id="unitProvince"]'))
        province.select_by_visible_text("Beijing")
        time.sleep(2)
        city = Select(self.browser.find_element_by_xpath('//*[@id="unitCity"]'))
        city.select_by_visible_text("Beijing")
        time.sleep(2)
        district = Select(self.browser.find_element_by_xpath('//*[@id="unitDistrict"]'))
        district.select_by_visible_text("Chaoyang District")
        self.browser.find_element_by_xpath('//*[@id="town"]').send_keys('employer\'s town')
        self.browser.find_element_by_xpath('//*[@id="street"]').send_keys('employer\'s street')
        self.browser.find_element_by_xpath('//*[@id="houseNum"]').send_keys('employer\'s houseNum')
        self.browser.find_element_by_xpath('//*[@id="apartmentNum"]').send_keys('employer\'s apartmentNum')
        self.browser.find_element_by_xpath('//*[@id="btnNext"]').click()

    def fill_3BOD(self, selfie):
        self.browser.find_element_by_xpath('//*[@id="idSelfieInput"]').send_keys(selfie)
        time.sleep(2)
        self.browser.find_element_by_xpath('//*[@id="btnVerifyIdentity"]').click()
        time.sleep(2)
        self.browser.find_element_by_xpath('//*[@id="btnSendVerificationCode"]').click()
        self.browser.find_element_by_xpath('//*[@id="verificationCode"]').send_keys(self.get_sms())
        self.browser.find_element_by_xpath('//*[@id="btnSubmit"]').click()

    def get_sms(phone=1234567):
        query = "SELECT * FROM MSGSRV.MSG_SMS_FAX_DATA M " \
                "WHERE M.ID > 0000000 AND M.RECIPIENT = '%s' " \
                "order by m.ins_time desc" % phone
        table = pd.read_sql(query, self.engine)
        message = table['message'][0]
        sms = findall('\d{6}', message)[0]
        return sms


    def main(self):
        self.fill_prepage(name='xxx', id='000000')
        time.sleep(3)
        self.fill_1BOD('K:\Public\xxx.JPG',
                       'K:\Public\xxx.JPG', email='xxxx@xxx.cn')
        time.sleep(2)
        self.fill_2BOD()
        time.sleep(5)
        self.fill_3BOD('D:\Inbox\xxx.jpg')


if __name__ == '__main__':
    c = UATRobot("https://xxx.cn/mock.do")
    # c.main()