from elioplus import ElioplusClient

elioplus = ElioplusClient()

if __name__ == "__main__":  
    print("This is a test module.")

    results = elioplus.browse(
        region="north-america",
        country="united-states",
        partner="channel-partners",
        vendor="yealink",
        limit=120
    )
    #results = elioplus.browse_url("https://elioplus.com/north-america/united-states/channel-partners/yealink?page=1", limit=10)

    print(results)
    print(f"Total results: {len(results)}")