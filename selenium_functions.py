#####################################################
#                Installed modules                  #
#####################################################
import pandas as pd


#####################################################
#                Selenium libraries                 #
#####################################################
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, TimeoutException



#####################################################
#         custom selenium functions                 #
#####################################################
def scrape_vendors(url):

    try:
        # install chromedriver if not installed
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(url)
        driver.set_page_load_timeout(500)

        driver.implicitly_wait(15)

        # get class selector for all vendors
        vendors = driver.find_elements_by_class_name('column.is-3-desktop.is-12-mobile.is-6-tablet.r-card.slide-card')

        # list to hold all vendors
        vendor_details = []

        for vendor in vendors:
            
            try:
                
                # get vendor details
                vendor_link = vendor.find_element_by_tag_name('a').get_attribute('href')
                vendor_name = vendor.find_element_by_class_name('top-info').find_element_by_class_name('name').get_attribute('innerHTML')
                description =  vendor.find_element_by_class_name('bottom-info').find_elements_by_tag_name('span')
                
                vendor_rating = f"{description[0].get_attribute('innerHTML')}stars".replace(
                            '<i class="fa fa-star-o mrxs"></i>', '').replace('&nbsp;', '').replace('•','') 
                
                vendor_description = description[-1].text
                
                if vendor_description == '':
                    vendor_description = description[-1].get_attribute('innerHTML')
                    
                vendor_details.append([vendor_name, vendor_link, vendor_rating, vendor_description])
                print(vendor_name, vendor_link, vendor_rating, vendor_description)

            except NoSuchElementException:
                pass
        
        # convert scraped data to dataframe
        vendors_df = pd.DataFrame(vendor_details, columns = ["Vendor names", "Vendor links", "Vendor ratings", "Vendor descriptions"])

        return vendors_df

    # exceptions for errors
    except NoSuchElementException as e:
        print(f"\nAn error occured : {e}") 
        driver.close()
        
    
    except ElementNotInteractableException as e:
        print(f"\nAn error occured : {e}") 
        driver.close()
        
        
    except TimeoutException as e:
        print(f"\nAn error occured : {e}") 
        driver.close()
        

    except:
        print(f"\n An Unknown error occured!") 
        driver.close()
        

 


def scrape_menu(vendor):

    try:

        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(vendor)
        driver.set_page_load_timeout(500)
        
        dish_category = driver.find_elements_by_class_name('menu-category-section.mtxxl')
        
        # list to hold all dishes
        dishes = []

        #get dish category
        for dish in dish_category:
            
            driver.implicitly_wait(10)

            # get and clean category name
            category = dish.find_element_by_class_name('bull-bfr.bull-aft.category-title').get_attribute(
                        "innerHTML").replace("&amp;", "").replace("\n", "").replace("/", "").strip(' ')
            
            
            # get category product list
            dish_lists = dish.find_element_by_class_name('category-product-list').find_elements_by_class_name('product-card')

            for dish_list in dish_lists:
                
                driver.implicitly_wait(5)
                dish_name = dish_list.find_element_by_class_name('product-title').find_element_by_tag_name('span').get_attribute(
                            "innerHTML").replace("&amp;", "").replace("\n", "").strip(' ')
                
                driver.implicitly_wait(5)
                dish_price = driver.find_element_by_css_selector('span.mlxs.fsh-0').get_attribute("innerHTML").replace("\n", "").strip(' ')
                
                driver.implicitly_wait(5)
                
                # try block to handle dishes with no description
                try:
                    dish_description = dish_list.find_element_by_css_selector('p.product-description.has-text-grey').get_attribute(
                                "innerHTML").replace("\n", "").replace("&amp;", "")
                except NoSuchElementException as e:
                    dish_description = ' '
                
                print(dish_name, dish_price, dish_description)

                dishes.append([category, dish_name, dish_price, dish_description])

        # convert data to dataframe
        menu_df = pd.DataFrame(dishes, columns=['Category', 'Dish name', 'Dish price','Dish description'])
   
        return menu_df

    # exceptions for errors
    except NoSuchElementException as e:
        print(f"\nAn error occured : {e}") 
        driver.close()
    
    except ElementNotInteractableException as e:
        print(f"\nAn error occured : {e}") 
        driver.close()
        
    except TimeoutException as e:
        print(f"\nAn error occured : {e}") 
        driver.close()

    except:
        print(f"\n An Unknown error occured!") 
        driver.close()
    

