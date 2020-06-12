## X-Ray Image Covid-19 Image Classifier

[![CircleCI](https://circleci.com/gh/andrewlee8247/computer-vision-covid-19/tree/development.svg?style=svg)](https://circleci.com/gh/andrewlee8247/computer-vision-covid-19/tree/development)

# Description

The Covid-19 Image Classifier is an application that utilizes machine learning 
on Google Cloud Platform (GCP) to predict the probability of a patient being positive for Covid-19. 

# Background

Beginning in 2019, the Covid-19 virus caused significant damage throughout the 
world. In haste to address the ongoing damage, scientific and medical experts have sought (and continue to seek out)
out new methods and technologies for treating, testing, and identifying the virus in humans. 

Computer vision technology can be leveraged to assist medical professionals in 
determining whether a patient is positive for Covid-19, utilizing x-ray images or CT scans. Currently, such technologies 
are used in determining other health conditions such as cancer.

# About the Data

Over 1290 images were collected from multiple open-source resources. The images include
x-ray images of Covid-19, pneumonia, and normal (no conditions) cases. For an application
utilizing machine learning, more data is always better. However, due to Covid-19 being a
new phenomena, the availability of Covid-19 imagery was limited. 
Image breakdown:
 - Normal – 500
 - Pneumonia – 500
 - COVID-19 - 293

# How it Works

The application utilizes Python as the primary language for system functionality. On the front-end, Python Flask
and HTML support the user interface. Continuous integration and continuous delivery are in place utilizing Circle CI. The 
code can be edited within Github and automatically updated within Cloud Repositories and directly to the live application via Cloud Run. 

The application utilizes two methods for determining the probability of an 
X-ray image being positive for Covid-19 - a GCP AutoML Cloud Vision tool and a custom model built using Python and Keras. 
The Cloud Vision tool is an automated machine learning tool that is fed images and with marginal effort trains and tests a model. 
The custom model was developed by the authors of the application where a convolutional neural network (CNN) has been trained and tested
on the same data used for the Cloud Vision tool.
The interface allows users to upload an X-ray image to the application. The application analyzes the image, 
and will predict if the patient has COVID, Pneumonia or is healthy.

Form data received from users is saved into BigQuery, where the data is collected and stored. Classification
scores (probability) are returned as a JSON response. The timestamp of requests, file names, and storage location (image uploaded) is also stored.

Images are stored in Cloud Storage (both the training/test data and the user input images). 

Two separate URLs are utilized - one for the Cloud Vison model (https://covid-3ghvym5f7q-uc.a.run.app/#form) and one for the 
custom model (https://covid-keras-3ghvym5f7q-uc.a.run.app/#form).

# The Model's Performance

The Cloud Vision model's accuracy is .86, with a precision score of .86 and recall score of .85. 
1164 images were used for training and 129 images were used for testing. 

The custom model's accuracy is .74, with a precision score of .75 and recall score of .74. 
1164 images were used for training and 129 images were used for testing. 

# Folders/Files

 - (Folder) .circleci: implements integration of CircleCI for continuous integration and continuous deployment
 - (Folder) app-automl: implements the GCP AutoML (Vision) application
 - (Folder) app-keras: implements the custom model version for the application (using an author built model as opposed to AutoML)
 - (Folder) tests: conduct testing on the application (front-end) and AutoML
 - (File) gitignore: what files Git should ignore
 - (File) Makefile: tells the system what to be executed
 - (File) conftest.py: 
 - (File) locustfile.py:
 - (File) requirements.txt: modules to be installed to support the application's functionality

# System Architecture

![System Architecture](https://i.ibb.co/VH86Sbg/Computer-Vision-Architecture-COVID-19-2.png)
 1. X-Ray images are uploaded to Cloud Storage that are used to train the classifier
 2. Updates to application are containerized and images are pushed to Google's Container Registry using CI/CD
 3. Container is deployed to Cloud Run automatically
 4. Prediction requests are sent to AutoML, images are stored in Cloud Storage, and data is user data is inserted into BigQuery
 5. Users/Clients can access the front-end through a public URL. API requests require and access token.

# Authors

Authors of this project include Andrew Lee, Jay Soto, Allison Ashley, and Michael Martley.


