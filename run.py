# -*- coding: utf-8 -*-
"""
Spyder Editor

@author: Carmen Cantudo Moreno SBS22086
"""

# Import the required libraries
from tkinter import *
from tkinter import ttk
from datetime import datetime
import csv
from pathlib import Path
import os

# News API
import requests
from newsapi import NewsApiClient

# Create an instance of tkinter frame or window
window=Tk()

# Set the size of the tkinter window
window.geometry("800x550")
window.resizable(width=FALSE, height=FALSE)

# Name the window
window.title("Today's News")

#Clock frame
clock_frame=Frame(window)
clock_frame.pack(fill="x")
clock_frame.config(width="150", height="80")

# Create clock function
def clock():
    time = datetime.now()
    hour = time.strftime("%H:%M:%S")
    weekday = time.strftime("%A")
    day = time.day
    month = time.strftime("%b")
    year = time.strftime("%Y")
    date_label.config(text=weekday + " " + str(day) + "/" + str(month) + "/" + (year) + "\n" + hour)
    date_label.after(200, clock)


# Display the date in a label widget
date_label = Label(clock_frame, text="", font=("Calibri", 20))
date_label.pack()

# Call the clock function
clock()


# News API Init
def getNewsApi(q):
    #Check if folder exists
    path = 'articles/'
    isExist = os.path.exists(path)
    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs(path)
    
    #Check if file exists
    path_to_file = f'articles/{q}.csv'
    path_article = Path(path_to_file)
    
    if path_article.is_file():
        f1 = open(f'articles/{q}.csv')
        for line in f1:
            i = 1
            my_articles.insert(i, line)
            i += 1
        f1.close()
        
    else:
        # api-endpoint
        URL = "https://newsapi.org/v2/everything"
    
        # defining a params dict for the parameters to be sent to the API 
        PARAMS = {"q": q,
            "apiKey":"467df1a9679d4ed3abe212dc47926126"}
        # sending get request and saving the response as response object 
        r = requests.get(url=URL, params=PARAMS)
        # extracting data in json format 
        news = r.json()
    
        # Loop to get 50 'news
        for i in range(50):
            articleDate = news["articles"][i]["publishedAt"]
            dateFormat = datetime.strptime(articleDate, '%Y-%m-%dT%H:%M:%SZ')
            articleDate = dateFormat.strftime('%d-%m-%Y')
            articleTitle = news["articles"][i]["title"]
            articleUrl = news["articles"][i]["url"]
            all_articles = [f"{articleDate}  -  {articleTitle} - {articleUrl}"]
            my_articles.insert(i+1, all_articles)
        
            # open the file in the write mode
            with open(f'articles/{q}.csv', 'a') as f:
                # create the csv writer
                writer = csv.writer(f)
                
                # write a row to the csv file
                writer.writerow(all_articles)
            
            #Open file and show saved articles
            f1 = open(f'articles/{q}.csv')
            for line in f1:
                i = 1
                my_articles.insert(i, line)
                i += 1
            f1.close() 
            
            
            
#Category Button Click Functions
def click_business():
    my_articles.delete(0,END)
    getNewsApi('business')
    
def click_sports():
    my_articles.delete(0,END)
    getNewsApi('sports')
    
def click_financial():
    my_articles.delete(0,END)
    getNewsApi('financial')
    

selected = []

#Select Record
def save_article():
    # Traverse the tuple returned by
    # curselection method and print
    # corresponding value(s) in the listbox
    for i in my_articles.curselection():
        #Check if folder exists
        path = 'articles/'
        # Check whether the specified path exists or not
        isExist = os.path.exists(path)
        if not isExist:
            # Create a new directory because it does not exist
            os.makedirs(path)
        with open('articles/readlater.csv', "a+") as file_object:
            # Move read cursor to the start of file.
            file_object.seek(0)
            # If file is not empty then append '\n'
            data = file_object.read(100)
            if len(data) > 0:
                file_object.write("\n")
            # Append text at the end of file
            file_object.write(my_articles.get(i))

# Open saved articles
def open_saved_articles():
    #Delete view
    my_articles.delete(0,END)
    
    path_to_file = 'articles/readlater.csv'
    path = Path(path_to_file)
    if path.is_file():
        #Open file and show saved articles
        f1 = open(path_to_file)
        for line in f1:
            i = 1
            my_articles.insert(i, line)
            i += 1
        f1.close() 
    else:
        my_articles.insert(1, 'No articles saved.')
    
#News buttons frame
buttons_frame=Frame(window)
buttons_frame.pack(side='left')
buttons_frame.config(width="180", height="470")
#Business news button

business_button = Button(buttons_frame, text="Business News", command=lambda: click_business(), padx=10, pady=10, width=13)
business_button.grid(row=1, column=1, padx=20, pady=10)

#Sport news button
sports_button = Button(buttons_frame, text="Sport News", command=lambda: click_sports(), padx=10, pady=10, width=13)
sports_button.grid(row=2, column=1, padx=20, pady=10)

#Financial news button
financial_button = Button(buttons_frame, text="Financial News", command=lambda: click_financial(), padx=10, pady=10, width=13)
financial_button.grid(row=3, column=1, padx=20, pady=10)

#Save article button
save_button = Button(buttons_frame, text="Save Articles", command=lambda: save_article(), padx=10, pady=10, width=13)
save_button.grid(row=4, column=1, padx=20, pady=10)

#Open save articles button
open_button = Button(buttons_frame, text="Open Articles", command=lambda: open_saved_articles(), padx=10, pady=10, width=13)
open_button.grid(row=5, column=1, padx=20, pady=10)

#News articles frame
articles_frame=Frame()
articles_frame.pack(side='right')
articles_frame.config(width="620", height="470")

#scrollbar
article_scroll_ver = Scrollbar(articles_frame,orient='vertical')
article_scroll_ver.pack(side=RIGHT, fill=Y)
article_scroll_hor = Scrollbar(articles_frame,orient='horizontal')
article_scroll_hor.pack(side= BOTTOM,fill=X)


my_articles = Listbox(articles_frame, yscrollcommand=article_scroll_ver.set, xscrollcommand=article_scroll_hor.set, selectmode=MULTIPLE)
my_articles.pack(side=RIGHT, padx=20, pady=20)
my_articles.config(width="620", height="470", font=("Calibri", 12))
my_articles.insert(1, "Click on Business, Sports or Financial News to get latest news.")
my_articles.insert(2, "Select the news you want to save to read later and click Save Article.")
my_articles.insert(3, "Click on Open Article to read the articles you saved.")

my_articles.pack()

article_scroll_ver.config(command=my_articles.yview)
article_scroll_hor.config(command=my_articles.xview)

window.mainloop()