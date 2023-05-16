import sys
import csv
import io

from bs4 import BeautifulSoup

css = open('style.css').read()
csv = csv.DictReader(io.open(sys.argv[1], "r", encoding = "utf-8-sig"))

categories = []
rawItems = []
for item in csv:
    rawItems.append(item)
    category = item["item_category"]
    if category not in categories:
        categories.append(category)


list = dict()
for category in categories:
    categoryItems = []
    for item in rawItems:
        itemCategory = item["item_category"]
        if category == itemCategory:
            categoryItems.append(item)
    list[category] = categoryItems


html = "<body>"
html += "<style>" + css + "</style>"
html += "<div class=\"menu-body\">"
html += "<h1 class=\"menu-section-title\">Ogato</h1>"

for index, category in enumerate(categories):
    items = list[category]
    sectionClass = 'menu-section-wide' if (index + 1) % 3 == 0 else 'menu-section'
    html += "<div class=\"" + sectionClass + "\"><h2 class=\"menu-section-title\">" + category + "</h2>"


    for item in items:
        description = item["item_description"]
        if item["item_vegetarian"] == "TRUE":
            description += " &bull; " + item["item_vegetarian_description"]
        if item["item_vegan"] == "TRUE":
            description += " &bull; " + item["item_vegan_description"]
        if item["item_glutenfree"] == "TRUE":
            description += " &bull; " + item["item_glutenfree_description"]


        html += "<div class=\"menu-item\">"

        html += "<div class=\"menu-item-name\">" + item["item_name"] + "</div>"
        html += "<div class=\"menu-item-price\">" + item["item_price"] + "</div>"
        html += "<div class=\"menu-item-description\">" + description + "</div>"

        html += "</div>"


    html += "</div>"

html += "</div>"
html += "</body>"

soup = BeautifulSoup(html, "html.parser")

html = soup.prettify()


html_file = open(sys.argv[2], "w")
html_file.write(html)
html_file.close()
