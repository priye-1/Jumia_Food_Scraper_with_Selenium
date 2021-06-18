#####################################################
#                Installed modules                  #
#####################################################
import gspread
import pandas as pd
from df2gspread import df2gspread as d2g
from df2gspread import gspread2df as g2d
from oauth2client.service_account import ServiceAccountCredentials


#####################################################
#         custom selenium functions                 #
#####################################################
from selenium_functions import scrape_vendors, scrape_menu









################################# Script Execution starts here #########################################



if __name__ == '__main__':
    
    # define scope for googlesheet api
    scope = ['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']

    # Authentication for google sheets api
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        'client_secret.json', scope)   

    #gspread to communicate directly to the sheet
    gc = gspread.authorize(credentials)

    gfile = "1yzAnR0zWVaPhMnHAkYym7UwBazQqbjGYB4-FgZTeZBU" #workbook ID
    
    print(f"\n Scraping vendors from Jumia Food...")
    url = 'https://food.jumia.com.ng/restaurants/city/abuja'
    vendors_df = scrape_vendors(url)


    print(f"\n Scraping menu from Jumia Food...")
    vendor = "https://food.jumia.com.ng/restaurant/n3bw/chicken-capitol"        
    menu_df = scrape_menu(vendor)


    if vendors_df.items()  and menu_df.items(): 

        # create sheet names and data
        sheet_names = {
                "Vendors" :vendors_df,
                "Menu" : menu_df
        }

        # loop through sheet_names to upload each dataframe
        for key in sheet_names.keys():
            
            #upload the dataframe to sheets
            print(f"\n Uploading {key} to sheet.... ")

            sheets = d2g.upload(df=sheet_names[key], gfile=gfile, wks_name=key, credentials=credentials, row_names=False, clean=True)

            if sheets:
                print(f"\n Data Upload is completed for {sheets.title}")

            else:
                print("Error Occured! Data not Uploaded")  

    else:
        print("Error Occured! Data Scraping Failed..")





        #https://github.com/priye-1/Jumia_Food_Scraper.git