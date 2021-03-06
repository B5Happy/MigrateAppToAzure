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
    conn = psycopg2.connect(host="uda3db.postgres.database.azure.com",
                                database="postgres",
                                user="saly@uda3db",
                                password="Itachi0812")

    # Open a cursor to perform database operations
    cur = conn.cursor()
    logging.info('Connecting to the PostgreSQL database...')
    
    try:
        # Get notification message and subject from database using the notification_id
        logging.info(notification_id)
        cur.execute("Select message, subject from notification where id = %s;",(notification_id,))
        row = cur.fetchone()
        notification = Notification(row[0],row[1])
        logging.info(notification)
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
        email_client = SendGridAPIClient(os.environ['SENDGRID_API_KEY'])
        email_client.send(email_msg)
        logging.info("Successfully notified %s", attendee.email)
        status = 'Notified {} attendees'.format(len(attendees))
        # Update the notification table by setting the completed date and updating the status with the total number of attendees notified
        cur.execute('UPDATE NOTIFICATION SET STATUS = %s, COMPLETED_DATE = %s WHERE ID = %s', (status, datetime.utcnow(), notification_id,))
        conn.commit()
        logging.info("update successful")

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

     