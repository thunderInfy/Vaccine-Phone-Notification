## Using Selenium and Twilio to get notifications for vaccine slots in India

This repository holds the code for my [medium blog](https://medium.com/@aditya.rastogi/using-selenium-and-twilios-voice-api-to-call-myself-for-getting-my-vaccine-slot-booked-in-india-7e95626f02eb?sk=6db4c55a224da9821e0df39e2925fa3b). I used Selenium to do interactive web browsing on the [CoWIN](https://www.cowin.gov.in/home) website and whenever a vaccine slot shows up in my pincode, I receive a call on my phone using Twilio's Voice API. 

### Running the Code

I used selenium==3.141.0, bs4==0.0.1, pandas==1.0.3 and twilio==5.7.0 python modules for running this code. All you need to do is get an account at Twilio (follow the blog for more instructions) and fill out the relevant information in the data.json file. Then you just need to run cowin.py in your laptop. Just keep your laptop running with this code, and whenever the vaccine slots show up, you would get a call at your number (feel free to check this by running call.py directly). Also note that this code searches the CoWIN homepage after every 600 seconds. If you want to reduce this time duration between consecutive calls to say 5 mins, you can do so by changing time.sleep(600) to time.sleep(300) at the end of cowin.py file.
