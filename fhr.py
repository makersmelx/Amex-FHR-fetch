import requests
from bs4 import BeautifulSoup, element as bs4Element
import re
import json
from cache import *

"""
    Get urls for all FHR properties with the brand
    will cache the html of the brand page
"""


def pullPropertyUrlsByBrandLink(brandUrl):
    url = f"https://www.americanexpress.com/en-us/travel/discover/{brandUrl}"
    brand = re.sub("brand/", "", brandUrl)
    createDirWithRelativePath(brand)
    brandPage = f"{brand}/index"
    if isRelativePathExists(brandPage):
        with open(getAbsolutePath(brandPage), "r+") as file:
            htmlDoc = file.read()
    else:
        response = requests.get(url)
        htmlDoc = response.text
        with open(getAbsolutePath(brandPage), "w+") as file:
            file.write(htmlDoc)

    soup = BeautifulSoup(htmlDoc, 'html.parser')
    properties = soup.find_all(
        name="a", class_="property-card", attrs={"data-programclass": re.compile("pc-fhr")}, href=re.compile("travel/discover/property"),
    )
    return [x["href"] for x in properties], brand


"""
    Pull the information of an FHR property with the property url
    will cache the html of the property page
"""


def pullProperty(propertyLink, brand):
    url = f"https://www.americanexpress.com/{propertyLink}"

    name = re.sub(r"^(\S*)/travel/discover/property/", "", propertyLink)
    name = re.sub(r"\?linknav(\S*)$", "", name)
    name = re.sub(r"/", "-", name)

    propertyCache = f"{brand}/{name}"
    if isRelativePathExists(propertyCache):
        with open(getAbsolutePath(propertyCache), "r+") as file:
            htmlDoc = file.read()
    else:
        response = requests.get(url)
        htmlDoc = response.text
        with open(getAbsolutePath(propertyCache), "w+") as file:
            file.write(htmlDoc)
    soup = BeautifulSoup(htmlDoc, 'html.parser')
    property = {}

    name = soup.find(class_="pt-supplierName")
    property["name"] = name.contents[0]

    brand = soup.find(class_="pt-brand")
    property["brand"] = brand.contents[0]

    # only the first one is the title
    title = soup.find(class_="pl-section-head")
    introduction = soup.find(class_="pl-description")
    property["description"] = {
        "title": title.contents[0],
        "introduction": introduction.contents[0]
    }

    city = soup.find(class_="pt-location")
    property["city"] = (city.contents[0]).contents[0]

    location = soup.find(class_="pl-location")
    property["location"] = location.contents[0]

    benefitsList = soup.find(class_="pibUL")
    benefitsItems = benefitsList.find_all("li")
    benefits = []
    for benefit in benefitsItems:
        # Check each benefit. At <li> tag now
        result = ""
        # At children inside <li> tag
        for item in benefit.contents:
            # Unique experience is presented as a non-tag NavigableString
            if isinstance(item, bs4Element.NavigableString):
                result += item.string
            else:
                for text in item.contents:
                    result += text
        benefits.append(result)
    property["benefits"] = benefits

    details = {}
    detailsBlocks = soup.find_all(class_="pl-written")
    for block in detailsBlocks:
        key = (block.find(class_="plw-head").contents[0]).contents[0]
        value = block.find("p").contents[0]
        details[key] = value
    property["details"] = details
    return property


"""
    Get all FHR properties with information
    will cache the property list
"""


def pullProperties():
    cache = "properties.json"
    properties = []

    if isRelativePathExists(cache):
        with open(getAbsolutePath(cache), "r+") as file:
            properties = json.loads(file.read())
    else:
        brandsCache = "brands"
        if (isRelativePathExists(brandsCache)):
            with open(getAbsolutePath(brandsCache), "r+") as file:
                htmlDoc = file.read()
        else:
            response = requests.get(
                "https://www.americanexpress.com/en-us/travel/discover/brands")
            htmlDoc = response.text
            with open(getAbsolutePath(brandsCache), "w+") as file:
                file.write(htmlDoc)

        soup = BeautifulSoup(htmlDoc, 'html.parser')
        brands = soup.find_all("a", class_="brand-tile")
        for brand in brands:
            subLink = brand["href"]
            propertyLinks, brandName = pullPropertyUrlsByBrandLink(subLink)
            for propertyLink in propertyLinks:
                print(propertyLink)
                property = pullProperty(propertyLink, brandName)
                properties.append(property)
        with open(getAbsolutePath(cache), "w+") as file:
            file.write(json.dumps(properties))
    return properties
