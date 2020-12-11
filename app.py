import mariadb
from flask import Flask, request, Response
import json
import dbcreds
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

@app.route('/artwork', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def artwork():
    if request.method == 'GET':
        conn = None
        cursor = None
        artworks = None
        content = request.args.get("content")
        art_id = request.args.get("id")
        print(art_id)
        try:
            conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, port=dbcreds.port, database=dbcreds.database, host=dbcreds.host)
            cursor = conn.cursor()
            if art_id != None and art_id != "":
                cursor.execute("SELECT * FROM artwork WHERE id=?", [art_id,])
                rows = cursor.fetchall()
                artworks = []
                headers = [i[0] for i in cursor.description]
                for row in rows:
                    artwork = dict(zip(headers, row))
                    # cursor.execute("SELECT COUNT(*) FROM tweet_like WHERE tweet_id=?", [tweet['id']])
                    # like_amount = cursor.fetchone()[0]
                    # print(like_amount)
                    # tweet["like_amount"] = like_amount
                    artworks.append(artwork)
                print(artworks)
            elif content != None and content != "":
                cursor.execute("SELECT * FROM artwork WHERE name LIKE ? ORDER BY completed_at DESC", ["%{}%".format(content),])
                rows = cursor.fetchall()
                artworks = []
                headers = [i[0] for i in cursor.description]
                for row in rows:
                    artwork = dict(zip(headers, row))
                    # cursor.execute("SELECT COUNT(*) FROM tweet_like WHERE tweet_id=?", [tweet['id']])
                    # like_amount = cursor.fetchone()[0]
                    # print(like_amount)
                    # tweet["like_amount"] = like_amount
                    artworks.append(artwork)
                print(artworks)
            elif id == None or id == "" or content == None or content == "":
                cursor.execute("SELECT * FROM artwork ORDER BY completed_at DESC")
                rows = cursor.fetchall()
                artworks = []
                headers = [i[0] for i in cursor.description]
                for row in rows:
                    artwork = dict(zip(headers, row))
                    # cursor.execute("SELECT COUNT(*) FROM tweet_like WHERE tweet_id=?", [tweet['id']])
                    # like_amount = cursor.fetchone()[0]
                    # print(like_amount)
                    # tweet["like_amount"] = like_amount
                    artworks.append(artwork)
                print(artworks)
        except mariadb.dataError:
            print("There seems to be something wrong with your data.")
        except mariadb.databaseError:
            print("There seems to be something wrong with your database.")
        except mariadb.ProgrammingError:
            print("There seems to be something wrong with SQL written.")
        except mariadb.OperationalError:
            print("There seems to be something wrong with the connection.")
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
            if(artworks != None):
                return Response(json.dumps(artworks, default=str), mimetype="application/json", status=200)
            else:
                return Response("Something went wrong!", mimetype="text/html", status=500)
    
    elif request.method == 'POST':
        conn = None
        cursor = None
        name = request.json.get("name")
        length = request.json.get("length")
        width = request.json.get("width")
        completed_at = request.json.get("completed_at")
        category = request.json.get("category")
        status = request.json.get("status")
        url = request.json.get("url")
        rows = None
        artwork = None
        try:
            conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, port=dbcreds.port, database=dbcreds.database, host=dbcreds.host)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO artwork(name, length, width, completed_at, category, status, url) VALUES(?, ?, ?, ?, ?, ?, ?)", [name, length, width, completed_at, category, status, url])
            conn.commit()
            rows = cursor.rowcount
            if rows == 1:
                art_id = cursor.lastrowid
                print(art_id)
                cursor.execute("SELECT * FROM artwork WHERE id=?", [art_id])
                row = cursor.fetchone()
                print(row)
                artwork = {}
                headers = [i[0] for i in cursor.description]
                artwork = dict(zip(headers, row))
        except mariadb.dataError:
            print("There seems to be something wrong with your data.")
        except mariadb.databaseError:
            print("There seems to be something wrong with your database.")
        except mariadb.ProgrammingError:
            print("There seems to be something wrong with SQL written.")
        except mariadb.OperationalError:
            print("There seems to be something wrong with the connection.")
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
            if(artwork != None):
                return Response(json.dumps(artwork, default=str), mimetype="application/json", status=201)
            else:
                return Response("Something went wrong!", mimetype="text/html", status=500)
    
    elif request.method == 'PATCH':
        conn = None
        cursor = None
        name = request.json.get("name")
        length = request.json.get("length")
        width = request.json.get("width")
        completed_at = request.json.get("completed_at")
        category = request.json.get("category")
        status = request.json.get("status")
        url = request.json.get("url")
        art_id = request.json.get("id")
        rows = None
        artwork = None
        try:
            conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, port=dbcreds.port, database=dbcreds.database, host=dbcreds.host)
            cursor = conn.cursor() 
            if name != "" and name != None:
                cursor.execute("UPDATE artwork SET name=? WHERE id=?", [name, art_id])
            if length != "" and length != None:
                cursor.execute("UPDATE artwork SET length=? WHERE id=?", [length, art_id])
            if width != "" and width != None:
                cursor.execute("UPDATE artwork SET width=? WHERE id=?", [width, art_id])
            if completed_at != "" and completed_at != None:
                cursor.execute("UPDATE artwork SET completed_at=? WHERE id=?", [completed_at, art_id])
            if category != "" and category != None:
                cursor.execute("UPDATE artwork SET category=? WHERE id=?", [category, art_id])
            if status != "" and status != None:
                cursor.execute("UPDATE artwork SET status=? WHERE id=?", [status, art_id])
            if url != "" and url != None:
                cursor.execute("UPDATE artwork SET url=? WHERE id=?", [url, art_id])
            conn.commit()
            rows = cursor.rowcount
            print(rows)
            cursor.execute("SELECT * FROM artwork WHERE id=?", [art_id,])
            row = cursor.fetchone()
            print(row)
            artwork = {}
            headers = [i[0] for i in cursor.description]
            artwork = dict(zip(headers, row))
        except mariadb.dataError:
            print("There seems to be something wrong with your data.")
        except mariadb.databaseError:
            print("There seems to be something wrong with your database.")
        except mariadb.ProgrammingError:
            print("There seems to be something wrong with SQL written.")
        except mariadb.OperationalError:
            print("There seems to be something wrong with the connection.")
        finally:
            if cursor != None:
                cursor.close()
            if conn != None:
                conn.rollback()
                conn.close()
            if rows == 1:
                return Response(json.dumps(artwork, default=str), mimetype="application/json", status=200)
            else:
                return Response("Updated failed", mimetype="text/html", status=500)
    
    elif request.method == 'DELETE':
        conn = None
        cursor = None
        art_id = request.json.get("id")
        print(art_id)
        rows = None
        user = None
        try:
            conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, port=dbcreds.port, database=dbcreds.database, host=dbcreds.host)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM artwork WHERE id=?", [art_id,])
            conn.commit()
            rows = cursor.rowcount
        except mariadb.dataError:
            print("There seems to be something wrong with your data.")
        except mariadb.databaseError:
            print("There seems to be something wrong with your database.")
        except mariadb.ProgrammingError:
            print("There seems to be something wrong with SQL written.")
        except mariadb.OperationalError:
            print("There seems to be something wrong with the connection.")
        finally:
            if cursor != None:
                cursor.close()
            if conn != None:
                conn.rollback()
                conn.close()
            if rows == 1:
                return Response("Delete Success", mimetype="text/html", status=204)
            else:
                return Response("Delete failed", mimetype="text/html", status=500)

