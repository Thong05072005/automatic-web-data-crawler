from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os




def crawl_tgdd():
    try:
        options = Options()# Khởi tạo Chrome
        # options.add_argument('--headless')  # Chạy ẩn chrome
        driver = webdriver.Chrome(options=options)
        driver.get("https://www.thegioididong.com/dtdd")
        time.sleep(2)
        #Ấn nút xem thêm đến khi load hết sản phẩm
        while True:
            try:
                button = driver.find_element(By.CSS_SELECTOR, ".view-more a")
                button.click()
                time.sleep(2)
            except:
                print("Đã load hết tất cả sản phẩm!")
                break
        #Lấy thông tin sản phẩm
        products = driver.find_elements(By.CSS_SELECTOR, "li.item.ajaxed.__cate_42")
        product_links = []
        product_name=[]
        data=[]
        for i, p in enumerate(products):
            try:
                #Lấy tên sản phẩm
                name = p.find_element(By.CSS_SELECTOR, "h3").text
                #Lấy link chi tiết cửa từng sản phẩm
                link = p.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                product_name.append(name)
                product_links.append(link)
            except:
                continue
        print(f"Đã thu được {len(product_links)} link sản phẩm.")
        for i,p in enumerate(products):
                print('----------------------------------------------------')
                #Truy cập link chi tiết của từng sản phẩm
                driver.get(product_links[i])
                time.sleep(2)  # chờ trang tải
                #Lấy toàn bộ mã html trong trang
                page_source = driver.page_source
                # Sử dụng BeautifulSoup để phân tích mã nguồn HTML
                prod_soup = BeautifulSoup(page_source, "html.parser")
                #Lấy giá sản phẩm
                price_tag = prod_soup.select_one(".bs_price strong")
                try:
                    if not price_tag:
                        price_tag = prod_soup.select_one(".item.cf-left b b")
                        price = price_tag.get_text(strip=True) if price_tag else prod_soup.select_one(".box-price-present").get_text(strip=True)
                except:
                    continue
                print(i)
                print(product_name[i])
                print(price)
                text_content=""
                lines=""
                #Lấy thẻ chứa thông tin về sản phẩm dạng thứ nhất
                if prod_soup.select_one('ul.parameter'):
                    text_content=prod_soup.select_one('ul.parameter').get_text(separator="\n",strip=True)
                    lines = text_content.split('\n')
                #Lấy thẻ chứa thông tin về sản phẩm dạng thứ hai
                #Dạng hai muốn có thông tin về camera thì phải tạo sự kiện click vào phần xem camera (nằm ở thẻ có class=box-specifi thứ hai)
                else:
                    try:
                        button = WebDriverWait(driver,1).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, ".specification-item .box-specifi:nth-child(2)"))
                        )
                        button.click()
                        time.sleep(1)
                    except:
                            continue
                    #Lấy thông tin từ các thẻ chứa thông tin sản phẩm (ít nhất là hai thẻ)
                    divs = prod_soup.select('.box-specifi')
                    #Kiểm tra có lấy được đủ thông tin chưa
                    if len(divs) >= 2:
                        #Lấy nội dung trong các thẻ trên
                        text_content = divs[0].get_text(separator="\n", strip=True)+'\n'
                        text_content+=divs[1].get_text(separator="\n", strip=True)
                        #Tạo mảng các dữ liệu đã lấy dựa trên kí tự xuống dòng
                        lines = text_content.split('\n')
                ram_value = "Không hỗ trợ"
                camera_value="Không hỗ trợ"
                memory_value="Không hỗ trợ"
                rate="Chưa có đánh giá"
                #Lấy thông tin từ mảng lines
                for j, line in enumerate(lines):
                    if 'RAM:' == line.upper():  # Dùng .upper() để tránh sai lệch do chữ hoa/thường
                            ram_value = lines[j + 1]

                    if 'DUNG LƯỢNG LƯU TRỮ' in line.upper():
                            memory_value = lines[j + 1]
                
                    if 'ĐỘ PHÂN GIẢI CAMERA SAU' in  line.upper()or 'CAMERA SAU:' ==  line.upper():
                            camera_value=lines[j + 1]

                print("RAM:", ram_value)
                print("DUNG LƯỢNG LƯU TRỮ:", memory_value)
                print("CAMERA:",camera_value)
                find_rate=prod_soup.find(class_='point-average-score')
                if find_rate:
                    rate=find_rate.get_text(strip=True)
                print("Đánh giá:",rate)
                print(product_links[i])
                data.append({
                        "Tên sản phẩm": product_name[i],
                        "Giá bán": price,
                        "RAM":ram_value,
                        "Bộ nhớ trong": memory_value,
                        "Camera": camera_value,
                        "Đánh giá": rate,
                        "Đường dẫn":product_links[i]
                })
                # Xuất file Excel

                os.makedirs("../data", exist_ok=True)
                df = pd.DataFrame(data)
                file_name = f"../data/tgdd_dienthoai_{datetime.now().strftime('%Y%m%d')}.xlsx"
                df.to_excel(file_name, index=False)
                print(f"Crawl hoàn tất! Đã lưu vào: {file_name}")
        driver.quit()
    except Exception as e:
        print(f"[X] Lỗi không thể truy cập trang chính: {e}")

# Lập lịch chạy mỗi ngày lúc 9 giờ sáng
# schedule.every().day.at("08:39").do(crawl_tgdd)
# print("Đang chạy lịch...")
# while True:
#     schedule.run_pending()
#     time.sleep(60)
crawl_tgdd()