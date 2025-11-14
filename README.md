# ElioplusApiWrapper
Elioplus api wrapper with simple methods

### [Example Code Link](https://github.com/Monnapse/Elioplus-Api-Wrapper/blob/main/__main__.py)
```python
results = elioplus.browse(
    region="north-america",
    country="united-states",
    partner="channel-partners",
    vendor="yealink",
    limit=-1 # -1 for infinite, but any limit works
)
#results = elioplus.browse_url("https://elioplus.com/north-america/united-states/channel-partners/yealink", limit=-1) # You can also use browse_url to directly specify a URL

print(f"Total results: {len(results)}")
for i in range(10):
    listing = results[i]
    print(f"--------------------------------------{i+1}----------------------------------------")
    print(f"    Name: {listing.name}")
    print(f"    MSP: {listing.msp}, Country: {listing.country}, City: {listing.city}")
    print(f"    Categories: {listing.categories}")
    print(f"    Products: {listing.products}")
    print(f"    Overview: {listing.overview}")
    print("-------------------------------------------------------------------------------")
```