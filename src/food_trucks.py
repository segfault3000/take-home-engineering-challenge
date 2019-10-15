import arrow
import requests
import geocoder
import geopandas

import pandas as pd
import shapely.geometry as geom
from tabulate import tabulate


class FoodTrucks:
    """FoodTrucks provides access to a list of San Francisco trucks near a location.

    It wraps access to the San Francisco government food truck permit api and adds some
    geospatial search to provide a list of possible food trucks near a location.
    """
    DEFAULT_SOURCE_URL = 'https://data.sfgov.org/api/geospatial/rqzj-sfat?method=export&format=GeoJSON'  # "Live" GeoJSON food truck locations

    def __init__(self, source: str = None) -> None:
        """Initialize a new FoodTruck lookup.

        Parameters
        ----------
        source : str
            an alternative url or path for food truck geojson.
            this is intended to be used only for testing as any live instance
            will need current data.
        """
        self.src_url = source or self.DEFAULT_SOURCE_URL
        self.update()

    def update(self) -> None:
        """Update the geojson based dataset held by this object.

        If the object is cached or long-lived then this will need to be periodically run to
        ensure current data is available when providing suggestions.
        """
        self.geodata = geopandas.read_file(self.src_url)
        self.updated_at = arrow.get()
        self.geodata['expirationdate'] = pd.to_datetime(self.geodata['expirationdate'])

        # the food truck data includes expired or pending permits
        # so we must filter it or we will provide innacurate results.
        self.geodata = self.geodata.query('not x.isnull() &'
                                          'not expirationdate.isnull() &'
                                          'facilitytype == "Truck" &'
                                          'status == "APPROVED" &'
                                          f'expirationdate > "{self.updated_at:YYYY-MMM-DD}"')

    def suggest(self, location: str = None, count: int = 20) -> pd.DataFrame:
        """Get a list of possible food truck locations near your location.

        Parameters
        ----------
        locations : str
            Optional explicit location to geocode. By default this call will attempt
            to provide a location by IP address which can be *very* inaccurate.
        count : int
            Defaults to 20 rows in the resulting `DataFrame`. Expected to be >0.

        Returns
        -------
        pd.DataFrame
            a geopandas dataframe containing the nearest subset of food trucks from the
            permit dataset.
            None if there are no possible results
        """
        if count is None or count < 0:
            return None

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
        print(tabulate(ft.suggest()))

