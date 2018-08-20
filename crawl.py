
from selenium import webdriver
import time
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import pandas as pd
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

#chromdriver의 위치를 지정
driver = webdriver.Chrome("/Users/seong/Downloads/chromedriver_win32/chromedriver")
#phantomJS의 위치를 지정

#암묵적으로 웹 자원 로드를 위해 3초 기다려준다.
driver.implicitly_wait(3)

#url에 접근
#URL에 접근하는 API    -> get.('http://url.com')
driver.get('https://chams.cju.ac.kr/')

#아이디/비밀번호
#페이지 단일 element에 접근하는 api -> (1)find_element_by_name('HTML_name') (2)find_element_by_id('HTML_id') (3)find_element_by_xpath('/html/body/some/xpath')
#페이지 여러 element에 접근하는 api -> (1)find_element_by_css_selector('#css > div.selector') (2)find_element_by_class_name('some_class_name') (3)find_element_by_tag_name('h1')
driver.find_element_by_xpath('/html/body/form/table/tbody/tr[1]/td[2]/table/tbody/tr[1]/td/table/tbody/tr[2]/td[2]/input').send_keys('')
driver.find_element_by_xpath('/html/body/form/table/tbody/tr[1]/td[2]/table/tbody/tr[1]/td/table/tbody/tr[3]/td[2]/input').send_keys('')

#확인 버튼
driver.find_element_by_xpath('/html/body/form/table/tbody/tr[1]/td[2]/table/tbody/tr[1]/td/table/tbody/tr[4]/td/a[1]').click()

#상단 frame에서 수업 클릭
driver.switch_to.frame(driver.find_element_by_name("TF"))
driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[4]/font/a[2]').click()

#접속한 frame 탈출
driver.switch_to_default_content()

#하단 좌측 frame에서 개설강좌조회 클릭
driver.switch_to.frame(driver.find_element_by_name("LF"))
driver.find_element_by_xpath('/html/body/table[17]/tbody/tr/td[2]/div/a').click()

#접속한 frame 탈출
driver.switch_to_default_content()

#하단 우측 frame 접속
driver.switch_to.frame(driver.find_element_by_name("RF"))

#하단 우측 frame의 상단 frame접속
driver.switch_to.frame(driver.find_element_by_name("RTF"))

html = driver.page_source
soup = BeautifulSoup(html,'html.parser')

#전공
part = Select(driver.find_element_by_name("part"))

