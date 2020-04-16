from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from getpass import getpass
import sys
import time
import si_to_int
import csv

option = Options()

#Adding attributes to the browser to be openned
option.add_argument('--disable-infobars')
option.add_argument('start-maximized')
option.add_argument('--disable-extensions')
option.add_argument('--disable-notifications')

#Click 'Block' option on browser notification that asks for 'Push notifications' permission
option.add_experimental_option('prefs', { 'profile.default_content_setting_values.notifications': 2})   

print('Provide your login credentials!')

username = input('Enter your username: ')


password = getpass()
targetUsername = input("Enter target's username: ")


#Number of users followed
followed = 0

browser = webdriver.Chrome(options=option)

followedCheck = 0 #Check for number of accounts unfollowed

#Adding a delay, and waiting for the element to be loaded
delay = 10
wait = WebDriverWait(browser, delay)

browser.get('https://www.instagram.com/accounts/login/?next=%2F{}%2F&source=desktop_nav'.format(username))


time.sleep(4)


try:
    #Referencing text box that asks for email
    usernameInput = browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[2]/div/label/input')
    usernameInput.send_keys(username)
    
    #Referencing text box that asks for password
    passwordInput = browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[3]/div/label/input')
    passwordInput.send_keys(password)

    #Referencing Login Button
    loginButton = browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]/button')
    loginButton.click()

    time.sleep(4)

    try:
        
        #Looking for a login error message
        errorMessagePresent = browser.find_element_by_xpath('//*[@id="slfErrorAlert"]')
      
        print('Wrong Credentials :(')
        sys.exit() #exit the program

    except  (NoSuchElementException, TimeoutException) as exception:

        print('Successfuly Loggedin :)')  
          

except (NoSuchElementException, TimeoutException) as exception:


    try:

        #Referencing text box that asks for email
        usernameInput = browser.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[2]/div/label/input')
        usernameInput.send_keys(username)
    
        #Referencing text box that asks for password
        passwordInput = browser.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[3]/div/label/input')
        passwordInput.send_keys(password)

        #Referencing Login Button
        loginButton = browser.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[4]/button')
        loginButton.click()

        time.sleep(4)

        try:
        
            #Looking for a login error message
            errorMessagePresent = browser.find_element_by_xpath('//*[@id="slfErrorAlert"]')
      
            print('Wrong Credentials :(')
            sys.exit() #exit the program

        except  (NoSuchElementException, TimeoutException) as exception:

            print('Successfuly Loggedin :)')  
          

    except (NoSuchElementException, TimeoutException) as exception:
    
        print("Slow Or No Connection :(")
        sys.exit()


try:

    browser.get('https://www.instagram.com/{}/'.format(targetUsername)) #Openning target's profile

    try:
        
        privateAccountMessage = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/section/main/div/div/article/div/div/h2')))

        print('This account is private!')
        sys.exit()

    except (NoSuchElementException, TimeoutException) as exception:

        #Getting the totals number of followers out target user has
        numberOfFollowers = browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span')

        followers = numberOfFollowers.text

        #Converting Units 'k', 'm' and 'b' into numbers
        followers = si_to_int.convert_si_to_number(followers)

        print(followers)
    
except (NoSuchElementException, TimeoutException) as exception:
    
    print("Slow Or No Connection :(")
    sys.exit()

followersList = ['']


try:
    
    followersSection = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a')))
    followersSection.click()

    time.sleep(2)

    followersPopup = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, "//div[@class='isgrP']")))

    for followedCheck in range(1, followers):
        
        try:

            #Changing xpath for 'followButton' and 'usernameFollowed' after scroll 
            if followedCheck <= 6:

                
                usernameFollowed = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div[2]/ul/div/li[{}]/div/div[2]/div[1]/div/div/a'.format(followedCheck))))
                                                                                                      
            else:

                usernameFollowed = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div[2]/ul/div/li[{}]/div/div[1]/div[2]/div[1]/a'.format(followedCheck))))
                

            followersList.append(usernameFollowed.text)

            #Scrolling on Followers popup after unfollowing 7 users every time
            if followedCheck % 6 == 0:  
                browser.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', followersPopup)
                print('Scrolling...')
                time.sleep(3)
                

        except (NoSuchElementException, TimeoutException) as exception:
            
            #Break the loop if there are no more accounts being followed
            print('Some error occured :(')
            break
        
except (NoSuchElementException, TimeoutException) as exception:
    print('Slow Or No Connection :(')


def saveUsersList(usersList , targetusername):

    with open(targetusername + '.csv','wt', newline = '') as result_file:

        wr = csv.writer(result_file)

        for user in usersList:

            wr.writerow([user])

saveUsersList(followersList, targetUsername)