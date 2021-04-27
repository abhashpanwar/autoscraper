from flask import Flask, render_template, request
  
app = Flask(__name__)


@app.route("/",methods=['GET'])  
def home():    

    if request.args.get('search'):
        search = request.args.get('search')
        search_data = searchquery(search)
        data_length = len(search_data)
        return render_template("index.html",data = {'query':search,'searchData':search_data,'totalRecords':data_length}) 
    data_length = -1
    return render_template("index.html",data = {'query':"",'searchData':"d",'totalRecords':data_length}) 
def searchquery(search):
    from autoscraper import AutoScraper

    amazon_url="https://www.amazon.in/s?k={}&s=price-desc-rank".format(search)

    amazon_scraper = AutoScraper()
    amazon_scraper.load('amazon_in')
    
    data = amazon_scraper.get_result_similar(amazon_url, group_by_alias=True)
    search_data = tuple(zip(data['Title'],data['ImageUrl'],data['Price'],data['Rating']))
    
    return search_data
if __name__ == "__main__":
    app.run(debug=True)