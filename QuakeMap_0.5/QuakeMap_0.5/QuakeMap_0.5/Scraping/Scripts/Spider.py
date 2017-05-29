import scrapy, time, zmq, os, json

class Spider(scrapy.Spider):
    name = 'Spider'
    count = 0
    def __init__(self, maxPages=20, place='europe', *args, **kwargs):
        super(Spider, self).__init__(*args, **kwargs)
        self.maxPages = int(maxPages)
        self.start_urls = ['http://earthquaketrack.com/' + place + '/recent']
    
    def parse(self, response):
        if(response.css('div.quake-info').extract_first() is not None):
            if(self.count <= self.maxPages):
                for quakeInfo in response.css('div.quake-info'):
    
                    dateTime = quakeInfo.css('abbr ::attr(title)').extract_first()
                    magnitude = quakeInfo.css('span ::text').extract_first().split()[0]
                    epicenter = quakeInfo.css('div.quake-info-window').xpath("p[position() = 2]").re(r'Epicenter at (.*)')
                    latitude = epicenter[0].split(', ')[0]
                    longitude = epicenter[0].split(', ')[1]
                    depth = quakeInfo.css('div.quake-info-window').xpath("p[contains(text(), 'Depth')]/text()").extract_first().split()[1]
                    locationData = quakeInfo.css('div.quiet').xpath('a/text()').extract()
                    try: 
                        city = locationData[0]
                        location = locationData[1]
                        country = locationData[2]
                    except IndexError:
                        location = locationData[0]
                        yield {'DateTime' : dateTime, 'Magnitude' : magnitude, 'City' : '', 'Location': location, 'Country' : '', 'Longitude' : longitude, 'Latitude' : latitude, 'Depth' : depth}    
                    else:
                        yield {'DateTime' : dateTime, 'Magnitude' : magnitude, 'City' : city, 'Location': location, 'Country' : country, 'Longitude' : longitude, 'Latitude' : latitude, 'Depth' : depth}

                next_page = response.css('a.next_page ::attr(href)').extract_first()
                if next_page is None:
                    next_page = response.css('div.pagination a:nth-child(2) ::attr(href)').extract_first()
                if next_page:
                    self.count += 1
                    yield scrapy.Request(response.urljoin(next_page), callback=self.parse)
            else:
                self.count = 0