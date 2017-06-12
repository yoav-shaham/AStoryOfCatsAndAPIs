# AStoryOfCatsAndAPIs
The python script checks the paths of a given bucket and when it notices 
a new file was uploaded it uses the google cloud api to check if the 
photo is of a apropriate food tag if it is it updates the file containing 
the last time fed. If the cat hasnt been fed in 15 minutes it sends a warning
if it is fed after the fifteen minutes but not before 16 minutes 40 seconds it 
sends back to normal email else it sends cat died email.
# Getting Started
In order to run the script succecfully you will need these python librarys:
1)google.cloud 
2)google.auth
3)urllib
4)boto3
5)regex
6)smtplib
7)time
8)shelve
And make sure you have installed python 2.7.
# Starting Up The Program
In order to start the program you will need to if you want to use your own bucket and own google api update the credentials 
for both.
Then just start the program and it will begin the inital scan of the s3 bucket and then just start feeding the cat.
# Other 
For any other questions I am available at shaham.yoav2000@gmail.com 

