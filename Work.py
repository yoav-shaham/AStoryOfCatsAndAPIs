from google.cloud import vision
import google.auth
import urllib
import boto3
import re
import smtplib
import time
import shelve
"""
please note that i have made all documents on the bucket public to the world
"""
#setting up shelve simple data saving
variables=shelve.open("file")
#sigining in to the bucket and google api
credentials, project_id = google.auth.default()
vision_client = vision.Client(project='My First Project', credentials=credentials)
s3 = boto3.resource("s3")
#-------------------------------------varaibles------------------
time_til_notification = 900
time_till_death = 1000
last_cheked_paths = []
LastChekedList = []
sent_notification = 0
user = ""
pwd = ""
recipient = ""
Bucket_URL = r"https://s3.eu-central-1.amazonaws.com/catfood002/"
Food_Labels = ["milk", "bread", "fish"]
#---------------------------------------------------------------

def send_email(subject, body):
    """
    Takes body and subject from pramaters, takes user, password and recepient from global variables
    :param subject: The email's subject
    :type subject: str
    :param body: The email's body text
    :type subject: str
    """
    global user, pwd, recipient
    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print 'successfully sent the mail'
    except:
        print "failed to send mail"


def update_last_ate():
    """
    updates the time variable in the shelves file and sent notification global variables while sending an email
    notifing the recepient the cat has been fed if there was a notification
    """
    global sent_notification,variables
    if sent_notification==1:
        send_email("Feeding the cat", "you have fed the cat and he is back to normal")
    variables["time"]=time.time()
    sent_notification = 0


def cat_died():
    """
    Sends email notifing recipient the cat has died
    """
    send_email("YOU MONSTER", "HOW COULD YOU KILL AND INOCCENT CAT")


def notification_email():
    """
    Sends email notyfing recepient to feed the virtual cat
    """
    send_email("Notifing You to FEED YOUR VIRTUAL CAT!!!!", "FEED THE CAT!!!!!")


def keyCheker(key):
    """
    Checks using regex if the key is a image type
    :param key: The key class object main wants to checvk
    :return: returns true if the key is a type png or jpg image otherwise returns false
    :rtype: bool
    """
    match = re.search(r"\.jpg|\.png", key.key)
    if match:
        return True
    else:
        return False


def check_photo(key):
    """
    Uses the adress from global variable Bucket url to get
    the file from aws bucket and using the global list Food_Labels
    it checks the google api returned variables
    :param key: The key class object main wants to check
    :returns: True if with atleast 50% likliood the image contains one of the food lables
    :rtype: bool
    """
    global Bucket_URL, Food_Labels
    opener = urllib.URLopener()
    myurl = Bucket_URL
    if not keyCheker(key):
        print "a non picture file was uploaded"
    myurl += key.key
    myfile = opener.open(myurl)
    file = myfile.read()
    image = vision_client.image(file)
    labels = image.detect_labels()
    for label in labels:
        if label.description == Food_Labels[0] or label.description == Food_Labels[1] or label.description == \
                Food_Labels[2]:
            if label.score > 0.5:
                return True
    return False


def main():
    global sent_notification, time_til_notification, time_till_death, last_cheked_paths, variables,user,pwd,recipient #getting globals

    user = raw_input("Please insert a gmail account username: ")#getting user and recepient info for emails
    pwd = raw_input("please enter your password: ")
    recipient = raw_input("please enter an email to recieve cat status emails: ")
    bucketLst = []
    for bucket in s3.buckets.all():#getting the first bucket
        print bucket
        bucketLst.append(bucket)
    bucket = bucketLst[0]
    print bucket
    for key in bucket.objects.all():#enter the original file keys contained in the bucket into the last_cheked_paths
        if key.key not in last_cheked_paths:#for future references
            last_cheked_paths.append(key.key)
    variables["time"]=time.time()#saves last changed time
    while variables["time"] + time_till_death > time.time():#checks if the cat already died and continues to the while
        for key in bucket.objects.all():#checks the keys and sends to check photo to check if its cat food
            if key.key not in last_cheked_paths:#if it is then updates the last time the cat ate and updates the
                print key.key#last checked paths
                if check_photo(key):
                    update_last_ate()
                last_cheked_paths.append(key.key)
            elif variables["time"] + time_til_notification < time.time() and sent_notification == 0:#checks if there is a need to notifi the recipientr of emails
                notification_email()
                sent_notification = 1

    cat_died()
    exit("The cat died")#exits cus the cat died


if __name__ == '__main__':
    main()