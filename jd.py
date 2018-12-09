from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import time
import random


def if_is_s(img_1, img_2):
    a = 0
    for i in range(1, img_1.size[1]):
        for j in range(1, 3):
            rgb1 = img_1.load()[i, j]
            rgb2 = img_2.load()[i, j]
            res1 = abs(rgb1[0] - rgb2[0])
            res2 = abs(rgb1[1] - rgb2[1])
            res3 = abs(rgb1[2] - rgb2[2])
            if res1 < 10 and res2 < 10 and res3 < 10:
                a += 1
            else:
                a = 0
            if a > 50:
                return True
    return False
def get_distance(image1,image2):
    a = 0
    threshold=60
    left=57
    for i in range(left,image1.size[0]):
        for j in range(image1.size[1]):
            rgb1=image1.load()[i,j]
            rgb2=image2.load()[i,j]
            res1=abs(rgb1[0]-rgb2[0])
            res2=abs(rgb1[1]-rgb2[1])
            res3=abs(rgb1[2]-rgb2[2])
            if not (res1 < threshold and res2 < threshold and res3 < threshold):
                a += 1
                return i+20
    return i+20


def get_tracks(distance):
    tracks = []
    current = 0
    mid = distance * 4 / 5
    t = 0.2
    v = 0
    while current < distance:
        if current < mid:
            a = random.uniform(2, 5)
        else:
            a = -(random.uniform(12.5, 13.5))
        v0 = v
        v = v0 + a * t
        x = v0 * t + 1 / 2 * a * (t ** 2)
        current += x
        if 0.6 < current - distance < 1:
            x = x - 0.53
            tracks.append(round(x, 2))
        elif 1 < current - distance < 1.5:
            x = x - 1.4
            tracks.append(round(x, 2))
        elif 1.5 < current - distance < 3:
            x = x - 1.8
            tracks.append(round(x, 2))
        else:
            tracks.append(round(x, 2))
    if sum(tracks) > distance:
        i = sum(tracks) - distance
        tracks[-1] = round(tracks[-1] - i, 2)
    i = random.uniform(1, 3  )
    i = round(i, 2)
    zz = random.uniform(0.1, 0.3)
    tracks[-1] = round(tracks[-1] + i, 2)
    i = round(i - zz, 2)
    tracks.append(-i)
    if sum(tracks) < distance:
        si = distance - sum(tracks)
        tracks.append(round(si, 2))
    print(tracks, sum(tracks))
    return tracks


if __name__=='__main__':
    browser = webdriver.Firefox()
    browser.get('https://passport.jd.com/new/login')
    butt = WebDriverWait(browser,10).until(EC.presence_of_element_located((By.CLASS_NAME,'link-login')))
    butt.click()
    butt = WebDriverWait(browser,10).until(EC.presence_of_element_located((By.XPATH,'//a[@clstag="pageclick|keycount|login_pc_201804112|10"]')))
    butt.click()
    user = WebDriverWait(browser,10).until(EC.presence_of_element_located((By.ID,'loginname')))
    password = WebDriverWait(browser,10).until(EC.presence_of_element_located((By.ID,'nloginpwd')))
    user.send_keys('xxx')
    time.sleep(2)
    password.send_keys('xxx')
    izsz = 1
    while izsz == 1:
        try:
            button = WebDriverWait(browser,10).until(EC.presence_of_element_located((By.CLASS_NAME,'btn-img.btn-entry')))
            time.sleep(2)
            button.click()
            time.sleep(2)
            browser.save_screenshot('1.png')
            page_snap_obj = Image.open('1.png')
            img = WebDriverWait(browser,10).until(EC.presence_of_element_located((By.CLASS_NAME,'JDJRV-bigimg')))
            local = img.location
            size = img.size
            top = local['y']
            bottom = local['y'] + size['height']
            left = local['x']
            right = local['x'] + size['width']
            img_1 = Image.open('index2.png')
            img_2 = page_snap_obj.crop((left, top, right, bottom))
            img_2.save('2.png')
            i = if_is_s(img_1,img_2)
            while not i:
                time.sleep(2)
                butt = WebDriverWait(browser,10).until(EC.presence_of_element_located((By.CLASS_NAME,'JDJRV-img-refresh')))
                butt.click()
                time.sleep(2)
                browser.save_screenshot('1.png')
                page_snap_obj = Image.open('1.png')
                img = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'JDJRV-bigimg')))
                local = img.location
                size = img.size
                top = local['y']
                bottom = local['y'] + size['height']
                left = local['x']
                right = local['x'] + size['width']
                img_1 = Image.open('index2.png')
                img_2 = page_snap_obj.crop((left, top, right, bottom))
                img_2.save('2.png')
                time.sleep(2)
                i = if_is_s(img_1, img_2)
            ji = get_distance(img_1, img_2)
            print(ji)
            tracks = get_tracks(ji)
            ijs = len(tracks)//5*3
            tracks1 = tracks[:ijs]
            tracks2 = tracks[ijs:]
            z = sum(tracks1)
            tracks2.insert(0,z)
            tracks2.insert(0,0)
            button = WebDriverWait(browser,10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="JDJRV-slide-inner JDJRV-slide-btn"]')))
            ActionChains(browser).click_and_hold(button).perform()
            for track in tracks:
                ActionChains(browser).move_by_offset(xoffset=track, yoffset=0).perform()

            time.sleep(0.5)  # 0.5秒后释放鼠标
            ActionChains(browser).release().perform()
            url = browser.current_url
            if 'https://passport.jd.com/new/login.aspx?' in str(url):
                izsz = 1
            else:
                izsz = 0
        except:
            izsz = 1



