from flask import Flask, redirect, url_for, render_template, request, session
#import os
import sqlite3 #for datatabase
import random   #for generating random values for creating VendorId,BookingId,UserId
import datetime #for generating current date and time for creating VendorId,BookingId,UserId
from hash import pw_hash    #for encoding password

#current_path = os.path.dirname(os.path.abspath(__file__))

creative_app = Flask(__name__)
creative_app.secret_key = "xxxxxxxxxx"

#Home Page
@creative_app.route("/")
def home():
    return render_template("index.html")

#Log In Page for User
@creative_app.route("/login/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form.get("Email")
        password = request.form.get("Password")

        conn = sqlite3.connect('creative.db')
        curso = conn.cursor()
        curso.execute("""SELECT Email FROM User WHERE Email = :em AND Password = :pw""", {"em":email, "pw":pw_hash(password)})
        row = curso.fetchall()
        if len(row) == 1:
            session["email"] = email
            curso.execute("""UPDATE User SET LoginStatus = :ls WHERE Email = :em """, {"ls":1,"em":email})
            conn.commit()
            conn.close()
            return redirect(url_for("services"))
        else:
            return render_template("failed_login.html", email=email)
    return render_template("login.html")

#Log Out Page for User
@creative_app.route("/logout/", methods=["POST", "GET"])
def logout():
    if "email" in session:
        email= session["email"]
        conn = sqlite3.connect('creative.db')
        curs = conn.cursor()
        curs.execute("""UPDATE User SET LoginStatus = 0 WHERE Email = :em """, {"em":email})
        conn.commit()
        conn.close()
        session.pop("email", None)
        return redirect(url_for("home"))
    return redirect(url_for("home"))

#Signup Page for User
@creative_app.route("/usersignup/", methods=["POST", "GET"])
def usersignup():
    if request.method == "POST":
        first_name = request.form.get("FirstName")
        last_name = request.form.get("LastName")
        email = request.form.get("Email")
        mobile = request.form.get("Mobile_Number")
        password = request.form.get("Password")
        password2 = request.form.get("Password2")

        conn = sqlite3.connect('creative.db')
        curso = conn.cursor()
        curso.execute("""SELECT Email FROM User WHERE Email = :em""", {"em":email})
        row = curso.fetchall()
        if len(row) == 1:
            return render_template("failed_reg.html", name=first_name, email=email)
        else:
            session["name"] = first_name

            t = str(datetime.datetime.now())
            ti = t.replace(" ","")
            ti = ti.replace("-","")
            ti = ti.split(".")
            userid = ""
            userid += random.choice(first_name)
            userid += random.choice(last_name)
            userid += ti[0]

            curso = conn.cursor()
            curso.execute("""INSERT INTO User VALUES(:em,:ui,:fn,:ln,:mo,:pw,:ls)""",{"em":email,"ui":userid,"fn":first_name,"ln":last_name,"mo":mobile,"pw":pw_hash(password),"ls":0})
            conn.commit()
            conn.close()
            return render_template("success_reg.html", name=first_name)  
    else:
        return render_template("usersignup.html")

#Services Page for User
@creative_app.route("/services/", methods=["POST", "GET"])
def services():
    if "email" in session:
        email = session["email"]
        conn = sqlite3.connect('creative.db')
        curso = conn.cursor()
        curso.execute("""SELECT FirstName,LoginStatus FROM User WHERE Email = :em""", {"em":email})
        row = curso.fetchall()
        fname, status = row[0]
        if status == 1:
            return render_template("services.html", name=fname)
        else:
            return redirect(url_for("login"))
    else:
        return redirect(url_for("login"))

#Log In Page for Creative
@creative_app.route("/crlogin/", methods=["POST", "GET"])
def crlogin():
    if request.method == "POST":
        email = request.form.get("Email")
        password = request.form.get("Password")

        conn = sqlite3.connect('creative.db')
        curso = conn.cursor()
        curso.execute("""SELECT Email FROM Vendors WHERE Email = :em AND Password = :pw""", {"em":email, "pw":pw_hash(password)})
        row = curso.fetchall()
        if len(row) == 1:
            session["cremail"] = email
            curso.execute("""UPDATE Vendors SET LoginStatus = :ls WHERE Email = :em """, {"ls":1,"em":email})
            conn.commit()
            conn.close()
            return redirect(url_for("ManageBooking"))
        else:
            return render_template("failed_crlogin.html", email=email)
    return render_template("crlogin.html")

#Log Out Page for Creative
@creative_app.route("/crlogout/", methods=["POST", "GET"])
def crlogout():
    if "cremail" in session:
        bemail = session["cremail"]
        conn = sqlite3.connect('creative.db')
        curs = conn.cursor()
        curs.execute("""UPDATE Vendors SET LoginStatus = 0 WHERE Email = :em """, {"em":bemail})
        conn.commit()
        conn.close()
        session.pop("cremail", None)
        return redirect(url_for("home"))
    return redirect(url_for("home"))

#Sign Up Page for Creative
@creative_app.route("/crsignup/", methods=["POST", "GET"])
def crsignup():
    if request.method == "POST":
        BName = request.form.get("BName")
        BEmail = request.form.get("BEmail")
        Mobile = request.form.get("Mobile_Number")
        BAddress = request.form.get("Address")
        City = request.form.get("City")
        ZipCode = request.form.get("ZipCode")
        Country = request.form.get("Country")
        BWebsite = request.form.get("BWebsite")
        BPicture = request.form.get("ProfilePic")
        BDesc = request.form.get("BDescript")
        ServiceType = request.form.get("service")
        HourlyRate = request.form.get("HourlyRate")
        password= request.form.get("Password")
        password2= request.form.get("Password2")


        conn = sqlite3.connect('creative.db')
        curso = conn.cursor()
        curso.execute("""SELECT Email FROM User WHERE Email = :em""", {"em":BEmail})
        row = curso.fetchall()
        if len(row) == 1:
            return render_template("failed_reg.html", name=BName, email=BEmail)
        else:
            session["crname"] = BName
            t = str(datetime.datetime.now())
            ti = t.replace(" ","")
            ti = ti.replace("-","")
            ti = ti.split(".")
            vendorid = ""
            bname = str(BName).replace(" ","")
            vendorid += random.choice(bname)
            vendorid += random.choice(bname)
            vendorid += ti[0]

            curso = conn.cursor()
            curso.execute("""SELECT CreativeId,Name FROM Creatives WHERE NAME =:st""",{"st":ServiceType})
            id = curso.fetchall()
            idc,nam = id[0]

            curso = conn.cursor()
            curso.execute("""SELECT ZipCode FROM Zip_Code WHERE ZipCode =:zc 
            AND City =:ct""",{"zc":ZipCode,"ct":City})
            zip = curso.fetchall()
            if len(zip) != 1:
                curso = conn.cursor()
                curso.execute("""SELECT Email FROM Vendors WHERE Email = :em""", {"em":BEmail})
                rowc = curso.fetchall()
                if len(rowc) == 1:
                    return render_template("failed_reg.html", name=BName, email=BEmail)
                curso = conn.cursor()
                curso.execute("""INSERT INTO Zip_Code VALUES(:zc,:ct,:cy)""",
                {"zc":ZipCode,"ct":City,"cy":Country})
                curso.execute("""INSERT INTO Vendors VALUES(:em,:vi,:bn,:ba,:mo,:bd,:bw,
                :hr,:pw,:zc,:ls,:pp)""",{"em":BEmail,"vi":vendorid,"bn":BName,"ba":BAddress,
                "mo":Mobile,"bd":BDesc,"bw":BWebsite,"hr":HourlyRate,"pw":pw_hash(password),
                "zc":ZipCode,"ls":0,"pp":BPicture})
                curso.execute("""INSERT INTO Vendor_Creatives (Vendor_id,Creative_id) 
                VALUES(:vi,:ci)""", {"vi":vendorid,"ci":idc})
                conn.commit()
                conn.close()
                return render_template("success_reg.html", name=BName)
            else:
                curso = conn.cursor()
                curso.execute("""SELECT Email FROM Vendors WHERE Email = :em""", {"em":BEmail})
                rowc = curso.fetchall()
                if len(rowc) == 1:
                    return render_template("failed_reg.html", name=idc, email=BEmail)
                curso = conn.cursor()
                curso.execute("""INSERT INTO Vendors VALUES(:em,:vi,:bn,:ba,:mo,:bd,:bw,
                :hr,:pw,:zc,:ls,:pp)""",{"em":BEmail,"vi":vendorid,"bn":BName,"ba":BAddress,
                "mo":Mobile,"bd":BDesc,"bw":BWebsite,"hr":HourlyRate,"pw":pw_hash(password),
                "zc":ZipCode,"ls":0,"pp":BPicture})
                curso.execute("""INSERT INTO Vendor_Creatives (Vendor_id,Creative_id) VALUES(:vi,:ci)""",{"vi":vendorid,"ci":idc})
                conn.commit()
                conn.close()
                return render_template("success_reg.html", name=BName)  
    else:
        return render_template("creativesignup.html")

#Services SubPage (EventPlanners Page)
@creative_app.route("/eventP/", methods=["POST","GET"])
def eventP():
    if "email" in session:
        email = session["email"]
        conn = sqlite3.connect('creative.db')
        curso = conn.cursor()
        curso.execute("""SELECT FirstName,LoginStatus FROM User WHERE Email = :em""", {"em":email})
        row = curso.fetchall()
        fname, status = row[0]
        if status == 1:
            curso = conn.cursor()
            curso.execute("""SELECT * FROM vendors_info 
            WHERE VendorId IN 
            (SELECT Vendor_id FROM Vendor_Creatives WHERE Creative_id = 
            (SELECT CreativeId FROM Creatives WHERE Name = "EventPlanning"))""")
            event_p = curso.fetchall()
            creative_ev = {}
            for planner in event_p:
                em, *other = planner
                creative_ev[em] = other

            return render_template("event.html", name=fname, event_pl=creative_ev )
        else:
            return redirect(url_for("login"))
    return redirect(url_for("login"))

#Services SubPage (Photographer's Page)
@creative_app.route("/photoG/")
def photoG():
    if "email" in session:
        email = session["email"]
        conn = sqlite3.connect('creative.db')
        curso = conn.cursor()
        curso.execute("""SELECT FirstName,LoginStatus FROM User WHERE Email = :em""", {"em":email})
        row = curso.fetchall()
        fname, status = row[0]
        if status == 1:
            curso = conn.cursor()
            curso.execute("""SELECT * FROM vendors_info 
            WHERE VendorId IN 
            (SELECT Vendor_id FROM Vendor_Creatives WHERE Creative_id = 
            (SELECT CreativeId FROM Creatives WHERE Name = "Photography"))""")
            event_p = curso.fetchall()
            creative_ph = {}
            for planner in event_p:
                em, *other = planner
                creative_ph[em] = other

            return render_template("photo.html", name=fname, event_pl=creative_ph )
        else:
            return redirect(url_for("login"))
    return redirect(url_for("login"))

#VendorId Session Page
@creative_app.route("/eventPvid/", methods=["POST","GET"])
def eventPvid():
    if "email" in session:
        venid = request.form.get("venid")
        session["vid"] = venid
        return redirect(url_for("booking"))
    else:
        return redirect(url_for("login"))

#Booking Page
@creative_app.route("/booking/", methods=["POST","GET"])
def booking():
    if "email" in session:
        venid = session["vid"]
        email = session["email"]
        conn = sqlite3.connect('creative.db')
        curso = conn.cursor()
        curso.execute("""SELECT FirstName,LoginStatus FROM User WHERE Email = :em""", {"em":email})
        row = curso.fetchall()
        fname, status = row[0]
  
        if status == 1:
            if request.method == "POST":
                #Extracting Values from Booking Form
                EDate = request.form.get("EventDate")
                ETime = request.form.get("EventTime")
                EDesc = request.form.get("EDescript")
                EDuration = request.form.get("Duration")
                EAddress = request.form.get("Address")
                ZipCode = request.form.get("Zip")
                City = request.form.get("City")
                Country = request.form.get("Country")

                #Creation of BookingId
                t = str(datetime.datetime.now())
                ti = t.replace(" ","")
                ti = ti.replace("-","")
                ti = ti.split(".")
                bookingid = ""
                edesc = str(EDesc).replace(" ","")
                bookingid += random.choice(edesc)
                bookingid += random.choice(edesc)
                bookingid += ti[0]

                curso = conn.cursor()
                curso.execute("""SELECT UserId,FirstName FROM User WHERE Email =:em""",{"em":email})
                id = curso.fetchall()
                userid,nam = id[0]

                curso = conn.cursor()
                curso.execute("""SELECT ZipCode FROM Zip_Code WHERE ZipCode =:zc 
                AND City =:ct""",{"zc":ZipCode,"ct":City})
                zip = curso.fetchall()
                if len(zip) != 1:  
                    curso = conn.cursor()
                    curso.execute("""INSERT INTO Zip_Code VALUES(:zc,:ct,:cy)""",
                    {"zc":ZipCode,"ct":City,"cy":Country})
                    curso.execute("""INSERT INTO Booking VALUES(:bi,:ad,:ed,:ea,:edu,:st,:ui,
                    :zc,:vi,:et)""",{"bi":bookingid,"ad":EDate,"ed":EDesc, "ea":EAddress,
                    "edu":EDuration,"st":"Booked","ui":userid,"zc":ZipCode,"vi":venid,"et":ETime})
                    conn.commit()
                    conn.close()
                    return render_template("success_book.html", bi=bookingid, name=nam)
                else:  
                    curso = conn.cursor()
                    curso.execute("""INSERT INTO Booking VALUES(:bi,:ad,:ed,:ea,:edu,:st,:ui,
                    :zc,:vi,:et)""",{"bi":bookingid,"ad":EDate,"ed":EDesc, "ea":EAddress,
                    "edu":EDuration,"st":"Booked","ui":userid,"zc":ZipCode,"vi":venid,"et":ETime})
                    conn.commit()
                    conn.close()
                    return render_template("success_book.html", name=nam, bi=bookingid)  
            else:
                return render_template("userbooking.html")
        else:
            return redirect(url_for("login"))
    else:
        return redirect(url_for("login"))

#Booking History Page
@creative_app.route("/ManageBooking/", methods=["POST","GET"])
def ManageBooking():
    if "cremail" in session:
        bemail = session["cremail"]
        conn = sqlite3.connect('creative.db')
        curso = conn.cursor()
        curso.execute("""SELECT VendorId,LoginStatus FROM Vendors WHERE Email = :bem""", {"bem":bemail})
        row = curso.fetchall()
        vid, status = row[0]
        if status == 1:
            curso = conn.cursor()
            curso.execute("""SELECT b.*,z.City,z.Country,u.FirstName,u.Email,u.MobileNumber 
            FROM Booking b INNER JOIN Zip_Code z ON b.ZipCode=z.ZipCode
            INNER JOIN User u ON b.userId=u.userId  
            WHERE VendorId = :vi""", {"vi":vid})
            bookings = curso.fetchall()
            booking = {}
            for book in bookings:
                em, *other = book
                booking[em] = other

            return render_template("mbooking.html", booking=booking )
        else:
            return redirect(url_for("crlogin"))
    return redirect(url_for("crlogin"))
    

if __name__ == "__main__":
    creative_app.run()