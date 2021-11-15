import logging
import azure.functions as func
import psycopg2
import os
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def main(msg: func.ServiceBusMessage):

    notification_id = int(msg.get_body().decode('utf-8'))
    logging.info('Python ServiceBus queue trigger processed message: %s',notification_id)

    # connection to database
    conn = psycopg2.connect("dbname=test user=postgres")

    # Open a cursor to perform database operations
    cur = conn.cursor()
    
    try:
        # Get notification message and subject from database using the notification_id
        cur.execute("Select massage, subject from notification where id = %s;",notification_id)
        row = cur.fetchone()
        notification = Notification(row[0],row[1])
        
        # Get attendees email and name
        cur.execute("Select email, first_name from attendee;")
        rows = cur.fetchall()
        
        # Loop through each attendee and send an email with a personalized subject
        attendees = []
        for row in rows:
            attendee = Attendee(row[0], row[1])
            attendees.append(attendee)
        email_msg = Mail(
                from_email="saly.moubarak@gmail.com",
                to_emails=attendee.email ,
                subject= notification.subject,
                plain_text_content= notification.message )
        email_client = SendGridAPIClient("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")
        email_client.send(email_msg)
        
        # Update the notification table by setting the completed date and updating the status with the total number of attendees notified
        cur.execute('UPDATE notification set status = Notified %s attendees, completed_date = %s where id = %s', (len(attendees), datetime.today(), notification_id ))
        conn.commit()
    
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
    finally:
        # Close connection
        cur.close()
        conn.close()

class Notification(object):
    def __init__(self, msg, sub):       
        self.message = msg        
        self.subject = sub

class Attendee(object):
    def __init__(self, email, fname):
        self.email = email
        self.first_name = fname

     