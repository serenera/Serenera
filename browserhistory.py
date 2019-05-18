import csv
import os
import sqlite3
import sys
from datetime import datetime
import copy
import shutil


# platform_table maps the name of user's OS to a platform code
platform_table = {
        'linux': 0,
        'linux2': 0,
        'darwin': 1,
        'cygwin': 2,
        'win32': 2,
        }

# it supports Linux, MacOS, and Windows platforms.
try:
    user_platformcode = platform_table[sys.platform]
except KeyError:
    class NotAvailableOS(Exception):
        pass
    raise NotAvailableOS("It does not support your OS.")


def get_username() -> str:
    """
    Get username based on their local computers
    """
    platform_code = user_platformcode
    cwd_path = os.getcwd()
    cwd_path_list = []
    # if it is a macOS
    if platform_code == 1:
        cwd_path_list = cwd_path.split('/')
    # if it is a windows
    elif platform_code == 2:
        cwd_path_list = cwd_path.split('\\')
    # if it is a linux
    else:
        cwd_path_list = cwd_path.split('/')
    return cwd_path_list[2]


def get_database_paths() -> dict:
    """
    Get paths to the database of browsers and store them in a dictionary.
    It returns a dictionary: its key is the name of browser in str and its value is the path to database in str.
    """
    platform_code = user_platformcode
    browser_path_dict = dict()
    # if it is a macOS
    if platform_code == 1:
        cwd_path = os.getcwd()
        cwd_path_list = cwd_path.split('/')
        # it creates string paths to browser databases

        abs_chrome_path = os.path.join('/', cwd_path_list[1], cwd_path_list[2], 'Library', 'Application Support', 'Google/Chrome/Default', 'History')

        # check whether the databases exist
        if os.path.exists(abs_chrome_path):
            dire = os.path.dirname(__file__)
            shutil.copy(abs_chrome_path,dire)
            browser_path_dict['chrome'] = dire
            
      
    # if it is a windows
    if platform_code == 2:
        homepath = os.path.expanduser("~")
        abs_chrome_path = os.path.join(homepath, 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'History')
        abs_firefox_path = os.path.join(homepath, 'AppData', 'Roaming', 'Mozilla', 'Firefox', 'Profiles')
        # it creates string paths to broswer databases
        if os.path.exists(abs_chrome_path):
            browser_path_dict['chrome'] = abs_chrome_path
      
    # if it is a linux 
    if platform_code == 0:
        cwd_path = os.getcwd()
        #print(cwd_path)
        cwd_path_list = cwd_path.split('/')
        # it creates string paths to broswer databases
        
        abs_chrome_path = os.path.join('/', cwd_path_list[1], cwd_path_list[2],'.config','google-chrome','Default','History')
        # check whether the path exists
        if os.path.exists(abs_chrome_path):
            #print(abs_chrome_path)
            dirname = os.path.dirname(__file__)
            #print(dirname)
            filename = os.path.join(dirname, 'history_sql_chrome')
            #print(filename)
            shutil.copy(abs_chrome_path, filename)
            browser_path_dict['chrome'] = filename
      

    return browser_path_dict


def get_browserhistory() -> dict:
    
    # browserhistory is a dictionary that stores the query results based on the name of browsers.
    browserhistory = {}

    # call get_database_paths() to get database paths.
    paths2databases = get_database_paths()

    for browser, path in paths2databases.items():
        try:
            conn = sqlite3.connect(path)
            cursor = conn.cursor()
            _SQL = ''
            # SQL command for browsers' database table
            if browser == 'chrome':
                _SQL = """SELECT url, title, datetime((last_visit_time/1000000)-11644473600, 'unixepoch', 'localtime') 
                                    AS last_visit_time FROM urls ORDER BY last_visit_time DESC"""
           
            else:
                pass
            # query_result will store the result of query
            query_result = []
            try:
                cursor.execute(_SQL)
                query_result = cursor.fetchall()
            except sqlite3.OperationalError:
                print('* Notification * ')
                print('Please Completely Close ' + browser.upper() + ' Window')
            except Exception as err:
                print(err)
            # close cursor and connector
            cursor.close()
            conn.close()
            # put the query result based on the name of browsers.
            browserhistory[browser] = query_result
        except sqlite3.OperationalError:
            print('* ' + browser.upper() + ' Database Permission Denied.')

    return browserhistory


def write_browserhistory_csv() -> None:
    """It writes csv files that contain the browser history in
    the current working directory. It will writes csv files base on
    the name of browsers the program detects."""
    browserhistory = get_browserhistory()
    
    for browser, history in browserhistory.items():
        with open(browser + '_history.csv', mode='w', encoding='utf-8', newline='') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=',',
                            quoting=csv.QUOTE_ALL)
            i=0
            for data in history:
                if i==1000: break
                csv_writer.writerow(data)
                i+=1
                
                
                
