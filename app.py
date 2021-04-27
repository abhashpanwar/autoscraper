from flask import Flask, render_template, request
from autoscraper import AutoScraper
import pandas as pd
import time
app = Flask(__name__)

#creating object and loading
amazon_scraper = AutoScraper()
amazon_scraper.load('amazon_in.json')    
    
@app.route("/",methods=['GET'])  
def home():    

    #when user search it
    if request.args.get('search'):
        #inputs
        search = request.args.get('search')
        sortby = request.args.get('sortby','relevanceblender')
        
        #call function to retrieve data
        search_data,original_url = searchquery(search,sortby)
        data_length = len(search_data)
        
        #show to user
        return render_template("index.html",data = {'original_url':original_url,'query':search,'sortby':sortby,'searchData':search_data,'totalRecords':data_length}) 
    
    #default data_length when no search
    data_length = -1
    return render_template("index.html",data = {'query':"",'searchData':"d",'totalRecords':data_length}) 
def searchquery(search,sortby):
    #load library    

    #define url
    amazon_url="https://www.amazon.in/s?k={}&s={}".format(search,sortby)    
    
    #get data
    data = amazon_scraper.get_result_similar(amazon_url, group_by_alias=True)

    #combine data into tuple to show it to user
    search_data = tuple(zip(data['Title'],data['ImageUrl'],data['Price'],data['Reviews']))

    #creating dataframe so that user can download it in csv format
    df = pd.DataFrame(columns=['Query','Title','Price','Reviews','ImageUrl'])
    for i in range(len(search_data)):
        df.loc[len(df)] = [search,search_data[i][0],search_data[i][2],search_data[i][3],search_data[i][1]]
    df.to_csv("static/searchedData.csv",index=False)
    
    #returing data
    return search_data,amazon_url
if __name__ == "__main__":
    app.run(debug=True)
