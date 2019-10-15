import arrow
import requests
import geocoder
import geopandas

import pandas as pd
import shapely.geometry as geom



class FoodTrucks:
    DEFAULT_SOURCE_URL = 'https://data.sfgov.org/api/geospatial/rqzj-sfat?method=export&format=GeoJSON'  # "Live" GeoJSON food truck locations

    def __init__(self, source: str = None) -> None:
        self.src_url = source or self.DEFAULT_SOURCE_URL
        self.update()

    def update(self) -> None:
        self.geodata = geopandas.read_file(self.src_url)
        self.updated_at = arrow.get()
        self.geodata['expirationdate'] = pd.to_datetime(self.geodata['expirationdate'])
        self.geodata = self.geodata.query('not x.isnull() &'
                                          'not expirationdate.isnull() &'
                                          f'expirationdate > "{self.updated_at:YYYY-MMM-DD}"')

    def suggest(self, location: str = None, count: int = 20) -> pd.DataFrame:
        if location is None:
            loc = geocoder.ip('me')
        else:
            loc = geocoder.osm(location)

        if loc is None:
            raise Exception(f"Unable to geocode current location. [location={location}]")

        self.loc = geom.Point(loc.latlng)
        self.geodata['distance_to_us'] = self.geodata.distance(self.loc)

        return self.geodata.sort_values('distance_to_us', ascending=True).groupby('applicant').head(count)



if __name__ == '__main__':
        ft = FoodTrucks()
        print(ft.suggest())

