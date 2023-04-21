import requests
import base64
import json

# set the API endpoint
API_ENDPOINT = "https://api.clearview.ai/graphql"

# set the API key and secret
API_KEY = "your_api_key"
API_SECRET = "your_api_secret"

# set the image path
IMAGE_PATH = "path/to/image.jpg"

# read the image file as binary
with open(IMAGE_PATH, "rb") as image_file:
    image_data = image_file.read()

# encode the image as base64
encoded_image = base64.b64encode(image_data).decode()

# construct the GraphQL query
query = """
{
    search(
        image: "%s",
        size: 10
    ) {
        edges {
            node {
                id,
                urls,
                matches {
                    id,
                    name,
                    type,
                    confidence,
                    media {
                        url,
                        type
                    }
                }
            }
        }
    }
}
""" % encoded_image

# set the headers and authentication
headers = {
    "Content-Type": "application/json",
    "X-User-Email": API_KEY,
    "X-User-Token": API_SECRET
}

# send the GraphQL query to the API endpoint
response = requests.post(API_ENDPOINT, headers=headers, data=json.dumps({"query": query}))

# parse the response JSON and extract the matches
matches = response.json()["data"]["search"]["edges"][0]["node"]["matches"]

# print the matches
for match in matches:
    print("Name: %s, Type: %s, Confidence: %s, URL: %s" % (match["name"], match["type"], match["confidence"], match["media"]["url"]))
