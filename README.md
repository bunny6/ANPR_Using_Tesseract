# ANPR_Using_Tesseract

> Introduction 

Number plate authentication system is a full-fledged system for authentication of the cars using their number plates which can 
have many real-world use cases. For example automated garage opening.

To ensure that the access must be given to the users who have registered their car’s number plate in the system.


> Scope

By using Yolov5 and tesseract, we can detect an object and extract the text from the object. This application can be used in many real-world cases such as the Entry gate of Society ,Offices, Colleges,etc.

> Technologies used

- Python.

- Tesseract.

- Yolov5.

- Optical Character Recognition.

- PostgreSql.

> Steps performed

1 : Downloaded car images with number plates.
    
Downloaded car images of high quality and cleaned the images which were  blurred and not useful for prediction.
          
2 : Label the images.

Labeled the data images using labelImg tool as it is the required input format for yolov5 algorithm.

3 : Used the Yolov5 algorithm.

By using google collab, Cloned the Yolov5 algorithm and trained the model by passing images and downloaded the best.pt file.

4 : Added some cars license numbers to the postgresql database.

For the authentication process, I added the car license number into the database.

5 : Passing the cropped image to tesseract.

By using tesseract, I extracted the text from the image. Then the authentication process starts. If the car license number is available in the database, it will return Car Access Granted and if the car license number is not available in the database it will return car access denied on the web page.