@app.route('/enquiry', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def enquiries():
    if request.method == 'GET':
        conn = None
        cursor = None
        enquiries = None
        art_id = request.args.get("art_id")
        print(art_id)
        try:
            conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, port=dbcreds.port, database=dbcreds.database, host=dbcreds.host)
            cursor = conn.cursor()
            if art_id != None and art_id != "":
                cursor.execute("SELECT enquiry.id, enquiry.firstname, enquiry.lastname, enquiry.message, enquiry.email, enquiry.created_at, enquiry.art_id, artwork.name, artwork.url FROM enquiry INNER JOIN artwork ON enquiry.art_id = artwork.id WHERE enquiry.art_id=? ORDER BY enquiry.created_at DESC", [art_id])
                rows = cursor.fetchall()
                print(rows)
                enquiries = []
                print(enquiries)
                headers = [i[0] for i in cursor.description]
                for row in rows:
                    enquiry = dict(zip(headers, row))
                    print(enquiry)
                    enquiries.append(enquiry)
                    print(enquiries)
            else:
                cursor.execute("SELECT enquiry.id, enquiry.firstname, enquiry.lastname, enquiry.message, enquiry.email, enquiry.created_at, enquiry.art_id, artwork.name, artwork.url FROM enquiry INNER JOIN artwork ON enquiry.art_id = artwork.id ORDER BY enquiry.created_at DESC")
                rows = cursor.fetchall()
                enquiries = []
                headers = [i[0] for i in cursor.description]
                for row in rows:
                    enquiry = dict(zip(headers, row))
                    print(enquiry)
                    enquiries.append(enquiry)
        except mariadb.dataError:
            print("There seems to be something wrong with your data.")
        except mariadb.databaseError:
            print("There seems to be something wrong with your database.")
        except mariadb.ProgrammingError:
            print("There seems to be something wrong with SQL written.")
        except mariadb.OperationalError:
            print("There seems to be something wrong with the connection.")
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
            if(enquiries != None):
                return Response(json.dumps(enquiries, default=str), mimetype="application/json", status=200)
            else:
                return Response("Something went wrong!", mimetype="text/html", status=500)

    elif request.method == 'POST':
        conn = None
        cursor = None
        art_id = request.json.get("art_id")
        firstname = request.json.get("firstname")
        lastname = request.json.get("lastname")
        email = request.json.get("email")
        message = request.json.get("message")
        rows = None
        comment = None
        try:
            conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, port=dbcreds.port, database=dbcreds.database, host=dbcreds.host)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO enquiry(firstname, lastname, email, message, art_id) VALUES(?, ?, ?, ?, ?)", [firstname, lastname, email, message, art_id])
            conn.commit()
            rows = cursor.rowcount
            if rows == 1:
                enquiry_id = cursor.lastrowid
                print(enquiry_id)
                cursor.execute("SELECT enquiry.id, enquiry.firstname, enquiry.lastname, enquiry.message, enquiry.email, enquiry.created_at, enquiry.art_id, artwork.name, artwork.url FROM enquiry INNER JOIN artwork ON enquiry.art_id = artwork.id WHERE enquiry.id=?", [enquiry_id])
                row = cursor.fetchone()
                print(row)
                enquiry = {}
                headers = [i[0] for i in cursor.description]
                enquiry = dict(zip(headers, row))
        except mariadb.dataError:
            print("There seems to be something wrong with your data.")
        except mariadb.databaseError:
            print("There seems to be something wrong with your database.")
        except mariadb.ProgrammingError:
            print("There seems to be something wrong with SQL written.")
        except mariadb.OperationalError:
            print("There seems to be something wrong with the connection.")
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
            if(rows == 1):
                return Response(json.dumps(enquiry, default=str), mimetype="application/json", status=201)
            else:
                return Response("Something went wrong!", mimetype="text/html", status=500)
    
    elif request.method == 'PATCH':
        conn = None
        cursor = None
        token = request.json.get("token")
        comment_content = request.json.get("content")
        comment_image = request.json.get("image")
        comment_id = request.json.get("id")
        user = None
        rows = None
        comment = None
        try:
            conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, port=dbcreds.port, database=dbcreds.database, host=dbcreds.host)
            cursor = conn.cursor() 
            cursor.execute("SELECT * FROM user_session WHERE loginToken=?", [token,])
            user = cursor.fetchone()
            print(user)
            if user != None and user != []:
                user_id = user[2]
                print(user_id)
                if comment_content != "" and comment_content != None:
                    cursor.execute("UPDATE comment SET content=? WHERE id=? AND user_id=?", [comment_content, comment_id, user_id])
                if comment_image != "" and comment_image != None:
                    cursor.execute("UPDATE comment SET image=? WHERE id=? AND user_id=?", [comment_image, comment_id, user_id])
                conn.commit()
                rows = cursor.rowcount
                print(rows)
                cursor.execute("SELECT comment.id, comment.content, comment.image, comment.created_at, comment.user_id, comment.tweet_id, users.username FROM comment INNER JOIN users ON comment.user_id = users.id WHERE comment.id=?", [comment_id])
                comment_row = cursor.fetchone()
                print(comment_row)
                comment = {}
                headers = [i[0] for i in cursor.description]
                comment = dict(zip(headers, comment_row))
                print(comment)
        except mariadb.dataError:
            print("There seems to be something wrong with your data.")
        except mariadb.databaseError:
            print("There seems to be something wrong with your database.")
        except mariadb.ProgrammingError:
            print("There seems to be something wrong with SQL written.")
        except mariadb.OperationalError:
            print("There seems to be something wrong with the connection.")
        finally:
            if cursor != None:
                cursor.close()
            if conn != None:
                conn.rollback()
                conn.close()
            if rows == 1:
                return Response(json.dumps(comment, default=str), mimetype="application/json", status=200)
            else:
                return Response("Updated failed", mimetype="text/html", status=500)
    
    elif request.method == 'DELETE':
        conn = None
        cursor = None
        enquiry_id = request.json.get("id")
        rows = None
        try:
            conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, port=dbcreds.port, database=dbcreds.database, host=dbcreds.host)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM enquiry WHERE id=?", [enquiry_id])
            conn.commit()
            rows = cursor.rowcount
        except mariadb.dataError:
            print("There seems to be something wrong with your data.")
        except mariadb.databaseError:
            print("There seems to be something wrong with your database.")
        except mariadb.ProgrammingError:
            print("There seems to be something wrong with SQL written.")
        except mariadb.OperationalError:
            print("There seems to be something wrong with the connection.")
        finally:
            if cursor != None:
                cursor.close()
            if conn != None:
                conn.rollback()
                conn.close()
            if rows == 1:
                return Response("Delete Success", mimetype="text/html", status=204)
            else:
                return Response("Delete failed", mimetype="text/html", status=500)
