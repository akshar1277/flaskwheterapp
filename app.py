import requests
from  flask import Flask,render_template,request,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
import json


app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/weather'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SECRET_KEY']='AKSHAR'



db=SQLAlchemy(app)

class City(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50),nullable=False)


def get_weather_data(city):
    url=f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid=776c97053d9d9922ada774c50d9c8519"
    r=requests.get(url).json()
    return r    

@app.route('/')
def index_get():

   
    cities=City.query.all()


    # url="http://api.openweathermap.org/data/2.5/weather?q={}&appid=776c97053d9d9922ada774c50d9c8519"
    
    weather_data=[]

    for city in cities:
    
    
        # r=requests.get(url.format(city.name)).json()
        r=get_weather_data(city.name)
        # print(r)
        
        #-->have je data malyo chhe ane fetch karva dictonary banavia

        weather = {

            'city' :city.name,
            'temperature':r['main']['temp'],
            'description':r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],    
                    }
        # print(weather)
        weather_data.append(weather) 
        
        
    return render_template('weather.html',weather_data=weather_data)

@app.route('/',methods=['POST'])
def index_post():
    err_msg=''
    
    new_city=request.form.get('city')
    if new_city:
        existing_city=City.query.filter_by(name=new_city).first()
       
        if not existing_city:
            new_city_data=get_weather_data(new_city)
            if new_city_data['cod']==200:
                new_city_obj=City(name=new_city)


                db.session.add(new_city_obj)
                db.session.commit()
            else:
                err_msg="city does not exits!!!"
                
        else:
            err_msg="city already exists"
            
    if err_msg:
        flash(err_msg,'error')
    else:
        flash('city added succesfully')
    return redirect(url_for('index_get'))
    

@app.route('/delete/<name>')
def delete_city(name):
    city=City.query.filter_by(name=name).first()
    db.session.delete(city)
    db.session.commit()

    flash(f'succesfully deleted {city.name}','success')
    return redirect(url_for('index_get'))




if __name__ == "__main__":
    app.run(debug=True)