# MySpaceDay

#### Description:
**MySpaceReport** is a lightweight Python CLI app that takes as input the user's name, birthday date, and location, and generates a report that includes a few facts about the birthday and the location, and also makes a call to the Astronomy Photo Of the Day API from NASA to get the astronomy photo of the users birthday. The results are then written to a pdf file including the title of the APOD photo and its description.

## Usage

```
python project.py
```

## ✨ How it works
The project.py file contains all of the code for this app, however you may notice that it makes use of several third party libraries and API calls to make it all work.

***Getting inputs and constructing a Person object***
- The app will automatically prompt the user to input their name, birthday, and location, in order to construct a "Person" object
- Each of the functions used for getting these inputs have their corresponding validation criteria (although not very exhaustive at the moment)
- All three inputs need to pass validation, or if none is provided default values will be used, in order to proceed with the program

***Getting APOD, elapsed hours, and info about the country***
- The person object will be passed to a function which will get the Astronomy Photo Of the Day from NASA API, the title, and the description of the photo
- The person object is also passed to an "elapsed" function to calculate the number of hours since your birthday, and also get some interesting info about your country

***Creating the PDF***
- All of this info is then passed to another function that is responsible for creating a PDF file and writing all of the info there
- In case of a successful run the program also prints a success message with ASCII art using the Figlet library

***Default Values***
- If the user does not provide inputs the program uses default values to create a report for "Michael Scott from Scranton, United States, who's birthday is the day before the current date".

> 💡 PRO TIP: The resulting PDF is then stored in the main directory of the project, and **will be overwritten** every time you run the program, so make sure to save the ones you like!


## ⚠️ Limitations
- For getting the Astronomy Photo Of the Day the inputted date needs to be after 1995-06-16, because it is the earliest date supported by APOD API. Feel free to leave it blank if your birthday is before 1995-06-16, in that case the program will use the default value (a day before your current date).
- There are not many limitations around the name and location as an attempt to support a wider range of users, with middle names, prefixes, etc.
- Third party APIs are using their respective "Demo keys", so it will be limited to 30 uses per day per user.

> 💡 PRO TIP: Be free to try out different dates to get all kinds of unique APODs and learn more about space events!

## 🧪 Testing
For unit tests for the program I used different kinds of mocks and patches because the program uses .today()'s date in several functions, and also to get around constructing a mock "Person" object for the test, as usually the "Person" object is constructed using user input.
