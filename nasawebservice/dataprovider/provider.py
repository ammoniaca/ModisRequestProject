import requests
from nasawebservice.parameters import *
from nasawebservice.utils import *
from typing import Iterator
import gc

# Asynchronous
from aiohttp import ClientSession, ClientConnectorError, ClientResponseError, ClientPayloadError, InvalidURL
from nasawebservice.utils import aiohttp_handler_exception
import asyncio
import platform
# Avoid RuntimeError: Event loop is closed in Windows
if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class NasaWebServiceAPIProvider:
    """The NasaWebServiceAPIProvider provides several methods for users to interact with the MODIS/VIIRS
    Land Products Web Service through standards based REST (Representational State Transfer) web service API.

        via https://modis.ornl.gov/data/modis_webservice.html \n

        The Open API documentation page for the web service can be accessed from:

        via https://modis.ornl.gov/rst/ui/

    Attributes
    ----------
    base_url : str
        URL base for the MODIS/VIIRS Land Products Web Service (i.e., https://modis.ornl.gov).

    Methods
    -------
    products(sensor=Sensors.ALL, tool=Tools.ALL) -> dict
        Returns the list of products available.

    bands(product) -> dict
        Returns the list of bands available for a product.

    dates(product, latitude, longitude) -> dict
        Returns a list of composite dates available for the product, latitude, longitude combination.

    subset(product, latitude, longitude, band, start_date, end_date, km_above_below, km_left_right) -> dict
        Returns the subset for the location, product, band and date combination with
        a maximum 10 modis dates per request limit.

    execute_many(product, latitude, longitude, band, start_date, end_date, km_above_below, km_left_right)
     -> Iterator[dict]
        Returns a generator object of the subset for the location, product, band and date combination without
        the limit of a maximum 10 modis dates per request in subset API call.

    execute_all(product, latitude, longitude, band, km_above_below, km_left_right) -> Iterator[dict]
        Returns a generator object of the set for the location, product and band combination for all available dates.

    last_product(product, latitude, longitude, band, km_above_below, km_left_right) -> dict
        Returns data of the last date for the product, location, and band combination.

    is_present(product, latitude, longitude, reference_date) -> bool
        Check if a given product, latitude, longitude combination is present according to the reference date.

    get_requests_http_time() -> str
        Returns the HTTP header time format from the last valid request.

    get_requests_url() -> str
        Returns the URL from the last valid request.

    available_products_by_date(latitude, longitude, reference_date) -> dict
        Returns all available and not available products for a given date, latitude, longitude combination.

    async_execute_many(product, latitude, longitude, band, km_above_below, km_left_right)
    -> Iterator[dict]:
        Returns an iterator for the location, product and band combination for all available dates. An asynchronous
        approach for multithreading the API call.

    async_execute_all(product, latitude, longitude, band, km_above_below, km_left_right)
    -> Iterator[dict]:
        This returns a iterator for the location, product and band combination for combination without
        the limit of a maximum 10 modis dates per request in subset API call. An asynchronous approach for
        multithreading the API call.

    Notes
    -----
    .. [1] The current API REST (Representational State Transfer) version is v1.

    .. [2] ORNL DAAC. 2018. MODIS and VIIRS Land Product Subsets RESTful Web Service. ORNL DAAC,
            Oak Ridge, Tennessee, USA. https://doi.org/10.3334/ORNLDAAC/1600.

    """

    def __init__(self, base_url: str, version: int = 1):
        self._DATES_SLOT: str = 'dates'
        self._MODIS_DATE: str = 'modis_date'
        self._PRODUCTS: str = 'products'
        self._MAXIMUM_CONCURRENT_NUMBER: int = 10
        self._base_url: str = base_url
        self._current_version: float = version
        self._url_path: str = ''.join(['rst/api/v', str(self._current_version)])
        self._url: str = '/'.join([self._base_url, self._url_path])
        self._requests_time: str = ''
        self._requests_url: str = ''
        self._session: requests.sessions.Session = requests.Session()

    @property
    def base_url(
        self
    ) -> str:
        """Get base url of MODIS/VIIRS Land Products Web Service.

        Returns
        -------
        base_url: str

        """
        return self._url

    @property
    def version(
        self
    ) -> float:
        """This returns the REST API current version.

        Returns
        -------
        float
            current version

        """
        return self._current_version

    @property
    def maximum_concurrent_number(
        self
    ) -> int:
        """This returns the maximum number of concurrent requests. The NASA web service policy states that cannot
        process more than 10 concurrent requests from the same host.

        Returns
        -------
        int
            Maximum number of concurrent requests.

        """
        return self._MAXIMUM_CONCURRENT_NUMBER

    @maximum_concurrent_number.setter
    def maximum_concurrent_number(
        self,
        concurrent_number: int
    ) -> None:
        """Set the maximum number of concurrent requests

        Parameters
        ----------
        concurrent_number: int
            Maximum number of concurrent requests

        Raises
        ------
        ValueError
            If the maximum number of concurrent for host exceeds 10, the service
            cannot process more than 10 concurrent requests from the same host.

        """
        if concurrent_number > 10:
            raise ValueError(f'the maximum number of concurrent cannot be {concurrent_number}, since the API service '
                             f'cannot process more than 10 concurrent requests from the same host.')
        self._MAXIMUM_CONCURRENT_NUMBER = concurrent_number

    @staticmethod
    def _response_fault_handling(
        response: requests.models.Response
    ) -> dict:
        """Exception response for the Python requests module intercepted by response.raise_for_status()

        Parameters
        ----------
        response: requests.models.Response

        Returns
        -------
            error_response: dict


        """
        error_response = {'status': response.status_code, 'title': response.reason, 'url': response.url}
        if isinstance(response.json(), dict):
            error_response.update({'detail': response.json().get('detail')})
        elif isinstance(response.json(), str):
            error_response.update({'detail': response.text.rstrip("\n").replace('"', '')})
        else:
            error_response.update({'detail': 'something wrong'})
        return error_response

    @staticmethod
    def _error_fault_handling(
        error_obj,
        status_code: int,
        title: str
    ) -> dict:
        """Exception response for the Python requests module

        Parameters
        ----------
        error_obj: requests exceptions

        status_code: int
            Hypertext Transfer Protocol (HTTP) response status code. The code is 777 if a
            valid HTTP status code could not be deduced.
        title: str
            title of the cause of error

        Returns
        -------
        error_response: dict
            error response

            {
                'status': 'Integer',
                'title': 'String',
                'url': 'String',
                'detail': 'String'
            }

        """
        base_url = error_obj.request.url
        error_response = {'status': status_code,
                          'title': title,
                          'url': base_url,
                          'detail': f'Exception for {base_url}'}
        return error_response

    def _response(
        self,
        query: str
    ) -> dict:
        """Request to MODIS/VIIRS Land Products Web Service and Exception handling of the Python requests module.

            via https://stackoverflow.com/questions/16511337/correct-way-to-try-except-using-python-requests-module

        Parameters
        ----------
        query: str
            Query string for MODIS/VIIRS Land Products Web Service

        Returns
        -------
        response_result: dict

        """
        self._requests_time: str = ''
        self._requests_url: str = ''
        try:
            response = self._session.get(query)
            self._requests_time: str = response.headers.get('Date')
            self._requests_url: str = response.url
            if response.ok:
                response_result = response.json()
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            # An HTTP error (4xx) occurred.
            if errh.response is None:
                response_result = self._error_fault_handling(error_obj=errh, status_code=400, title='HTTP ERROR')
            else:
                response_result = self._response_fault_handling(response=errh.response)
        except requests.exceptions.ConnectionError as errc:
            # A Connection error occurred.
            response_result = self._error_fault_handling(error_obj=errc, status_code=777, title='CONNECTION ERROR')
        except requests.exceptions.Timeout as errt:
            # The request timed out. Catching this error will catch both: ConnectTimeout, ReadTimeout
            response_result = self._error_fault_handling(error_obj=errt, status_code=777, title='TIMEOUT ERROR')
        except requests.exceptions.RequestException as err:
            # Ambiguous exception
            response_result = self._error_fault_handling(error_obj=err, status_code=777, title='AMBIGUOUS ERROR')
        finally:
            self._session.close()
        return response_result

    def get_request_http_time(
        self
    ) -> str:
        """This returns the HTTP header time format from the last valid request.

        Returns
        -------
        str
            The HTTP headers use a particular format, involving abbreviated English names of the days of the week
            and the months, a comma (after the first of these), day before month before year,
            24-hour:minute:second, and GMT (Greenwich Mean Time). Examples: Thu, 01 Dec 1994 16:00:00 GMT,
            Thu, 26 Jan 2006 15:01:16 GMT.

        Examples
        --------
        >>> provider = NasaWebServiceAPIProvider(base_url='https://modis.ornl.gov')
        # get the list of all available bands for the product MOD13Q1
        >>> mod13q1 = provider.bands(product=Products.MOD13Q1)
        # get HTTP header time format of the last valid request
        >>> print(provider.get_request_http_time())
        Mon, 21 Mar 2022 10:06:49 GMT

        Raises
        ------
        NameError
            If the HTML header time is not found (for example,
            because no previous valid request has been made) a NameError is raised.

        Notes
        -----
        .. [1] Useful Python time formats for dealing with HTTP headers.
        https://dpb.bitbucket.io/useful-python-time-formats-for-dealing-with-http-headers.html

        """
        if self._requests_time == '':
            raise NameError('The HTML header time is not found. Try to make a valid request first.')
        return self._requests_time

    def get_request_url(
        self
    ) -> str:
        """This returns the URL (Uniform Resource Locator) from the last valid request.

        Returns
        -------
        str
            The encoded URL from the last valid request.

        Examples
        --------
        >>> provider = NasaWebServiceAPIProvider(base_url='https://modis.ornl.gov')
        # get the list of all available bands for the product MOD13Q1
        >>> mod13q1 = provider.bands(product=Products.MOD13Q1)
        # get URL of the last valid request
        >>> print(provider.get_request_url())
        https://modis.ornl.gov/rst/api/v1/MOD13Q1/bands

        Raises
        ------
        NameError
            If the URL is not found (for example,
            because no previous valid request has been made) a NameError is raised.

        """
        if self._requests_url == '':
            raise NameError('The URL is not found. Try to make a valid request first.')
        return self._requests_url

    def products(
        self,
        sensor: Sensors = Sensors.ALL,
        tool: Tools = Tools.ALL
    ) -> dict:
        """This returns the list of products available.

            via  https://modis.ornl.gov/rst/ui/#!/products/get_products

        Parameters
        ----------
        sensor : Sensors class, optional
            NASA sensor type. Available sensors: MODIS-Terra, MODIS-Aqua, MODIS-TerraAqua, VIIRS-SNPP, Daymet, SMAP,
            ECOSTRESS, SIFESDR. Default: all sensors (i.e., Sensors.ALL).
        tool : Tools class, optional
            Only display products available for the specified tool. Available tools: FixedSite, GlobalSubset.
            Default: all tools (i.e., Tools.ALL).

        Returns
        -------
        response_result: dict
            List of products available, an error content otherwise.

            if HTTP Status Code is 200:

                [
                    {
                        'description': 'String',
                        'frequency': 'String',
                        'product': 'String',
                        'resolution_meters': 'Integer'
                    }
                ]

            if HTTP Status Code is not 200:

                [
                    {
                        'status': 'Integer'
                        'title': 'String',
                        'detail': 'String'
                    }
                ]

        Examples
        --------
        >>> from nasawebservice import *
        >>> provider = NasaWebServiceAPIProvider(base_url='https://modis.ornl.gov')
        # get the list of all products available for MODIS-Terra
        >>> terra = provider.products(sensor=Sensors.MODIS_TERRA)
        # get the list of all products available for MODIS-Aqua
        >>> aqua = provider.products(sensor=Sensors.MODIS_AQUA)
        # get the list of all products available for MODIS-Terra+Aqua
        >>> aqua = provider.products(sensor=Sensors.MODIS_TERRA_AQUA)

        Notes
        -----
        .. [1] The Daily Surface Weather Data (Daymet) is available ONLY for North America.

        """
        request_url = f'{self._url}/products?sensor={str(sensor)}&tool={str(tool)}'
        response_result = self._response(query=request_url)
        return response_result

    def bands(
        self,
        product: Products
    ) -> dict:
        """This returns the list of bands available for a product.

            via  https://modis.ornl.gov/rst/ui/#!/bands/get_bands

        Parameters
        ----------
        product: Products class
            Short name of the product, from the NASA specified sensor, to query.

        Returns
        -------
        response_result: dict
            List of bands available for a product, an error content otherwise.

            if HTTP Status Code is 200::

                [
                    {
                        'add_offset': 'String',
                        'band': 'String',
                        'description': 'String',
                        'fill_value': 'String',
                        'scale_factor': 'String',
                        'units': 'String',
                        'valid_range': 'String'
                    }
                ]

            if HTTP Status Code is not 200::

                [
                    {
                        'status': 'Integer'
                        'title': 'String',
                        'detail': 'String'
                    }
                ]

        Examples
        --------
        >>> from nasawebservice import *
        >>> provider = NasaWebServiceAPIProvider(base_url='https://modis.ornl.gov')
        # get the list of all available bands for the product MOD13Q1
        >>> mod13q1 = provider.bands(product=Products.MOD13Q1)

        """
        request_url = f'{self._url}/{str(product)}/bands'
        response_result = self._response(query=request_url)
        return response_result

    def dates(
        self,
        product: Products,
        latitude: float,
        longitude: float
    ) -> dict:
        """This returns the list of composite dates available for the product, latitude, longitude combination.

            via https://modis.ornl.gov/rst/ui/#!/dates/get_dates

        Parameters
        ----------
        product : Products class
            Short name of the product, from the NASA specified sensor, to query.
        latitude : float
            Latitude in decimal degrees in geographic Lat/Long WGS 84 coordinate system.
        longitude : float
            Longitude in decimal degrees in geographic Lat/Long WGS 84 coordinate system.

        Returns
        -------
        response_result: dict
            List of composite dates available, in calendar_date (YYYY-MM-DD) and in modis_date (AYYYYDDD),
            for the product, Latitude, Longitude combination, otherwise an error content.

            if HTTP Status Code is 200::

                [
                    {
                        'calendar_date': 'String',
                        'modis_date': 'String'
                    }
                ]

            if HTTP Status Code is not 200::

                [
                    {
                        'status': 'Integer'
                        'title': 'String',
                        'detail': 'String'
                    }
                ]

        Examples
        --------
        >>> from nasawebservice import *
        >>> provider = NasaWebServiceAPIProvider(base_url='https://modis.ornl.gov')
        # get the list of all available dates for the product MOD13Q1 by a given location
        >>> mod13q1_dates = provider.dates(product=Products.MOD13Q1, latitude=41.84936, longitude=13.58814)

        """
        query = f'{self._url}/{str(product)}/dates?latitude={latitude}&longitude={longitude}'
        response_result = self._response(query=query)
        return response_result

    def subset(
        self,
        product: Products,
        latitude: float,
        longitude: float,
        band: Bands,
        start_date: str,
        end_date: str,
        km_above_below: int,
        km_left_right: int
    ) -> dict:
        """This returns the subset for the location, product, band and date combination.
        There is a limit of a maximum 10 modis dates per request.

            via https://modis.ornl.gov/rst/ui/#!/subset/get_subset

        Parameters
        ----------
        product: Products class
            Short name of the product, from the NASA specified sensor, to query.
        latitude: float
            Latitude in decimal degrees in geographic Lat/Long WGS 84 coordinate system.
        longitude: float
            Longitude in decimal degrees in geographic Lat/Long WGS 84 coordinate system.
        band: Bands Class
            Name of data layer. If 'ALL' is selected (i.e., Band.PRODUCT-TYPE.ALL) all bands are extracted.
        start_date: str
            Composite date (i.e., AYYYYDDD, e.g., A2022023) start of the subset period, where DDD is in Day-Of-Year
            calendar (DOY) format.
        end_date: str
            Composite date (i.e., AYYYYDDD, e.g., A2022034) end of the subset period, where DDD is in Day-Of-Year
            calendar (DOY) format.
        km_above_below: int
            Size in km of the subset above and below the center location. The value must be less than or equal to
            100 (0 &lt= km_above_below &lt= 100).
        km_left_right: int
            Size in km of the subset left and right of the center location. The value must be less than or equal to
            100 (0 &lt= km_left_right &lt= 100).

        Returns
        -------
        response_results: dict
            This returns the subset for the location, product, band and date combination.

            if HTTP Status Code is 200 for ONLY ONE BAND:

                {
                    'xllcorner': 'String',
                    'yllcorner': 'String'
                    'cellsize': 'Double',
                    'nrows': 'Integer',
                    'ncols': 'Integer',
                    'band': 'String',
                    'units': 'String',
                    'scale': 'Double',
                    'latitude': 'Double',
                    'longitude': 'Double',
                    'header': 'String',
                    'subset':
                    [
                        {
                            'modis_date': 'string',
                            'calendar_date': 'String',
                            'band': 'String',
                            'tile': 'string'
                            'proc_date': 'string',
                            'data': 'ListInteger',
                        }
                    ],
                }

            if HTTP Status Code is 200 for ALL BANDS:

                {
                    'xllcorner': 'String',
                    'yllcorner': 'String',
                    'cellsize': 'Double',
                    'nrows': 'Integer',
                    'ncols': 'Integer',
                    'band': 'String',
                    'latitude': 'Double',
                    'longitude': 'Double',
                    'header': 'String',
                    'subset':
                        [
                            {
                                'modis_date': 'String',
                                'calendar_date': 'String',
                                'band': 'String',
                                'tile': 'String',
                                'proc_date': 'String',
                                'data': 'ListInteger'
                            },
                        ]
                }

            if HTTP Status Code is not 200 for ONLY ONE BAND and for ALL BANDS:

                [
                    {
                        'status': 'Integer'
                        'title': 'String',
                        'detail': 'String'
                    }
                ]

        Examples
        --------
        >>> from nasawebservice import *
        >>> provider = NasaWebServiceAPIProvider(base_url='https://modis.ornl.gov')
        # get NDVI band for MOD13Q1 subset by a given time interval and location
        >>> mod13q1_ndvi = provider.subset(product=Products.MOD13Q1, latitude=41.84936, longitude=13.58814,
        ...    band=Bands.MOD13Q1.NDVI, start_date='A2000001', end_date='A2000200', km_above_below=1, km_left_right=1)
        # get ALL bands for MOD13Q1 subset by a given time interval and location
        >>> mod13q1_all = provider.subset(product=Products.MOD13Q1, latitude=41.84936, longitude=13.58814,
        ...    band=Bands.MOD13Q1.ALL, start_date='A2000001', end_date='A2000200', km_above_below=1, km_left_right=1)

        Notes
        -----
        .. [1] If km_above_below=0 and km_left_right=0, returns the single pixel value.

        """
        request_url = f'{self._url}/{str(product)}/subset?latitude={latitude}&longitude={longitude}&band={str(band)}' \
                      f'&startDate={start_date}&endDate={end_date}' \
                      f'&kmAboveBelow={km_above_below}&kmLeftRight={km_left_right}'
        response_result = self._response(query=request_url)
        return response_result

    def execute_many(
        self,
        product: Products,
        latitude: float,
        longitude: float,
        band: Bands,
        start_date: str,
        end_date: str,
        km_above_below: int,
        km_left_right: int
    ) -> Iterator[dict]:
        """This returns a generator object of the subset for the location, product, band and date
        combination without the limit of a maximum 10 modis dates per request in subset API call.

        Parameters
        ----------
        product: Products object
            Short name of the product, from the NASA specified sensor, to query.
        latitude: float
            Latitude in decimal degrees in geographic Lat/Long WGS 84 coordinate system.
        longitude: float
            Longitude in decimal degrees in geographic Lat/Long WGS 84 coordinate system.
        band: Bands object
            Name of data layer. If 'ALL' is selected (i.e., Band.PRODUCT-TYPE.ALL) all bands are extracted.
        start_date: str
            Composite date (i.e., AYYYYDDD, e.g., A2022023) start of the subset period, where DDD is in Day-Of-Year
            calendar (DOY) format. If there is not an acquisition for the start date, the algorithm finds the nearest
            acquisition start date.
        end_date: str
            Composite date (i.e., AYYYYDDD, e.g., A2022034) end of the subset period, where DDD is in Day-Of-Year
            calendar (DOY) format. If there is no acquisition for the end date, the algorithm finds the nearest
            acquisition end date.
        km_above_below: int
            Size in km of the subset above and below the center location. The value must be less than or equal to
            100 (0 &lt= km_above_below &lt= 100).
        km_left_right: int
            Size in km of the subset left and right of the center location. The value must be less than or equal to
            100 (0 &lt= km_left_right &lt= 100).

        Yields
        ------
        dict
            This returns the subset for the location, product, band and date combination without the limit of
            a maximum 10 modis dates per request in subset API call.
        dict
            Error message as dictornary.

        Examples
        --------
        >>> from nasawebservice import *
        >>> provider = NasaWebServiceAPIProvider(base_url='https://modis.ornl.gov')
        # get NDVI band of product MOD13Q1 by a given time interval and location
        >>> for item_ndvi in provider.execute_many(product=Products.MOD13Q1, latitude=41.84936, longitude=13.58814,
        ...                                              band=Bands.MOD13Q1.NDVI,
        ...                                              start_date='A2000001', end_date='A2000300',
        ...                                              km_above_below=1, km_left_right=1):
        >>>     print(item_ndvi)
        # get ALL bands of product MOD13Q1 by a given time interval and location
        >>> for item_all in provider.execute_many(product=Products.MOD13Q1, latitude=41.84936, longitude=13.58814,
        ...                                              band=Bands.MOD13Q1.ALL,
        ...                                              start_date='A2000001', end_date='A2000300',
        ...                                              km_above_below=1, km_left_right=1):
        >>>     print(item_all)

        Notes
        -----
        .. [1] If km_above_below=0 and km_left_right=0, returns the single pixel value.

        Raises
        ------
        ValueError
            If 'start date' >= 'end date' an ValueError is raised, because the function receives an argument
            of the correct type but an inappropriate value.

        """
        all_dates: dict = self.dates(product=product, latitude=latitude, longitude=longitude)
        if 'status' not in all_dates:
            time_dates: list[dict] = sorted(all_dates.get(self._DATES_SLOT), key=lambda x: x.get(self._MODIS_DATE))
            time_dates: list[str] = [d.get(self._MODIS_DATE) for d in time_dates]
            for time_date in compute_date_interval(all_dates=time_dates, start_date=start_date, end_date=end_date):
                yield self.subset(product=product,
                                  latitude=latitude,
                                  longitude=longitude,
                                  band=band,
                                  start_date=time_date,
                                  end_date=time_date,
                                  km_above_below=km_above_below,
                                  km_left_right=km_left_right)
        else:
            yield all_dates

    def execute_all(
        self,
        product: Products,
        latitude: float,
        longitude: float,
        band: Bands,
        km_above_below: int,
        km_left_right: int
    ) -> Iterator[dict]:
        """This returns a generator object of the set for the location, product and band combination
        for all available dates (i.e., from the first to the last available product date).

        Parameters
        ----------
        product: Products object
            Short name of the product, from the NASA specified sensor, to query.
        latitude: float
            Latitude in decimal degrees in geographic Lat/Long WGS 84 coordinate system.
        longitude: float
            Longitude in decimal degrees in geographic Lat/Long WGS 84 coordinate system.
        band: Bands object
            Name of data layer. If 'ALL' is selected (i.e., Band.PRODUCT-TYPE.ALL) all bands are extracted.
        km_above_below: int
            Size in km of the subset above and below the center location. The value must be less than or equal to
            100 (0 &lt= km_above_below &lt= 100).
        km_left_right: int
            Size in km of the subset left and right of the center location. The value must be less than or equal to
            100 (0 &lt= km_left_right &lt= 100).

        Yields
        ------
        dict
            Data for the location, product, band and date combination for all available dates.
        dict
            Error message as dictornary.

        Examples
        --------
        >>> from nasawebservice import *
        >>> provider = NasaWebServiceAPIProvider(base_url='https://modis.ornl.gov')
        # get NDVI band by a given location for all available dates of MOD13Q1
        >>> for item_ndvi in provider.execute_all(product=Products.MOD13Q1, latitude=41.84936, longitude=13.58814,
        ...                                           band=Bands.MOD13Q1.NDVI, km_above_below=1, km_left_right=1):
        >>>     print(item_ndvi)
        # get ALL bands by a given location for all available dates of MOD13Q1
        >>> for item_all in provider.execute_all(product=Products.MOD13Q1, latitude=41.84936, longitude=13.58814,
        ...                                          band=Bands.MOD13Q1.ALL, km_above_below=1, km_left_right=1):
        >>>     print(item_all)

        Notes
        -----
        .. [1] If km_above_below=0 and km_left_right=0, returns the single pixel value.

        """
        dates_intervals = self.dates(product=product, latitude=latitude, longitude=longitude)
        if 'status' not in dates_intervals:
            time_dates = (d[self._MODIS_DATE] for d in dates_intervals.get(self._DATES_SLOT))
            for time_date in time_dates:
                yield self.subset(product=product,
                                  latitude=latitude,
                                  longitude=longitude,
                                  band=band,
                                  start_date=time_date,
                                  end_date=time_date,
                                  km_above_below=km_above_below,
                                  km_left_right=km_left_right)
        else:
            yield dates_intervals

    def last_product(
        self,
        product: Products,
        latitude: float,
        longitude: float,
        band: Bands,
        km_above_below: int,
        km_left_right: int
    ) -> dict:
        """This returns the data of the last acquisition for the product, location, and band combination.

        Parameters
        ----------
        product: Products object
            Short name of the product, from the NASA specified sensor, to query.
        latitude: float
            Latitude in decimal degrees in geographic Lat/Long WGS 84 coordinate system.
        longitude: float
            Longitude in decimal degrees in geographic Lat/Long WGS 84 coordinate system.
        band: Bands object
            Name of data layer. If 'ALL' is selected (i.e., Band.PRODUCT-TYPE.ALL) all bands are extracted.
        km_above_below: int
            Size in km of the subset above and below the center location. The value must be less than or equal to
            100 (0 &lt= km_above_below &lt= 100).
        km_left_right: int
            Size in km of the subset left and right of the center location. The value must be less than or equal to
            100 (0 &lt= km_left_right &lt= 100).

        Returns
        -------
        dict
            This returns the data of the last date for the product, location, and band combination.

            if HTTP Status Code is 200 for ONLY ONE BAND::

                {
                    'xllcorner': 'String',
                    'yllcorner': 'String'
                    'cellsize': 'Double',
                    'nrows': 'Integer',
                    'ncols': 'Integer',
                    'band': 'String',
                    'units': 'String',
                    'scale': 'Double',
                    'latitude': 'Double',
                    'longitude': 'Double',
                    'header': 'String',
                    'subset':
                    [
                        {
                            'modis_date': 'string',
                            'calendar_date': 'String',
                            'band': 'String',
                            'tile': 'string'
                            'proc_date': 'string',
                            'data': 'ListInteger',
                        }
                    ],
                }

            if HTTP Status Code is 200 for ALL BANDS::

                {
                    'xllcorner': 'String',
                    'yllcorner': 'String',
                    'cellsize': 'Double',
                    'nrows': 'Integer',
                    'ncols': 'Integer',
                    'band': 'String',
                    'latitude': 'Double',
                    'longitude': 'Double',
                    'header': 'String',
                    'subset':
                        [
                            {
                                'modis_date': 'String',
                                'calendar_date': 'String',
                                'band': 'String',
                                'tile': 'String',
                                'proc_date': 'String',
                                'data': 'ListInteger'
                            },
                        ]
                }

            if HTTP Status Code is not 200 for ONLY ONE BAND and for ALL BANDS::

                [
                    {
                        'status': 'Integer'
                        'title': 'String',
                        'detail': 'String'
                    }
                ]

        Examples
        --------
        >>> from nasawebservice import *
        >>> provider = NasaWebServiceAPIProvider(base_url='https://modis.ornl.gov')
        # get the last NDVI band of MOD13Q1 by a given location
        >>> last_mod13q1_ndvi = provider.last_product(product=Products.MOD13Q1, latitude=41.84936, longitude=13.58814,
        ...                                       band=Bands.MOD13Q1.NDVI, km_above_below=1, km_left_right=1)
        # get the last ALL bands of MOD13Q1 by a given location
        >>> last_mod13q1_all = provider.last_product(product=Products.MOD13Q1, latitude=41.84936, longitude=13.58814,
        ...                                      band=Bands.MOD13Q1.ALL, km_above_below=1, km_left_right=1)

        Notes
        -----
        .. [1] If km_above_below=0 and km_left_right=0, returns the single pixel value.

        """
        all_dates_intervals = self.dates(product=product, latitude=latitude, longitude=longitude)
        if 'status' in all_dates_intervals:
            return all_dates_intervals
        last_dates: str = max([d[self._MODIS_DATE] for d in all_dates_intervals.get(self._DATES_SLOT)])
        return self.subset(
            product=product,
            latitude=latitude,
            longitude=longitude,
            band=band,
            start_date=last_dates,
            end_date=last_dates,
            km_above_below=km_above_below,
            km_left_right=km_left_right
        )

    def is_present(
        self,
        product: Products,
        latitude: float,
        longitude: float,
        reference_date: str
    ) -> bool:
        """Check if a given product, latitude, longitude combination is present according to the reference date.

        Parameters
        ----------
        product: Products object
            Short name of the product, from the NASA specified sensor, to query.
        latitude: float
            Latitude in decimal degrees in geographic Lat/Long WGS 84 coordinate system.
        longitude: float
            Longitude in decimal degrees in geographic Lat/Long WGS 84 coordinate system.
        reference_date: str
            Composite date (i.e., AYYYYDDD, e.g., A2022023) to check, where DDD is in Day-Of-Year calendar (DOY) format.

        Returns
        -------
        bool
            Returns true if a product is present at the reference date, otherwise it returns false.

        Examples
        --------
        >>> from nasawebservice import *
        >>> provider = NasaWebServiceAPIProvider(base_url='https://modis.ornl.gov')
        >>> flag_true = provider.is_present(product=Products.MOD13Q1, latitude=41.84936, longitude=13.58814,
        ...                                 reference_date='A2000049')
        >>> print(flag_true)
        True
        >>> flag_false = provider.is_present(product=Products.MOD13Q1, latitude=41.84936, longitude=13.58814,
        ...                                  reference_date='A2000050')
        >>> print(flag_false)
        False

        Raises
        ------
        requests.exceptions.RequestException
            If the call to API dates fails an exception is raised.

        """
        flag = True
        interval_dates = self.dates(product=product, latitude=latitude, longitude=longitude)
        if 'status' in interval_dates:
            raise requests.exceptions.RequestException(interval_dates.get('detail'))
        time_dates: list = [d.get(self._MODIS_DATE) for d in interval_dates.get(self._DATES_SLOT)]
        if reference_date not in time_dates:
            flag = False
        return flag

    def available_products_by_date(
        self,
        latitude: float,
        longitude: float,
        reference_date: str
    ) -> dict:
        """This returns all available and not available products for a given date, latitude, longitude combination.

        Parameters
        ----------
        latitude: float
            Latitude in decimal degrees in geographic Lat/Long WGS 84 coordinate system.

        longitude: float
            Longitude in decimal degrees in geographic Lat/Long WGS 84 coordinate system.

        reference_date: str
            Composite date (i.e., AYYYYDDD, e.g., A2022023) to check, where DDD is in Day-Of-Year calendar (DOY) format.

        Returns
        -------
        dict
            This returns all available and not available products for a given date, latitude, longitude combination.

            {
                'date': 'String'
                'available':
                    [
                        {
                            'product': 'String',
                            'description': 'String',
                            'frequency': 'String',
                            'resolution_meters': 'Integer'
                        }
                    ]
                'not_available':
                    [
                        {
                            'product': 'String',
                            'description': 'String',
                            'frequency': 'String',
                            'resolution_meters': 'Integer',
                            'status': 'Integer',
                            'title': 'String',
                            'url': 'String',
                            'detail' 'String'
                        }
                    ]
            }

            Otherwise

            {
                'status': 'Integer',
                'title': 'String',
                'url': 'String',
                'detail' 'String'
            }

        Examples
        --------
        >>> from nasawebservice import *
        >>> provider = NasaWebServiceAPIProvider(base_url='https://modis.ornl.gov')
        >>> report_prod = provider.available_products_by_date(latitude=41.84936,
        ...                                 longitude=13.58814, reference_date='A2021001')

        Notes
        -----
        .. [1] If status code = 777, means that the product is available for latitude and longitude location
        but is not available for that specific date.

        """
        all_products = set([str(product) for product in Products])
        product_report: dict = {'date': reference_date,
                                'available': [],
                                'not_available': []}
        products: dict = self.products(sensor=Sensors.ALL, tool=Tools.ALL)
        if 'status' in products:
            return products
        products_lst: list[dict] = products.get('products')
        for product in products_lst:
            product_code: str = product.get('product').upper()  # upper for Daytime -> DAYMATE
            if product_code in all_products:
                product_date: dict = self.dates(product=getattr(Products, product.get('product').upper()),
                                                latitude=latitude, longitude=longitude)
                if 'status' not in product_date:
                    product_date: list[str] = [d.get(self._MODIS_DATE) for d in product_date.get(self._DATES_SLOT)]
                    if reference_date in product_date:
                        product_report.get('available').append(product)
                    else:
                        add_dict = {'status': 777,
                                    'title': 'NO DATA AVAILABLE',
                                    'url': self._requests_url,
                                    'detail': f'No data available for day {reference_date} '
                                              f'for {product_code} {latitude} {longitude} combination.'
                                    }
                        product.update(add_dict)
                        product_report.get('not_available').append(product)
                else:
                    up_dict: dict = {**product, **product_date}
                    product_report.get('not_available').append(up_dict)
            return product_report

    @staticmethod
    def _asynchronous_exception_handling(
        error_obj,
        request_url: str,
        status_code: int,
        title: str
    ) -> dict:
        """Exception response for the Python requests module

        Parameters
        ----------
        error_obj: requests exceptions object

        status_code: int
            Hypertext Transfer Protocol (HTTP) response status code. The code is 777 if a
            valid HTTP status code could not be deduced cause an Exception is raised.
        title: str
            title of the cause of error

        Returns
        -------
        error_response: dict
            error response

            {
                'status': 'Integer',
                'title': 'String',
                'url': 'String',
                'detail': 'String'
            }

        """
        error_response = {'status': status_code,
                          'title': title,
                          'url': request_url,
                          'detail': str(error_obj)}
        return error_response

    async def _asynchronous_response(
        self,
        session,
        request_url: str
    ) -> dict:
        """Get response from request using an aiohttp ClientSession. Its needed for working with async method.

        Parameters
        ----------
        session: aiohttp.client.ClientSession object
            HTTP Session open in "async with ClientSession() as session"
        request_url: str
            Request URL (Uniform Resource Locator).

        Returns
        -------
        dict

        """
        self._requests_time: str = ''
        self._requests_url: str = ''
        try:
            async with session.get(request_url) as response:
                if response.ok:
                    self._requests_time: str = response.headers.get('Date')
                    self._requests_url: str = str(response.url)
                    response_result = await response.json()
                else:
                    detail: str = aiohttp_handler_exception(status_code=response.status)
                    response_result = {
                        'status': response.status,
                        'title': response.reason,
                        'url': str(response.url),
                        'detail': detail
                    }
        except ClientConnectorError as ecc:
            error_tile = 'CLIENT CONNECTION ERROR'
            response_result = self._asynchronous_exception_handling(error_obj=ecc, request_url=request_url,
                                                                    status_code=777, title=error_tile)
        except ClientResponseError as ecr:
            error_tile = 'CLIENT RESPONSE ERROR'
            response_result = self._asynchronous_exception_handling(error_obj=ecr, request_url=request_url,
                                                                    status_code=777, title=error_tile)
        except ClientPayloadError as ecp:
            error_tile = 'CLIENT PAYLOAD ERROR'
            response_result = self._asynchronous_exception_handling(error_obj=ecp, request_url=request_url,
                                                                    status_code=777, title=error_tile)
        except InvalidURL as eiu:
            error_tile = 'INVALID URL ERROR'
            response_result = self._asynchronous_exception_handling(error_obj=eiu, request_url=request_url,
                                                                    status_code=777, title=error_tile)
        return response_result

    async def _asynchronous_subset(
        self,
        chunks: Iterator[list[str]],
        product: Products,
        latitude: float,
        longitude: float,
        band: Bands,
        km_above_below: int,
        km_left_right: int
    ) -> list[dict]:
        """Central Method to

        Parameters
        ----------
        chunks: Iterator of list of str
            List of list of composite date (i.e., AYYYYDDD, e.g., A2022023), where DDD is in Day-Of-Year calendar (DOY)
            format.
        product: Products object
            Short name of the product, from the NASA specified sensor, to query.
        latitude: float
            Latitude in decimal degrees in geographic Lat/Long WGS 84 coordinate system.
        longitude: float
            Longitude in decimal degrees in geographic Lat/Long WGS 84 coordinate system.
        band: Bands object
            Name of data layer. If 'ALL' is selected (i.e., Band.PRODUCT-TYPE.ALL) all bands are extracted.
        km_above_below: int
            Size in km of the subset above and below the center location. The value must be less than or equal to
            100 (0 &lt= km_above_below &lt= 100).
        km_left_right: int
            Size in km of the subset left and right of the center location. The value must be less than or equal to
            100 (0 &lt= km_left_right &lt= 100).

        Returns
        -------

        """
        async with ClientSession() as session:
            response: list[dict] = []
            for chunk in chunks:
                tasks: list = []
                for date in chunk:
                    request_url = f'{self._url}/{str(product)}/subset?latitude={latitude}&longitude={longitude}' \
                                  f'&band={str(band)}&startDate={date}&endDate={date}' \
                                  f'&kmAboveBelow={km_above_below}&kmLeftRight={km_left_right}'
                    task = asyncio.ensure_future(
                        self._asynchronous_response(
                            session=session,
                            request_url=request_url
                        )
                    )
                    tasks.append(task)
                view_counts = await asyncio.gather(*tasks)
                response.extend(view_counts)
            return response

    async def _asynchronous_execute_all(
        self,
        product: Products,
        latitude: float,
        longitude: float,
        band: Bands,
        km_above_below: int,
        km_left_right: int
    ) -> Iterator[dict]:
        """This returns coroutine object. Indeed, when you have an asynchronous function (coroutine) in Python,
        you declare it with async def, which changes how its call behaves. In particular, calling it will immediately
        return a coroutine object, which basically says "I can run the coroutine with the arguments you called
        with and return a result when you await me".

            via https://www.aeracode.org/2018/02/19/python-async-simplified/

        Parameters
        ----------
        product: Products object
            Short name of the product, from the NASA specified sensor, to query.
        latitude: float
            Latitude in decimal degrees in geographic Lat/Long WGS 84 coordinate system.
        longitude: float
            Longitude in decimal degrees in geographic Lat/Long WGS 84 coordinate system.
        band: Band object
            Name of data layer. If 'ALL' is selected (i.e., Band.PRODUCT-TYPE.ALL) all bands are extracted.
        km_above_below: int
            Size in km of the subset above and below the center location. The value must be less than or equal to
            100 (0 &lt= km_above_below &lt= 100).
        km_left_right: int
            Size in km of the subset left and right of the center location. The value must be less than or equal to
            100 (0 &lt= km_left_right &lt= 100).

        Returns
        -------
        iterator of dict
            Data for the location, product, band and date combination for all available dates
            (i.e., from the first to the last available product date).

        """
        all_dates = self.dates(product=product, latitude=latitude, longitude=longitude)
        if 'status' not in all_dates:
            dates: list[str] = [d.get(self._MODIS_DATE) for d in all_dates.get(self._DATES_SLOT)]
            chunks: Iterator[list[str]] = (dates[i:i + self._MAXIMUM_CONCURRENT_NUMBER]
                                           for i in range(0, len(dates), self._MAXIMUM_CONCURRENT_NUMBER))
            del all_dates
            gc.collect()
            response = await self._asynchronous_subset(
                chunks=chunks,
                product=product,
                latitude=latitude,
                longitude=longitude,
                band=band,
                km_above_below=km_above_below,
                km_left_right=km_left_right
            )
            return iter(response)
        else:
            return iter([all_dates])

    def async_execute_all(
        self,
        product: Products,
        latitude: float,
        longitude: float,
        band: Bands,
        km_above_below: int,
        km_left_right: int
    ) -> Iterator[dict]:
        """This returns a iterator for the location, product and band combination for all available
        dates. (i.e., from the first to the last available product date). This method use an asynchronous
        approach for multithreading the API call.

            via https://docs.python.org/3/library/asyncio-task.html

        Parameters
        ----------
        product: Products object
            Short name of the product, from the NASA specified sensor, to query.
        latitude: float
            Latitude in decimal degrees in geographic Lat/Long WGS 84 coordinate system.
        longitude: float
            Longitude in decimal degrees in geographic Lat/Long WGS 84 coordinate system.
        band: Bands object
            Name of data layer. If 'ALL' is selected (i.e., Band.PRODUCT-TYPE.ALL) all bands are extracted.
        km_above_below: int
            Size in km of the subset above and below the center location. The value must be less than or equal to
            100 (0 &lt= km_above_below &lt= 100).
        km_left_right: int
            Size in km of the subset left and right of the center location. The value must be less than or equal to
            100 (0 &lt= km_left_right &lt= 100).

        Returns
        -------
        iterator of dict
            Data for the location, product, band and date combination for all available dates
            (i.e., from the first to the last available product date).

        Examples
        --------
        >>> import time
        >>> from nasawebservice import *
        >>> provider = NasaWebServiceAPIProvider(base_url='https://modis.ornl.gov')
        >>> start_time = time.time()
        >>> all_mod13q1 = provider.async_execute_all(product=Products.MOD13Q1,
        ...                                                 latitude=41.84936, longitude=13.58814,
        ...                                                 band=Bands.MOD13Q1.NDVI, km_above_below=0, km_left_right=0)
        >>> print("--- %s seconds ---" % (time.time() - start_time))
        >>> for index, modis in enumerate(all_mod13q1):
        ...     # check if 'modis' is not a error message
        ...     if 'status' not in modis:
        ...         print(f'{index} -> {modis}')
        ...     else:
        ...         print(f'ERROR: {modis}')

        Notes
        -----
        .. [1] If km_above_below=0 and km_left_right=0, returns the single pixel value.

        .. [2] If Maximum number of concurrent requests exceeded 10, the service cannot process more
        than 10 concurrent requests from the same host.

        .. [3] To change the maximum number of concurrent (the default value is 10) use the property setter:
        >>> provider = NasaWebServiceAPIProvider(base_url='https://modis.ornl.gov')
        >>> print(provider.maximum_concurrent_number)
        10
        >>> provider.maximum_concurrent_number = 8
        >>> print(provider.maximum_concurrent_number)
        8
        >>> provider.maximum_concurrent_number = 11
         the maximum number of concurrent cannot be 11, since the API service cannot process more than 10 concurrent
         requests from the same host.

        .. [4] Given the nature of the asynchronous multithreading approach the order of dates is not assured.

        .. [5] The asyncio.run() function to run the top-level entry point function (i.e., asynchronous_execute_all)

        """
        return asyncio.run(self._asynchronous_execute_all(
            product=product,
            latitude=latitude,
            longitude=longitude,
            band=band,
            km_above_below=km_above_below,
            km_left_right=km_left_right))

    async def _asynchronous_execute_many(
        self,
        product: Products,
        latitude: float,
        longitude: float,
        band: Bands,
        start_date: str,
        end_date: str,
        km_above_below: int,
        km_left_right: int
    ) -> Iterator[dict]:
        """

        Parameters
        ----------
        product: Products object
            Short name of the product, from the NASA specified sensor, to query.
        latitude: float
            Latitude in decimal degrees in geographic Lat/Long WGS 84 coordinate system.
        longitude: float
            Longitude in decimal degrees in geographic Lat/Long WGS 84 coordinate system.
        band: Bands object
            Name of data layer. If 'ALL' is selected (i.e., Band.PRODUCT-TYPE.ALL) all bands are extracted.
        start_date: str
            Composite date (i.e., AYYYYDDD, e.g., A2022023) start of the subset period, where DDD is in Day-Of-Year
            calendar (DOY) format.
        end_date: str
            Composite date (i.e., AYYYYDDD, e.g., A2022034) end of the subset period, where DDD is in Day-Of-Year
            calendar (DOY) format.
        km_above_below: int
            Size in km of the subset above and below the center location. The value must be less than or equal to
            100 (0 &lt= km_above_below &lt= 100).
        km_left_right: int
            Size in km of the subset left and right of the center location. The value must be less than or equal to
            100 (0 &lt= km_left_right &lt= 100).

        Returns
        -------
        Iterator

        Raises
        ------
        ValueError
            If 'start date' >= 'end date' an ValueError is raised, because the function receives an argument
            of the correct type but an inappropriate value.

        """
        all_dates = self.dates(product=product, latitude=latitude, longitude=longitude)
        if 'status' not in all_dates:
            dates: list[dict] = sorted(all_dates.get(self._DATES_SLOT), key=lambda x: x.get(self._MODIS_DATE))
            time_dates: list[str] = [d.get(self._MODIS_DATE) for d in dates]
            interval_dates: list[str] = list(compute_date_interval(
                all_dates=time_dates,
                start_date=start_date,
                end_date=end_date)
            )
            del dates
            del time_dates
            gc.collect()
            chunks: Iterator[list[str]] = (interval_dates[i:i + self._MAXIMUM_CONCURRENT_NUMBER]
                                           for i in range(0, len(interval_dates), self._MAXIMUM_CONCURRENT_NUMBER))
            response = await self._asynchronous_subset(
                chunks=chunks,
                product=product,
                latitude=latitude,
                longitude=longitude,
                band=band,
                km_above_below=km_above_below,
                km_left_right=km_left_right
            )
            return iter(response)
        else:
            return iter([all_dates])

    def async_execute_many(
        self,
        product: Products,
        latitude: float,
        longitude: float,
        band: Bands,
        start_date: str,
        end_date: str,
        km_above_below: int,
        km_left_right: int
    ) -> Iterator[dict]:
        """This returns a iterator for the location, product and band combination for combination without
        the limit of a maximum 10 modis dates per request in subset API call. This method use an asynchronous
        approach for multithreading the API call.

            via https://docs.python.org/3/library/asyncio-task.html

        Parameters
        ----------
        product: Products object
            Short name of the product, from the NASA specified sensor, to query.
        latitude: float
            Latitude in decimal degrees in geographic Lat/Long WGS 84 coordinate system.
        longitude: float
            Longitude in decimal degrees in geographic Lat/Long WGS 84 coordinate system.
        band: Bands object
            Name of data layer. If 'ALL' is selected (i.e., Band.PRODUCT-TYPE.ALL) all bands are extracted.
        start_date: str
            Composite date (i.e., AYYYYDDD, e.g., A2022023) start of the subset period, where DDD is in Day-Of-Year
            calendar (DOY) format. If there is not an acquisition for the start date, the algorithm finds the nearest
            acquisition start date.
        end_date: str
            Composite date (i.e., AYYYYDDD, e.g., A2022034) end of the subset period, where DDD is in Day-Of-Year
            calendar (DOY) format. If there is no acquisition for the end date, the algorithm finds the nearest
            acquisition end date.
        km_above_below: int
            Size in km of the subset above and below the center location. The value must be less than or equal to
            100 (0 &lt= km_above_below &lt= 100).
        km_left_right: int
            Size in km of the subset left and right of the center location. The value must be less than or equal to
            100 (0 &lt= km_left_right &lt= 100).

        Returns
        -------
        Iterator
            Iterator of all location, product and band combination.

        Examples
        --------
        >>> import time
        >>> from nasawebservice import *
        >>> provider = NasaWebServiceAPIProvider(base_url='https://modis.ornl.gov')
        >>> start_time = time.time()
        >>> many_mod13q1 = provider.async_execute_many(product=Products.MOD13Q1,
        ...                                             latitude=41.84936, longitude=13.58814,
        ...                                             start_date='A2017192', end_date='A2021321',
        ...                                             band=Bands.MOD13Q1.NDVI,
        ...                                             km_above_below=0, km_left_right=0)
        >>> print("--- %s seconds ---" % (time.time() - start_time))
        >>> for index, modis in enumerate(many_mod13q1):
        ...     # check if 'modis' is not a error message
        ...     if 'status' not in modis:
        ...         print(f'{index} -> {modis}')
        ...     else:
        ...         print(f'ERROR: {modis}')

        Raises
        ------
        ValueError
            If 'start date' >= 'end date' an ValueError is raised, because the function receives an argument
            of the correct type but an inappropriate value.

        Notes
        -----
        .. [1] If km_above_below=0 and km_left_right=0, returns the single pixel value.

        .. [2] If Maximum number of concurrent requests exceeded 10, the service cannot process more than 10 concurrent
        requests from the same host.

        .. [3] To change the maximum number of concurrent (the default value is 10) use the property setter:
        >>> provider = NasaWebServiceAPIProvider(base_url='https://modis.ornl.gov')
        >>> print(provider.maximum_concurrent_number)
        10
        >>> provider.maximum_concurrent_number = 8
        >>> print(provider.maximum_concurrent_number)
        8
        >>> provider.maximum_concurrent_number = 11
        the maximum number of concurrent cannot be 11, since the API service cannot process more than 10 concurrent
        requests from the same host.

        .. [4] Given the nature of the asynchronous multithreading approach the order of dates is not assured.

        .. [5] The asyncio.run() function to run the top-level entry point function (i.e., asynchronous_execute_all)

        """
        return asyncio.run(self._asynchronous_execute_many(
            product=product,
            latitude=latitude,
            longitude=longitude,
            band=band,
            start_date=start_date,
            end_date=end_date,
            km_above_below=km_above_below,
            km_left_right=km_left_right))
