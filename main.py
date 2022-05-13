from nasawebservice import *
from pprint import pprint

base_url = 'https://modis.ornl.gov'


if __name__ == '__main__':
    help(NasaWebServiceAPIProvider)

    base_url = 'https://modis.ornl.gov'
    provider = NasaWebServiceAPIProvider(base_url=base_url, version=1)

    all_products = provider.products(
        sensor=Sensors.ALL,
        tool=Tools.ALL
    )
    pprint(all_products)

    mod13q1_bands = provider.bands(
        product=Products.MOD13Q1
    )
    pprint(mod13q1_bands)

    mod13q1_dates = provider.dates(
        product=Products.MOD13Q1,
        latitude=44.04780019,
        longitude=10.35481917
    )
    pprint(mod13q1_dates)

    mod13q1_subsets_allbands = provider.subset(
        product=Products.MOD13Q1,
        latitude=44.04780019,
        longitude=10.35481917,
        band=Bands.MOD13Q1.ALL,
        start_date='A2020337',
        end_date='A2021113',
        km_above_below=0,
        km_left_right=0)
    pprint(mod13q1_subsets_allbands)

    mod13q1_subsets_ndvi = provider.subset(
        product=Products.MOD13Q1,
        latitude=44.04780019,
        longitude=10.35481917,
        band=Bands.MOD13Q1.NDVI,
        start_date='A2020337',
        end_date='A2021113',
        km_above_below=0,
        km_left_right=0)
    pprint(mod13q1_subsets_ndvi)

    mod13q1_many = provider.execute_many(
        product=Products.MOD13Q1,
        latitude=44.04780019,
        longitude=10.35481917,
        band=Bands.MOD13Q1.NDVI,
        start_date='A2020337',
        end_date='A2022049',
        km_above_below=0,
        km_left_right=0)

    for item in mod13q1_many:
        pprint(item)

    mod13q1_all = provider.execute_all(
        product=Products.MOD13Q1,
        latitude=44.04780019,
        longitude=10.35481917,
        band=Bands.MOD13Q1.NDVI,
        km_above_below=0,
        km_left_right=0)

    for item in mod13q1_all:
        pprint(item)

    async_mod13q1_many = provider.async_execute_many(
        product=Products.MOD13Q1,
        latitude=44.04780019,
        longitude=10.35481917,
        band=Bands.MOD13Q1.NDVI,
        start_date='A2020337',
        end_date='A2022049',
        km_above_below=0,
        km_left_right=0
    )
    for item in async_mod13q1_many:
        pprint(item)

    async_mod13q1_all = provider.async_execute_all(
        product=Products.MOD13Q1,
        latitude=44.04780019,
        longitude=10.35481917,
        band=Bands.MOD13Q1.NDVI,
        km_above_below=0,
        km_left_right=0
    )
    for item in async_mod13q1_all:
        pprint(item)

    last_product = provider.last_product(
        product=Products.MOD13Q1,
        latitude=44.04780019,
        longitude=10.35481917,
        band=Bands.MOD13Q1.NDVI,
        km_above_below=0,
        km_left_right=0
    )
    pprint(last_product)

    check = provider.is_present(
        product=Products.MOD13Q1,
        latitude=44.04780019,
        longitude=10.35481917,
        reference_date='A2019305'
    )
    print(f'Check MOD13Q1 in date A2019305: {check}')

    check = provider.is_present(
        product=Products.MOD13Q1,
        latitude=44.04780019,
        longitude=10.35481917,
        reference_date='A2019306'
    )
    print(f'Check MOD13Q1 in date A2019306: {check}')

    product_available = provider.available_products_by_date(
        latitude=44.04780019,
        longitude=10.35481917,
        reference_date='A2020337'
    )
    pprint(product_available)

