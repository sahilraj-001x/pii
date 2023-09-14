from geopy.geocoders import Nominatim

add = input("Enter your address : ")

try:
    geolocator = Nominatim(user_agent="sample app")
    data = geolocator.geocode("burfi ghar sweet shop, sri ram nagar, hyderabad, telangana")
    a = data.raw.get("lat")
    b = data.raw.get("lon")
    print(a, b)
    # print(geolocator.reverse(a, b))
except:
    print("Can't find the location")
# data.point
# data.point.latitude, data.point.longitude

# print(geolocator.reverse('17.342429 78.5978501'))
