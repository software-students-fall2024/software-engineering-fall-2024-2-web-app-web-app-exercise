import requests
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_bcrypt import Bcrypt
from pymongo import MongoClient
from dotenv import load_dotenv
from models import User
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
import os

bcrypt = Bcrypt()

def create_app():
    #initiate env
    app = Flask(__name__)

    # Load environment variables from .env file
    load_dotenv()
    
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')

    connection_string = os.getenv("MONGO_URI")  # Corrected to use "MONGO_URI" instead of MONGO_URI

    if connection_string is None:
        raise ValueError("MONGO_URI environment variable not found!")

    # Create a MongoDB client with the correct connection string
    client = MongoClient(connection_string)
    db = client["test_db"]
    
    # Define the MongoDB collection for articles
    articles_collection = db["articles"]

    # user auth stuff
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"
    
    article1 = {
    "title": "Finance Goldman Sachs beats on profit and revenue as stock trading and investment banking boost results",
    "author": "Hugh Son",
    "content": """Goldman Sachs topped estimates for third-quarter profit and revenue on strong results from its stock trading and investment banking operations. 
                Here’s what the company reported:
                Earnings: $8.40 per share vs. $6.89 LSEG estimate
                Revenue: $12.70 billion vs. $11.8 billion estimate
                The bank said profit surged 45% from a year earlier to $2.99 billion, or $8.40 per share, as revenue climbed 7% to $12.7 billion.

                Goldman shares were roughly flat after rising 2% earlier in the session.

                Over the past two years, the Federal Reserve’s tightening campaign has made for a less-than-ideal environment for investment banks like Goldman. Now that the Fed is easing its benchmark rate, Goldman is positioned to benefit as corporations that have waited on the sidelines to acquire competitors or raise funds begin to take action, and rising values bolster its asset and wealth management business.

                CEO David Solomon cited an “improving operating environment” as he touted his firm’s results on Tuesday.

                Equities trading was the outlier this quarter, posting an 18% revenue increase to $3.5 billion, more than half a billion dollars higher than the $2.96 billion estimate from StreetAccount. The company cited strong results in both derivatives and cash trading.

                Fixed income trading revenue slipped 12% from a year earlier to $2.96 billion, just above the $2.91 billion StreetAccount estimate, on a slowdown in interest rate products and commodities.

                Investment banking revenue jumped 20% to $1.87 billion, topping the $1.62 billion estimate, on strength in debt and equity underwriting, and the bank said its backlog for pending deals increased from both a year earlier and the second quarter.

                The firm’s asset and wealth management division also helped it top expectations; revenue there jumped 16% to $3.75 billion, exceeding the $3.58 billion estimate from StreetAccount on rising management fees and gains in investments.

                Last week, rival JPMorgan Chase set expectations high with better-than-anticipated results from trading and investment banking, factors that helped the bank top earnings estimates.

                Wells Fargo also exceeded estimates on Friday on the back of its investment banking division.
            """,
    "date": "%2024-%10-%15",
    "topImage": "https://image.cnbcfm.com/api/v1/image/108016846-1729004196183-108016846-1722955743918-gettyimages-2165053438-DAVID_SOLOMON_INTERVIEW.jpg?v=1729004209&w=1480&h=833&ffmt=webp&vtcrop=y"
}
    
    article2 = {
    "title": "United Airlines plans $1.5 billion share buyback, forecasts fourth-quarter earnings above estimates",
    "author": "Leslie Josephs",
    "content": """United Airlines
                  said Tuesday that it is starting a $1.5 billion share buyback as the carrier reported higher-than-expected earnings for the busy summer travel season and forecast strong results for the last three months of the year.

                  United expects to earn an adjusted $2.50 to $3.00 a share in the fourth quarter, compared to $2.00 a share a year earlier and the $2.68 analysts polled by LSEG estimated.

                  Here is what United reported for the third quarter compared with what Wall Street expected, based on average estimates compiled by LSEG:

                  Earnings per share: $3.33 adjusted vs. $3.17 expected
                  Revenue: $14.84 billion vs. $14.78 billion expected
                  The share buyback would be United’s first since before the Covid-19 pandemic. U.S. airlines received more than $50 billion in government aid during the pandemic travel slump that prohibited share repurchases and dividends, though airlines were still fighting for financial stability.

                  Southwest Airlines
                  announced a $2.5 billion share repurchase program last month.

                  “Like other leading airlines and companies, we are initiating a measured, strategic share repurchase program,” United CEO Scott Kirby said in a note to staff on Tuesday. “Importantly, my commitment to you is that investing in our people and our business will always be my top priority even while we institute this share repurchase program.”
            """,
    "date": "%2024-%10-%15",
    "topImage": "https://image.cnbcfm.com/api/v1/image/108026853-1724879553478-gettyimages-2167475948-san_diego_airplaines_ka_034.jpeg?v=1729024245&w=1480&h=833&ffmt=webp&vtcrop=y"
}

    article3 = {
    "title": "Don’t Chase China’s FOMO Rally",
    "author": "Jacky Wong",
    "content": """
            It’s rare to see a major country’s stock market go from the doghouse to the penthouse in a matter of weeks.

            Now that China has suddenly become the best-performing market in the world, investors need to recognize how much the gains are being driven by Beijing’s bolder steps to revive the nation’s sluggish economy and how much is just fear of missing out. They should proceed with caution.

            Despite a nearly 10% pullback in the past week or so, the MSCI China index has still gained around 20% in the past three weeks since Beijing signaled that it will roll out a slate of stimulus measures. That caught many investors by surprise after they had trimmed their positions in Chinese stocks in the past few years. The Chinese market has been beset by an implosion of the housing market and a regulatory crackdown on its leading technology companies.

            Global mutual funds were underweight China by around 3.1 percentage points at the end of August, according to Goldman Sachs. They have had to rapidly add to their positions to avoid underperforming the benchmark, fueling recent gains. Turnover hit record highs in both Hong Kong and mainland China’s stock markets. Even after the recent rally, MSCI China is still at around half of its 2021 peak.
            
            China is such a hot theme that U.S. individual investors paid more attention to it than a U.S. market also ripping to record highs. According to ETF.com, four of the 10 exchange-traded funds with the largest inflows last week were China funds, creating a rare period when foreign stock ETFs handily topped inflows into domestic stock ETFs. Domestic individual investors have hopped on board, too, with Chinese state television reporting that there was a record number of brokerage accounts opened during the recent seven-day national holiday.

            The price certainly seemed compelling: The Hang Seng China Enterprises index, a gauge of Chinese stocks listed in Hong Kong, was trading at just eight times forward earnings in early September. The ratio now stands at 9.7 times, still below the 10-year average of 11.3 times. By comparison, the U.S. benchmark S&P 500, which just touched a fresh record high, fetches nearly 24 times forward
            
            Beijing is addressing some of the key issues that plague China’s economy. The government said it has ample room to expand its fiscal deficit and plans to take the “boldest measure” to solve the debt issues at local governments. Those governments are starved of revenue from land sales because of the slumping housing market, which in turn has limited their ability to provide a boost to the economy. The central government will likely need to share some of the debt burden.

            If the fiscal stress at the local government level can be alleviated, they will have more room to tackle the problems of millions of unsold apartments. Beijing said in May that it would let local governments buy these homes to use as affordable housing, but that hasn’t happened on a large scale so far because of their own dire financial situation.

            The exact size of the stimulus remains hard for investors to pin down, though, which is why markets have fallen back lately. Investors might indeed be getting ahead of themselves. Such big changes to the budget will need the approval of the National People’s Congress, China’s legislature. Its standing committee will only meet later this month, which is when specific numbers will be announced.

            Even then, the package might still underwhelm investors. The process of easing the fiscal burden of local governments to stimulate demand could take a long time to work out. Meanwhile, providing big, direct stimulus to boost consumption seems unlikely as Beijing has long preferred supply-side measures. And housing inventories might take years to digest, even if the plan for local governments to buy some of those unsold apartments works out. And there is also the not-insignificant question of what can replace the housing market as the growth engine of the economy.

            There are indeed reasons to be more hopeful this time than the false dawns for Chinese stocks in the past few years, but the road to recovery will likely be gradual.
            """,
    "date": "%2024-%10-%15",
    "topImage": "https://images.wsj.net/im-11636049?width=700&size=1.520190023752969&pixel_ratio=2"
}
    
    article4 = {
    "title": "Wednesday’s big stock stories: What’s likely to move the market in the next trading session",
    "author": "Jason Gewirtz",
    "content": """
            Apple
            Despite concerns about the new iPhone, Apple
            hit a new all-time high on Tuesday.
            The stock ended the session up more than 1%, closing at $233.85. It hit a high of $237.49 before curtailing its gains for the day.
            Apple is up 5% in a month and 35% in six months.

            DJT
            Trading in Trump Media & Technology Group
            was wild on Tuesday.

            The stock finished down nearly 10%. It is down nearly 4% after hours.
            Check out the volume: 89 million shares. That is almost triple the ten-day average.
            The stock is up 68% in October. 

            Regional banks
            The big banks are just about done reporting. Now, the regionals move in.
            Citizens Financial
            , based in Providence, Rhode Island, reports before the bell. The stock has gained 12.5% in the past three months, and it’s up 5.5% in a week. The stock hit a new high on Tuesday.
            
            First Horizon
            , headquartered in Memphis, Tennessee, will also report before the bell. First Horizon is down 1% over the past three months. The stock is up 8% in a week and 4.3% from the July high.
            The SPDR S&P Regional Banking ETF (KRE)
            hit a new high on Tuesday. The ETF is up 6.7% in a week, and it has gained up 10.3% in three months.
            
            Wells Fargo
            , by the way, is up 10% in a week. In a rare interview on “Mad Money” Tuesday night, CEO Charles Scharf, who’s been leading a buyback charge, said, “We invest in much as we can inside the company and that’s our first priority.”
            
            Goldman Sachs
            is up 5.2% in week.

            Citigroup
            is down 4.7% in two days.
            
            JPMorgan Chase
            is up 5.5% in the past week.

            Bank of America
            is up 5.5% in a week, as well.

            Morgan Stanley
            is up 4.4% in a week. The bank reports on Wednesday morning before the bell, and CEO Ted Pick will be live on CNBC TV in the 10 a.m. hour, Eastern.
            """,
    "date": "%2024-%10-%15",
    "topImage": "https://image.cnbcfm.com/api/v1/image/108044733-1728397890304-gettyimages-2177438181-ms1_1579_gjdsvbyj.jpeg?v=1728398024&w=1480&h=833&ffmt=webp&vtcrop=y"
}
    
    # Insert the article into the MongoDB collection
    articles_collection.insert_one(article1)
    articles_collection.insert_one(article2)
    articles_collection.insert_one(article3)
    articles_collection.insert_one(article4)
    
    # user loader for flask login
    @login_manager.user_loader
    def load_user(user_id):
        user = db.users.find_one({"username": user_id}) # user is unique id'd by username (email)
        if user:
            return User(
                username=user["username"],
                password=user.get("password"),
                firstname=user.get("firstname"),
                lastname=user.get("lastname"),
            )
        return None
    
    @app.route("/")
    def home():
        return render_template("home.html")
    
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            # Login Logic
            username = request.form["username"]
            password = request.form["password"]
            user = User.validate_login(db, username, password)
            if user:
                login_user(user)
                return redirect(url_for("getNews"))
            else:
                flash("Invalid username or password. Try again.")
                return render_template('home.html', error="Error occurred!")
        return render_template("home.html")

    @app.route("/signup", methods=["GET", "POST"])
    def signup():
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            password2 = request.form["password2"]
            firstname = request.form["firstname"]
            lastname = request.form["lastname"]
            # check if passwords match
            if password != password2:
                flash("Passwords don't match!")
                return render_template("signup.html")
            
            if User.find_by_username(db, username):
                flash("Username with that email already exists!")
                return render_template('signup.html', error="Error occurred!")
            User.create_user(db, username, password, firstname, lastname)
            flash("User created successfully!")
            return redirect(url_for("login"))
        return render_template("signup.html")
    
    
    @app.route("/user-info")
    @login_required # this decorator makes it so you can only be logged in to view this page.... put this on any new routes you make pls
    def getUserInfo():
        #retrieve user info and return with template
        user_info = {
            "username": current_user.username,
            "password": current_user.password,
            "firstname": current_user.firstname,
            "lastname": current_user.lastname
        }
        
        return render_template("setting.html", user_info=user_info)
    
    @app.route("/update-info")
    @login_required
    def getUpdatePage():
        user_info = {
            "username": current_user.username,
            "password": current_user.password,
            "firstname": current_user.firstname,
            "lastname": current_user.lastname
        }
        
        return render_template("edit-user-info.html", user_info=user_info)
    
    @app.route("/user-info",methods=["POST"])
    @login_required
    def updateUserInfo():
        # getting firstname and last name from the HTML form
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        
        # update the user's first name and last name in the mongodb
        db.users.update_one(
            {"username": current_user.username},
            {"$set": {"firstname": firstname, "lastname": lastname}}
        )
        
        # update the current_user object on flask app
        current_user.firstname = firstname
        current_user.lastname = lastname
        
        # flash a success message and redirect back to the user info page
        flash("User info updated successfully!")
        return redirect(url_for("getUserInfo"))

    @app.route("/log-out")
    @login_required 
    def logout():
        logout_user() 
        return redirect(url_for('home'))
    
    @app.route("/delete-acct")
    @login_required 
    def delete_acct():
        return render_template("delete-acct.html")
        
    @app.route('/delete-acct', methods=['POST'])
    @login_required
    def delete_account():
        # getting the form data
        username = request.form.get('username')
        password = request.form.get('password')
        # if username entered from form == logged in user's username
        if username == current_user.username:
            user = db.users.find_one({"username": username})

            # check if the user exists and the password matches
            if user and bcrypt.check_password_hash(user['password'], password):
                db.users.delete_one({"username": username})
                
                # log user out and redirect to home w/ success message
                logout_user()
                flash('Account has been successfully deleted.')
                return redirect(url_for('home'))
            else:
                flash('Invalid username or password. Please try again.')
        else:
            flash('The provided email does not match the current user.')

        return render_template('delete-acct.html')
    
    
    @app.route("/contact_us")
    @login_required
    def contact_us():
        #get contact-us page
        return render_template("Contact_us.html")
    
    @app.route("/contact_us",methods=["POST"])
    def sendMessage():
        #get the message title and content from form and email it to a specific address
        title = request.form["title"]
        content = request.form["content"]
        ###TODO###
        
        
        flash("Message Sent!")
        return redirect(url_for("contact_us"))
    
    
    @app.route("/vocab")
    @login_required
    def getVocab():
        #retrieve vocab list of the user and return with template
        ###TODO###
        
        return render_template("vocab.html")
    
    @app.route("/vocab",methods=["POST"])
    def sendVocab():
        #add vocab(word, definition) to the user vocab list
        word = request.form["word"]
        definition = request.form["definition"]
        ###TODO###
        
        
        flash("Word added to the list!")
        return jsonify({"message": "word added!"}), 200
    
    @app.route("/vocab",methods=["DELETE"])
    def deleteVocab():
        #delete word
        ###TODO###
        
        
        flash("Word successfully deleted!")
        return redirect(url_for("getVocab"))
    
    @app.route("/news")
    def getNews():
        
        return render_template("news.html")
    
    @app.route("/news-content")
    def getNewsContent():

        return render_template("news-content.html")
    
    @app.route("/menu")
    def getMenu():
        
        return render_template("Menu.html")
    
    

    return app



    
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)