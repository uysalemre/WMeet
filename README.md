# WMeet 

The easiest way to send notifications and getting response from your friends for your meeting organizations. 

## INTRODUCTION

A meeting organizer application which has multi-channel communication capabilities and independent from using application. The meeting organizer application need to have an editor which creates events and defines time, address, attendees. After creating event with its properties editor needs to add attendees information to app. According to available communication channels of attendees application sends notifications to them and attendee defines his/her attendance status with replying this message.

## Flowchart of the Application

<img width="401" alt="image" src="https://user-images.githubusercontent.com/32219894/71528389-9c6ef180-28f0-11ea-8305-bb519764cdf9.png">

## Communication Channels 

#### Telegram
It is not proper for our application because we can create Bot from telegram and if we want to send notification user needs to sign-up for that bot.

#### Whatsapp 
It is not proper for our application because if we want to send notification to user, we need to reach the current user’s Whatsapp web application. For each message we need to open a new tab, so user may be scare about this.

#### Twitter 
Twitter did not accepted our developer account.

#### Instagram 
In Instagram there is no API for sending direct messages. 

#### Facebook
For Facebook we used fbchat library to send messages and notifications. 

#### Email 
We used server based email so from one email we send our invitations and notifications. 

#### Phone 
For sending messages to phone numbers all existing APIs has huge prices.



## Future Work

   - co-editor feature for events. 
   - Add attendees from file
   - API
   
## HOW TO RUN ?

#### 1st Install Requirements

    pip install -r requirements.txt


#### 2nd Go and Fill Some Required Spaces

In **settings.py** file you need to fill spaces below with your gmail account properties.

      EMAIL_HOST_USER = ‘’
      EMAIL_HOST_PASSWORD = ''
      
After that in **general_queries.py** you need to fill spaces below with facebook account properties.

    self.faceadminemail = ‘’
    self.faceadminpassword = ‘’


#### 3rd Setup Application 
    python manage.py makemigrations MeetingOrganizer 
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver
 
 
 ## ScreenShots
 
 <img width="416" alt="image" src="https://user-images.githubusercontent.com/32219894/71528580-94fc1800-28f1-11ea-85a3-90201c5dd226.png">
 
 <img width="416" alt="image" src="https://user-images.githubusercontent.com/32219894/71528588-9e858000-28f1-11ea-9199-e2a0b9f2b7c6.png">
 
 
 <img width="416" alt="image" src="https://user-images.githubusercontent.com/32219894/71528595-a7765180-28f1-11ea-8791-27eae6b4555c.png">


<img width="416" alt="image" src="https://user-images.githubusercontent.com/32219894/71528605-b3faaa00-28f1-11ea-9097-5528a11d3f39.png">















