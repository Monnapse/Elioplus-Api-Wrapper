import requests
from lxml import html
from .types import CompanyListing, ProcessedHTML

class ElioplusClient:
    """
        Elioplus API Client
        Made by Monnapse

        This is a simple API wrapper for the Elioplus API.
    """
    def __init__(self):
        self.base_url = "https://elioplus.com"

    def process_listing(self, listing_element, i: int):
        name_elem = listing_element.xpath(f".//a[@id='MainContent_RdgResults_aCompanyName_{i}']/text()")
        msp_elem = listing_element.xpath(f".//a[@id='MainContent_RdgResults_aMSPs_{i}']/strong/text()")
        country_elem = listing_element.xpath(".//div[contains(@class, 'country')]/h4/text()")
        city_elem = listing_element.xpath(f".//a[@id='MainContent_RdgResults_aAllCityChannelPartners_{i}']/text()")
        overview_elem = listing_element.xpath(f".//span[@id='MainContent_RdgResults_LblOverview_{i}']/text()")

        categories_elem = listing_element.xpath(f"//*[@id='MainContent_RdgResults_divCategoriesArea_{i}']/div[2]/a")
        categories = []

        for cat in categories_elem:
            cat = cat.xpath(".//span/text()")

            if not cat or len(cat) == 0: continue

            cat_text = cat[0].strip()
            categories.append(cat_text)

        products_elem = listing_element.xpath(f"//*[@id='MainContent_RdgResults_divProductsArea_{i}']/div[2]/a")
        products = []

        for prod in products_elem:
            prod = prod.xpath(".//span/text()")

            if not prod or len(prod) == 0: continue

            prod_text = prod[0].strip()
            products.append(prod_text)

        if name_elem:
            name = name_elem[0].strip()
            msp_prop = True if msp_elem else False
            country_prop = country_elem[0].strip() if country_elem and len(country_elem) > 0 else "Unknown"
            city_prop = city_elem[0].strip() if city_elem and len(city_elem) > 0 else "Unknown"
            overview_prop = overview_elem[0].strip() if overview_elem and len(overview_elem) > 0 else "No overview available."

            #print("-----------------------------")
            #print(f"    Index: {i}")
            #print(f"    Name: {name}")
            #print(f"    MSP: {msp_prop}, Country: {country_prop}, City: {city_prop}")
            #print(f"    Categories: {categories}")
            #print(f"    Products: {products}")
            #print(f"    Overview: {overview_prop}")
            #print("-----------------------------")

            return CompanyListing(
                name=name,
                msp=msp_prop,
                country=country_prop,
                city=city_prop,
                categories=categories,
                products=products,
                overview=overview_prop
            )
        
        #else: # Listing name not found / doesnt exist
            #print(f"Listing {i}: Name not found")

    def process_listings(self, listings_elements, limit: int = 10):
        processed_listings = []

        for i in range(len(listings_elements)):
            if i >= limit and limit != -1:
                break
            processed_listings.append(self.process_listing(listings_elements[i], i))
            
        return processed_listings

    def process_html(self, content: str):
        tree = html.fromstring(content)

        listings = tree.xpath('//*[@id="MainContent_divMainContent"]/div[1]/div')

        #processed_listings = []

        # The max per page is 101
        pages = tree.xpath('//*[starts-with(@id, "MainContent_RptNav_LblNavPage_")]')
        total_pages = len(pages) if pages else 1

        #print(f"Total pages: {total_pages}")


        #while len(processed_listings) < limit or limit == -1:
        #processed_listings = self.process_listings(listings, limit=limit)
            
        return ProcessedHTML(
            tree=tree,
            listings=listings,
            pages=total_pages
        ) #self.process_listings(listings, limit=limit)
    
    def get_page(self, url: str):
        response = requests.get(url)

        if response.status_code != 200:
            raise Exception(f"Failed to retrieve data: {response.status_code}")
        
        return self.process_html(response.content)

    def browse(
            self,
            partner: str = "channel-partners", # Default partner type set to channel-partners
            region: str = "north-america", # Default region set to North America
            country: str | None = None, 
            state: str | None = None,
            city: str | None = None,
            vendor: str | None = None,
            limit: int = 10, # Default limit set to 10
            overwrite_url: str | None = None
        ):
        """
            https://elioplus.com/north-america/united-states/channel-partners/yealink?page=1
            https://elioplus.com/north-america/united-states/channel-partners/yealink?page=1
            Browse items.

            :param partner: Partner type.
            :param region: Region.
            :param country: Country.
            :param state: State.
            :param city: City.
            :param vendor: Vendor.
            :param limit: Number of items to retrieve. There is no limit to this parameter. If you want infinite then set it to -1.
            :param overwrite_url: Overwrite the URL completely (DONT INCLUDE PAGE POSITION).

            :return: List of items.
        """

        url = f"{self.base_url}/{region}{f'/{country}' if country else ''}/{partner}{f'/{state}' if state else ''}{f'/{city}' if city else ''}{f'/{vendor}' if vendor else ''}" if not overwrite_url else overwrite_url

        processed_html = self.get_page(f"{url}?page=1") # Get the first page

        to_fetch = limit
        for page in range(1, processed_html.pages + 1):
            listings = None
            total_pages: int = None

            if page == 1:
                listings = processed_html.listings
                total_pages = processed_html.pages
            else:
                processed_html = self.get_page(f"{url}?page={page}")
                listings = processed_html.listings
                total_pages = processed_html.pages

            new_limit = min(to_fetch, 101) if to_fetch != -1 else len(listings)
            print(f"Processing page {page}/{total_pages} with limit {new_limit}...")
            processed_listings = self.process_listings(listings, limit=new_limit)
            to_fetch -= len(processed_listings)

        return []

    def browse_url(self, url: str, limit: int = 10):
        return self.browse(overwrite_url=url, limit=limit)