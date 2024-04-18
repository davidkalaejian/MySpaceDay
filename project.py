import requests
import re
from io import BytesIO
from PIL import Image
from datetime import datetime, timedelta
from fpdf import FPDF, XPos, YPos
from pyfiglet import Figlet
from countryinfo import CountryInfo

# Create a class to store info about the user
class Person:
    def __init__(self):

        # Construct an object of the Person class with the input information from each function
        self.name = get_name()
        self.birthday = get_birthday()
        self.location = get_location()

    def __str__(self):

        # Return a string with the constructed object of the class
        return f"I am {self.name}, born on {self.birthday}, in {self.location}!\n"

def main():

    # Create an object of the class Person
    person = Person()

    # Call the function the create a pdf with the constructed Person object
    create_pdf(person)

    # Create a figlet object and print a success message with ASCII art
    figlet = Figlet()
    figlet.setFont(font="larry3d")
    print(figlet.renderText("Success!"))

    # Print the metadata of the constructed Person object
    print(person)

def get_today():

    # Return current date
    return datetime.today()

def create_pdf(person):

    # Get the APOD photo, the title and the explanation from the apod function
    apod, title, explanation = get_apod(person)

    # Get the number of hours elapsed since the birthdate from the elapsed function
    hours = elapsed(person)

    # Get info about the country from the countr_info function
    cnt, pop, reg = country_info(person)

    # Create FPDF object
    pdf = FPDF()

    # Add a page and get pdf dimensions for later use
    pdf.add_page()

    pdf_w = pdf.w
    pdf_h = pdf.h

    # Image dimensions for the pdf
    img_w = 150
    img_h = 0

    # Set font and print the pdf title
    pdf.set_font("helvetica", "B", 30)
    pdf.cell(0, 20, person.name, new_x=XPos.LEFT, new_y=YPos.NEXT, align="C")

    # Print info about the hours elapsed from the birthdate
    pdf.set_font("helvetica", "", 10)
    pdf.cell(0, 5, f"It has been {hours:,} hours since you were born in {person.location}!", new_x=XPos.LEFT, new_y=YPos.NEXT, align="C")


    # Print info about the country
    pdf.cell(0, 5, f"{cnt} is a wonderful country located in {reg} and has a population of {pop:,}!", new_x=XPos.LEFT, new_y=YPos.NEXT, align="C")

    pdf.ln(10)

    # Print text for the image
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(0, 10, "Your NASA Astronomy Photo of Your Day is", new_x=XPos.LEFT, new_y=YPos.NEXT, align="C")

    pdf.ln(5)

    # Add the APOD image
    pdf.image(apod, x=(pdf_w - img_w) / 2, w=img_w, h=img_h)

    # Print the image title
    pdf.set_font("helvetica", "I", 10)
    pdf.cell(0, 10, title, new_x=XPos.LEFT, new_y=YPos.NEXT, align="L")

    # Print the image description
    pdf.set_font("helvetica", "", 10)
    pdf.multi_cell(0, 10, explanation, max_line_height=pdf.font_size*1.2)

    # Output the resulting pdf
    pdf.output("MyReport.pdf")

def get_apod(person):

    # URL for requesting APOD image from NASA with the person's birthday
    request_url = f"https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY&date={person.birthday}"

    # Make a request to the api
    response = requests.get(request_url, stream=True)

    # Get the response json and needed info from the response
    json = response.json()
    image_url = json["url"]
    title = json["title"]
    explanation = json["explanation"]

    # Make a request to get the actual image
    image_response = requests.get(image_url, stream=True)

    # Open the image from the APOD response
    apod = Image.open(BytesIO(image_response.content)).convert('RGB')

    return apod, title, explanation

def elapsed(person):

    # Create a datetime object from the person's birthday
    birthday_date = datetime.strptime(person.birthday, '%Y-%m-%d')

    # Get todays date as a datetime object
    today = get_today()

    # Calculate elapsed time from the person's birthday and convert to hours
    elapsed_time = today - birthday_date
    hours = round(elapsed_time.total_seconds() / 3600)

    return hours

def country_info(person):

    while True:
        try:
            # Get the country from the user's location field
            matches = re.search(r"^(\w+),?\s([\w\s]+)", person.location)
            cnt = matches.group(2)

            # Create a country info object with the provided country
            country = CountryInfo(cnt)

            # Store population and subregion data about the country in variables
            pop = country.population()
            reg = country.subregion()

        except (ValueError, KeyError, TypeError):

            print("\nPlease input a real City, Country combination\n")
            person.location = get_location()

        else:

            return cnt, pop, reg

def get_name():

    while True:
        try:

            # Try to get user input and convert to titlecase, strip whitespace
            name = input("Full name: ").title().strip()

            # If no name provided use default value
            if not name:
                return "Michael Scott"

            # If inputted name is a number raise error
            if name.isdigit():
                raise ValueError
                continue

            return name

        except ValueError:

            # Print error message if provided number for name
            print("\nFormat: Alphabetic characters only\n")

def get_birthday():

    while True:
        try:

            # Get user's birthday and strip whitespace
            birthday = input("Birthday (YYYY-MM-DD): ").strip()

            # Minimum and maximum values for date
            min_date = datetime(1995, 6, 16)
            max_date = get_today() - timedelta(days=1)

            # If no date is provided, default to current date
            if not birthday:
                return max_date.strftime('%Y-%m-%d')

            # Create a datetime object with provided birthday
            birthday_date = datetime.strptime(birthday, '%Y-%m-%d')

            # Check that the birthday is within supported range
            if birthday_date > max_date or birthday_date < min_date:
                raise ValueError
                continue

            else:
                return birthday

        except ValueError:

            # If user provides invalid date print error
            print("\nFormat: YYYY-MM-DD (Minimum 1995-06-16)\n")

def get_location():

    while True:
        try:

            # Try to get user's location, convert to titlecase and strip whitespace
            location = input("Birthplace (City, Country): ").title().strip()

            # If no location is provided return default value
            if not location:
                return "Scranton, United States"

            # Raise error if location does not have two required parts
            if not re.search(r"^\w+,?\s[\w\s]+", location):
                raise ValueError
                continue

            return location

        except ValueError:

            # If user provides invalid location input print error
            print("\nFormat: City, Country\n")

if __name__ == "__main__":
    main()
