from selenium import webdriver
from selenium.webdriver.common.by import By
import pickle
import os
from time import sleep

resume = ''
search_url = ''

if not search_url:
    raise Exception('Please provide a search URL')

if not resume:
    raise Exception('Please provide a cover letter')

def apply_in_page(driver):
    vakancies = driver.find_elements(By.CLASS_NAME, 'serp-item')

    for vakancy in vakancies:
        try:
            apply_btn = vakancy.find_element(By.CLASS_NAME, 'serp-item-controls').find_element(By.TAG_NAME, 'a')
            apply_btn.click()
            sleep(5)
            add2resume = vakancy.find_element(By.CLASS_NAME, 'bloko-link.bloko-link_pseudo')
            add2resume.click()
            textarea = vakancy.find_element(By.TAG_NAME, 'textarea')
            textarea.send_keys(resume)
            submit_btn = vakancy.find_element(By.CLASS_NAME, 'bloko-button.bloko-button_kind-primary')
            submit_btn.click()



        except Exception as e:
            if not driver.current_url.startswith('https://hh.ru/search'):
                driver.back()
            print(e)
            continue


def main():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    driver = webdriver.Chrome()#options=options)
    url = 'https://hh.ru'
    driver.get(url)

    if os.path.exists('cookies'):
        for cookie in pickle.load(open('cookies', 'rb')):
            driver.add_cookie(cookie)
    else:

        # auth and save cookies
        signin = driver.find_element('xpath', '//*[@id="HH-React-Root"]/div/div[2]/div/div/div/div/div[5]/a')
        signin.click()

        # login field
        login_input = driver.find_element('xpath',
                                          '//*[@id="HH-React-Root"]/div/div[3]/div[1]/div/div/div/div/div/div[1]/div[1]/div[1]/div/div[2]/div/form/div[1]/fieldset/input')
        login_input.clear()
        email = input('Введите email: ')
        login_input.send_keys(email)
        # sleep(3)
        continue_btn = driver.find_element('xpath',
                                           '//*[@id="HH-React-Root"]/div/div[3]/div[1]/div/div/div/div/div/div[1]/div[1]/div[1]/div/div[2]/div/form/div[5]/button[1]')
        continue_btn.click()
        sleep(3)
        code_input = driver.find_element(By.NAME, 'otp-code-input')
        code_input.clear()
        code = input('Введите код для подтверждения:  ')
        code_input.send_keys(code)

        confirm_btn = driver.find_element('xpath',
                                          '//*[@id="HH-React-Root"]/div/div[3]/div[1]/div/div/div/div/div/div/div/div/div/div/div/form/div/div[7]')
        confirm_btn.click()

        print('Запись куки')
        pickle.dump(driver.get_cookies(), open('cookies', 'wb'))

    driver.get(search_url)

    sleep(2.5)
    apply_in_page(driver)
    try:
        continue_btn_for_page = driver.find_element(By.CLASS_NAME, 'bloko-button')
        continue_btn_for_page.click()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