for numpart in range(1,len(part.options)):
    part = Select(driver.find_element_by_name("part"))
    part.select_by_index(numpart)
    time.sleep(5)

    #전공/ 교양 필수
    if numpart == 1 or numpart == 2:
        colg = Select(driver.find_element_by_name("colg"))
        #단대 / 학과
        for numcolg in range(1,len(colg.options)):
            colg = Select(driver.find_element_by_name("colg"))
            colg.select_by_index(numcolg)
            #선택한 옵션의 텍스트값
            #x = colg.first_selected_option.get_attribute('text')

            time.sleep(5)

            sust = Select(driver.find_element_by_name("sust"))
            for numsust in range(1,len(sust.options)):
                sust.select_by_index(numsust)
                indexnumber = 1
                #선택한 옵션의 텍스트값
                #y = sust.first_selected_option.get_attribute('text')

                #조회 버튼 클릭
                driver.find_element_by_xpath("/html/body/form/center/table[2]/tbody/tr[1]/td[5]/input").click()

                #하단 frame으로 접속
                driver.switch_to_default_content()
                driver.switch_to.frame(driver.find_element_by_name("RF"))
                driver.switch_to.frame(driver.find_element_by_name("RBF"))

                #DATA 긁어오기
                contents = soup.find_all("tr",{"tr_0","tr_1"})
                num = len(contents)

                #DataFrame 생성
                result = pd.DataFrame(columns=['A','B','C','D','E','F'],index = range(1,num))

                for content in contents:
                    predata = []
                    data=[]
                    tdata = content.find_all("td",class_="k_tdline")
                    for td in tdata:
                        predata.append(td.get_text().split('\n '))
                    #data 한줄 긁기
                    data.append(predata)
                                                #학년-반    학수번호   교과목명     담당교수   학점      강의시간/강의실   개설학과
                    result.loc[indexnumber] = [data[0][0],data[0][2],data[0][4],data[0][6],data[0][10],data[0][11]]
                    #result라는 DataFrame명을 각 과이름으로 변수명 변경
                    #title = result.copy()
                    #print(title)
                    indexnumber += 1
                    #time.sleep(1)
                #print(x+y)#학과 변경하기위해 상위frame으로 접속
                driver.switch_to_default_content()
                driver.switch_to.frame(driver.find_element_by_name("RF"))
                driver.switch_to.frame(driver.find_element_by_name("RTF"))
                #time.sleep(1)
            colg=Select(driver.find_element_by_name("colg"))
            time.sleep(5)
        part = Select(driver.find_element_by_name("part"))
        part.select_by_index(0)
        time.sleep(1)


    elif numpart == 3:
        section = Select(driver.find_element_by_name("section"))
        for numsec in range(1,len(section.options)):
            section = Select(driver.find_element_by_name("section"))
            section.select_by_index(numsec)
            indexnumber = 1
            #조회 버튼
            driver.find_element_by_xpath("/html/body/form/center/table[2]/tbody/tr[1]/td[5]/input").click()

            #하단 frame으로 접속
            driver.switch_to_default_content()
            driver.switch_to.frame(driver.find_element_by_name("RF"))
            driver.switch_to.frame(driver.find_element_by_name("RBF"))
            #DATA 긁어오기
            contents = soup.find_all("tr",{"tr_0","tr_1"})
            num = len(contents)
            #DataFrame 생성

            result = pd.DataFrame(columns=['A','B','C','D','E','F'],index = range(1,num))
            for content in contents:
                predata = []
                data=[]
                tdata = content.find_all("td")
                for td in tdata:
                    predata.append(td.get_text().split('\n '))
                #data 한줄 긁기
                data.append(predata)

                                            #학수번호   교과목명     담당교수   학점      강의시간       강의실
                result.loc[indexnumber] = [data[0][1],data[0][3],data[0][4],data[0][8],data[0][9],data[0][10]]
                #result라는 DataFrame명을 각 과이름으로 변수명 변경

                #title = result.copy()
                #print(title)

                indexnumber += 1

            driver.switch_to_default_content()
            driver.switch_to.frame(driver.find_element_by_name("RF"))
            driver.switch_to.frame(driver.find_element_by_name("RTF"))
        part = Select(driver.find_element_by_name("part"))
        part.select_by_index(0)
        time.sleep(1)

    #이수 구분이 교직
    elif numpart == 4 or numpart == 5 or numpart == 6 or numpart ==7:
        indexnumber = 1
        #조회 버튼
        driver.find_element_by_xpath("/html/body/form/center/table[2]/tbody/tr[1]/td[5]/input").click()

        #하단 frame으로 접속
        driver.switch_to_default_content()
        driver.switch_to.frame(driver.find_element_by_name("RF"))
        driver.switch_to.frame(driver.find_element_by_name("RBF"))
        #data 긁기
        contents = soup.find_all("tr",{"tr_0","tr_1"})
        num = len(contents)
        #DataFrame 생성
        result = pd.DataFrame(columns=['A','B','C','D','E'],index = range(1,num))
        for content in contents:
            predata = []
            data=[]
            tdata = content.find_all("td")
            for td in tdata:
                predata.append(td.get_text().split('\n '))
            #data 한줄 긁기
            data.append(predata)
                                      #학수번호   교과목명     담당교수   학점      강의시간       강의실
            result.loc[indexnumber] = [data[0][2],data[0][4],data[0][6],data[0][10],data[11]]
            #result라는 DataFrame명을 각 과이름으로 변수명 변경
            #title = result.copy()
            #print(title)
            indexnumber += 1
        driver.switch_to_default_content()
        driver.switch_to.frame(driver.find_element_by_name("RF"))
        driver.switch_to.frame(driver.find_element_by_name("RTF"))

        part = Select(driver.find_element_by_name("part"))
        part.select_by_index(0)
        time.sleep(1)
