from enum import Enum, unique
from nasawebservice.utils.decorators import stringformat


@unique
@stringformat
class Sensors(Enum):
    """Get products from the specified sensor. List of all available sensors:

        - MODIS_TERRA: MODIS Terra.
        - MODIS_AQUA: MODIS Aqua.
        - MODIS_TERRA_AQUA: MODIS Terra+Aqua.
        - VIIRS-SNPP: VIIRS (Visible Infrared Imaging Radiometer Suite) - Suomi NPP.
        - Daymet: daily Surface Weather Data (Daymet) on a 1-km Grid for North America, Version 4.
        - SMAP: soil Moisture Active Passive.
        - ECOSTRESS: ecosystem Spaceborne Thermal Radiometer Experiment on Space Station.
        - SIFESDR: global solar-induced chlorophyll fluorescence (SIF).
        - ALL: get products from all sensors.

    """
    MODIS_TERRA = 'MODIS-Terra'
    MODIS_AQUA = 'MODIS-Aqua'
    MODIS_TERRA_AQUA = 'MODIS-TerraAqua'
    VIIRS_SNPP = 'VIIRS-SNPP'
    DAYMET = 'Daymet'
    SMAP = 'SMAP'
    ECOSTRESS = 'ECOSTRESS'
    SIFESDR = 'SIFESDR'
    ALL = ''


@unique
@stringformat
class Tools(Enum):
    """Get products products available for the specified tool. Available tools:

        - FIXEDSSITE: FixedSite.
        - GLOBALSUBSET: GlobalSubset.
        - ALL: get products from all tools.

    """
    FIXEDSSITE = 'FixedSite'
    GLOBALSUBSET = 'GlobalSubset'
    ALL = ''


@unique
@stringformat
class Products(Enum):
    """List of all available products (product code: description, frequency, resolution in meters).

        **MODIS TERRA**:

        - MOD09A1: MODIS/Terra Surface Reflectance (SREF) 8-Day L3 Global 500m SIN Grid, 8-Day, 500-m.
        - MOD11A2: MODIS/Terra Land Surface Temperature and Emissivity (LST) 8-Day L3 Global 1 km SIN Grid, 8-Day, 1000-m.
        - MOD13Q1: MODIS/Terra Vegetation Indices (NDVI/EVI) 16-Day L3 Global 250m SIN Grid, 16-Day, 250-m.
        - MOD14A2: MODIS/Terra Thermal Anomalies/Fire (Fire) 8-Day L3 Global 1 km SIN Grid, 8-Day, 1000-m.
        - MOD15A2H: MODIS/Terra Leaf Area Index/FPAR (LAI/FPAR) 8-Day L4 Global 500 m SIN Grid, 8-Day, 500-m.
        - MOD16A2: MODIS/Terra Net Evapotranspiration (ET) 8-Day L4 Global 500 m SIN Grid, 8-Day, 500-m.
        - MOD17A2H: MODIS/Terra Gross Primary Productivity (GPP) 8-Day L4 Global 500 m SIN Grid, 8-Day, 500-m.
        - MOD17A3HGF: MODIS/Terra Net Primary Production Gap-Filled (NPP) Yearly L4 Global 500 m SIN Grid, Yearly, 500-m.
        - MOD21A2: MODIS/Terra Land Surface Temperature/3-Band Emissivity (LSTE) 8-Day L3 Global 1 km SIN Grid, 8-Day, 1000-m.
        - MOD44B: MODIS/Terra Vegetation Continuous Fields (VCF) Yearly L3 Global 250 m SIN Grid, Yearly, 250-m.

        **MODIS AQUA**:

        - MYD09A1: MODIS/Aqua Surface Reflectance (SREF) 8-Day L3 Global 500m SIN Grid, 8-Day, 500-m.
        - MYD11A2: MODIS/Aqua Land Surface Temperature and Emissivity (LST) 8-Day L3 Global 1 km SIN Grid, 8-Day, 1000-m.
        - MYD13Q1: MODIS/Aqua Vegetation Indices (NDVI/EVI) 16-Day L3 Global 250m SIN Grid, 16-Day, 250-m.
        - MYD14A2: "MODIS/Aqua Thermal Anomalies/Fire (Fire) 8-Day L3 Global 1 km SIN Grid, 8-Day, 1000-m.
        - MYD15A2H: MODIS/Aqua Leaf Area Index/FPAR (LAI/FPAR) 8-Day L4 Global 500 m SIN Grid, 8-Day, 500-m.
        - MYD16A2: MODIS/Aqua Net Evapotranspiration (ET) 8-Day L4 Global 500 m SIN Grid, 8-Day, 500-m.
        - MYD17A2H: MODIS/Aqua Gross Primary Productivity (GPP) 8-Day L4 Global 500 m SIN Grid, 8-Day, 500-m.
        - MYD17A3HGF: MODIS/Aqua Net Primary Production Gap-Filled (NPP) Yearly L4 Global 500 m SIN Grid, Yearly, 500-m.
        - MYD21A2: MODIS/Aqua Land Surface Temperature/3-Band Emissivity (LSTE) 8-Day L3 Global 1 km SIN Grid, 8-Day, 1000-m.

        **MODIS TERRA and AQUA**:

        - MCD12Q1: MODIS/Terra+Aqua Land Cover Type (LC) Yearly L3 Global 500 m SIN Grid, Yearly, 500-m.
        - MCD12Q2: MODIS/Terra+Aqua Land Cover Dynamics (LCD) Yearly L3 Global 500 m SIN Grid, Yearly, 500-m.
        - MCD15A2H: MODIS/Terra+Aqua Leaf Area Index/FPAR (LAI/FPAR)  8-Day L4 Global 500 m SIN Grid, 8-Day, 500-m.
        - MCD15A3H: MODIS/Terra+Aqua Leaf Area Index/FPAR (LAI/FPAR) 4-Day L4 Global 500 m SIN Grid, 4-Day, 500-m.
        - MCD19A3: MODIS/Terra+Aqua BRDF Model Parameters (MAIAC) 8-Day L3 Global 1 km SIN Grid, 8-Day, 1000-m.
        - MCD43A: MODIS/Terra+Aqua BRDF and Calculated Albedo (BRDF/MCD43A) 16-Day L3 Global 500m SIN Grid, Daily, 500-m.
        - MCD43A1: MODIS/Terra+Aqua BRDF/Albedo Model Parameters (BRDF) 16-Day L3 Global 500m SIN Grid, Daily, 500-m.
        - MCD43A4: MODIS/Terra+Aqua Nadir BRDF-Adjusted Reflectance (NBAR) Daily L3 Global 500 m SIN Grid, Daily, 500-m.
        - MCD64A1: MODIS/Terra+Aqua Burned Area (Burned Area) Monthly L3 Global 500 m SIN Grid, Monthly, 500-m.

        **VIIRS-SNPP**:

        - VNP09A1: VIIRS/S-NPP Surface Reflectance (SREF) 8-Day L3 Global 1 km SIN Grid, 8-Day, 1000-m.
        - VNP09H1: VIIRS/S-NPP Surface Reflectance (SREF) 8-Day L3 Global 500m SIN Grid, 8-Day, 500-m.
        - VNP13A1: VIIRS/S-NPP Vegetation Indices (NDVI/EVI) 16-Day L3 Global 500m SIN Grid, 16-Day, 500-m.
        - VNP15A2H: VIIRS/S-NPP Leaf Area Index/FPAR (LAI/FPAR) 8-Day L4 Global 500 m SIN Grid, 8-Day, 500-m.
        - VNP21A2: VIIRS/S-NPP Land Surface Temperature and Emissivity (LSTE) 8-Day L3 Global 1 km SIN Grid, 8-Day, 1000-m.
        - VNP22Q2: VIIRS/S-NPP Land Cover Dynamics (LCD) Yearly L3 Global 500 m SIN Grid, Yearly, 500-m.

        **DAYMET**:

        - DAYMET: Daily Surface Weather Data (Daymet) on a 1-km Grid for North America, Version 4, Daily, 1000-m.

        **SMAP**:

        - SPL3SMP_E: SMAP Enhanced Radiometer Soil Moisture (SM) Daily L3 Global 9km EASE-Grid, Daily, 9000-m.
        - SPL4CMDL: SMAP Carbon Net Ecosystem Exchange (NEE) Daily L4 Global 9 km EASE-Grid, Daily, 9000-m.

        **ECOSTRESS**:

        - ECO4ESIPTJPL: ECOSTRESS Evaporative Stress Index PT-JPL (ESI) Daily L4 Global 70 m, Varies, 70-m.
        - ECO4WUE: ECOSTRESS Water Use Efficiency (WUE) Daily L4 Global 70 m, Varies, 70-m.

        **SIFESDR**:

        - SIF005: SIF Estimates from Fused SCIAMACHY and GOME-2 (SIF), Version 1, Monthly, 5000-m.
        - SIF_ANN: SIF Estimates from OCO-2 SIF and MODIS (SIF), Version 2, 16-day, 5000-m.

        **GEDI**:

        - GEDI03: GEDI Gridded Land Surface Metrics (LSM) L3 1km EASE-Grid, Version 2, One-time, 1000-m.
        - GEDI04_B: GEDI Gridded Aboveground Biomass Density (AGBD) L4B 1km EASE-Grid, Version 2, One-time, 1000-m.


    """
    # MODIS-Terra
    MOD09A1 = 'MOD09A1'
    MOD11A2 = 'MOD11A2'
    MOD13Q1 = 'MOD13Q1'
    MOD14A2 = 'MOD14A2'
    MOD15A2H = 'MOD15A2H'
    MOD16A2 = 'MOD16A2'
    MOD17A2H = 'MOD17A2H'
    MOD17A3HGF = 'MOD17A3HGF'
    MOD21A2 = 'MOD21A2'
    MOD44B = 'MOD44B'
    # MODIS-Aqua
    MYD09A1 = 'MYD09A1'
    MYD11A2 = 'MYD11A2'
    MYD13Q1 = 'MYD13Q1'
    MYD14A2 = 'MYD14A2'
    MYD15A2H = 'MYD15A2H'
    MYD16A2 = 'MYD16A2'
    MYD17A2H = 'MYD17A2H'
    MYD17A3HGF = 'MYD17A3HGF'
    MYD21A2 = 'MYD21A2'
    # MODIS-Terra and Aqua
    MCD12Q1 = 'MCD12Q1'
    MCD12Q2 = 'MCD12Q2'
    MCD15A2H = 'MCD15A2H'
    MCD15A3H = 'MCD15A3H'
    MCD19A3 = 'MCD19A3'
    MCD43A = 'MCD43A'
    MCD43A1 = 'MCD43A1'
    MCD43A4 = 'MCD43A4'
    MCD64A1 = 'MCD64A1'
    # VIIRS-SNPP
    VNP09A1 = 'VNP09A1'
    VNP09H1 = 'VNP09H1'
    VNP13A1 = 'VNP13A1'
    VNP15A2H = 'VNP15A2H'
    VNP21A2 = 'VNP21A2'
    VNP22Q2 = 'VNP22Q2'
    # DAYMET
    DAYMET = 'Daymet'
    # SMAP
    SPL3SMP_E = 'SPL3SMP_E'
    SPL4CMDL = 'SPL4CMDL'
    # ECOSTRESS
    ECO4ESIPTJPL = 'ECO4ESIPTJPL'
    ECO4WUE = 'ECO4WUE'
    # SIFESDR
    SIF005 = 'SIF005'
    SIF_ANN = 'SIF_ANN'
    # OTHERS
    GEDI03 = 'GEDI03'
    GEDI04_B = 'GEDI04_B'


# --------------------------------------------------------------
# MODIS-Terra
# --------------------------------------------------------------


@unique
@stringformat
class _BandsMOD09A1(Enum):
    """Bands available for the product MODIS/Terra Surface Reflectance (SREF)
        8-Day L3 Global 500m SIN Grid.

        frequency: 8-Day

        resolution: 500-m

        - SURFACE_REFLECTANCE_BAND_01: surface reflectance for band 1.
        - SURFACE_REFLECTANCE_BAND_02: surface reflectance for band 2.
        - SURFACE_REFLECTANCE_BAND_03: surface reflectance for band 3.
        - SURFACE_REFLECTANCE_BAND_04: surface reflectance for band 4.
        - SURFACE_REFLECTANCE_BAND_05: surface reflectance for band 5.
        - SURFACE_REFLECTANCE_BAND_06: surface reflectance for band 6.
        - SURFACE_REFLECTANCE_BAND_07: surface reflectance for band 7.
        - SURFACE_REFLECTANCE_DAY_OF_YEAR: surface reflectance day of the year.
        - SURFACE_REFLECTANCE_QUALITY_CONTROL: surface reflectance 500m quality control flags.
        - SURFACE_REFLECTANCE_RELATIVE_AZIMUTH: surface reflectance relative azimuth.
        - SURFACE_REFLECTANCE_STATE_FLAGS: surface reflectance 500m state flags.
        - SURFACE_REFLECTANCE_SOLAR_ZENITH: surface reflectance solar zenith.
        - SURFACE_REFLECTANCE_VIEW_ZENITH: surface reflectance view zenith.
        - ALL: all MOD09A1 bands.

    """
    SURFACE_REFLECTANCE_BAND_01 = 'sur_refl_b01'
    SURFACE_REFLECTANCE_BAND_02 = 'sur_refl_b02'
    SURFACE_REFLECTANCE_BAND_03 = 'sur_refl_b03'
    SURFACE_REFLECTANCE_BAND_04 = 'sur_refl_b04'
    SURFACE_REFLECTANCE_BAND_05 = 'sur_refl_b05'
    SURFACE_REFLECTANCE_BAND_06 = 'sur_refl_b06'
    SURFACE_REFLECTANCE_BAND_07 = 'sur_refl_b07'
    SURFACE_REFLECTANCE_DAY_OF_YEAR = 'sur_refl_day_of_year'
    SURFACE_REFLECTANCE_QUALITY_CONTROL = 'sur_refl_qc_500m'
    SURFACE_REFLECTANCE_RELATIVE_AZIMUTH = 'sur_refl_raz'
    SURFACE_REFLECTANCE_STATE_FLAGS = 'sur_refl_state_500m'
    SURFACE_REFLECTANCE_SOLAR_ZENITH = 'sur_refl_szen'
    SURFACE_REFLECTANCE_VIEW_ZENITH = 'sur_refl_vzen'
    ALL = 'all'


@unique
@stringformat
class _BandsMOD11A2(Enum):
    """Bands available for the product MODIS/Terra Land Surface Temperature and Emissivity (LST)
        8-Day L3 Global 1 km SIN Grid.

        frequency: 8-Day

        resolution: 1000-m

        - DAYS_CLEAR_SKY_COVERAGE: Day clear-sky coverage.
        - NIGHTS_CLEAR_SKY_COVERAGE: Night clear-sky coverage.
        - DAY_VIEW_ANGLE_OBSERVATION: View zenith angle of day observation.
        - DAY_LOCAL_TIME_OBSERVATION: Local time of day observation
        - EMISSIVITY_BAND_31: Band 31 emissivity.
        - EMISSIVITY_BAND_32: Band 32 emissivity.
        - DAY_LAND_SURFACE_TEMPERATURE:  Daytime Land Surface Temperature.
        - NIGHT_LAND_SURFACE_TEMPERATURE: Nighttime Land Surface Temperature.
        - NIGHT_VIEW_ANGLE_OBSERVATION: View zenith angle of night observation.
        - NIGHT_LOCAL_TIME_OBSERVATION: Local time of night observation.
        - DAY_LAND_SURFACE_TEMPERATURE_QUALITY_INDICATORS: daytime LST quality Indicators.
        - NIGHT_LAND_SURFACE_TEMPERATURE_QUALITY_INDICATORS: nighttime LST quality indicators.
        - ALL: all MOD11A2 bands.

    """
    DAYS_CLEAR_SKY_COVERAGE = 'Clear_sky_days'
    NIGHTS_CLEAR_SKY_COVERAGE = 'Clear_sky_nights'
    DAY_VIEW_ANGLE_OBSERVATION = 'Day_view_angl'
    DAY_LOCAL_TIME_OBSERVATION = 'Day_view_time'
    EMISSIVITY_BAND_31 = 'Emis_31'
    EMISSIVITY_BAND_32 = 'Emis_32'
    DAY_LAND_SURFACE_TEMPERATURE = 'LST_Day_1km'
    NIGHT_LAND_SURFACE_TEMPERATURE = 'LST_Night_1km'
    NIGHT_VIEW_ANGLE_OBSERVATION = 'Night_view_angl'
    NIGHT_LOCAL_TIME_OBSERVATION = 'Night_view_time'
    DAY_LAND_SURFACE_TEMPERATURE_QUALITY_INDICATORS = 'QC_Day'
    NIGHT_LAND_SURFACE_TEMPERATURE_QUALITY_INDICATORS = 'QC_Night'
    ALL = 'all'


@unique
@stringformat
class _BandsMOD13Q1(Enum):
    """Bands available for the product MOD13Q1 (MODIS/Terra Vegetation Indices (NDVI/EVI)
        16-Day L3 Global 250m SIN.

        frequency: 16-Day

        resolution: 250-m

        - BLUE_REFLECTANCE: Surface Reflectance Band 3.
        - COMPOSITE_DAY_OF_THE_YEAR: Day of year VI pixel.
        - EVI: EVI 16 day average.
        - MIR_REFLECTANCE: Surface Reflectance Band 7.
        - NDVI: NDVI 16 day average.
        - NIR_REFLECTANCE: Surface Reflectance Band 2.
        - PIXEL_RELIABILITY: Quality reliability of VI pixel.
        - RED_REFLECTANCE: Surface Reflectance Band 1.
        - RELATIVE_AZIMUTH_ANGLE: relative azimuth angle of VI pixel.
        - SUN_ZENITH_ANGLE: Sun zenith angle of VI pixel.
        - VIEW_ZENITH_ANGLE: View zenith angle of VI Pixel.
        - VI_QUALITY: VI quality indicators.
        - ALL: all MOD13Q1 bands.

    """
    BLUE_REFLECTANCE = "250m_16_days_blue_reflectance"
    COMPOSITE_DAY_OF_THE_YEAR = "250m_16_days_composite_day_of_the_year"
    EVI = "250m_16_days_EVI"
    MIR_REFLECTANCE = "250m_16_days_MIR_reflectance"
    NDVI = "250m_16_days_NDVI"
    NIR_REFLECTANCE = "250m_16_days_NIR_reflectance"
    PIXEL_RELIABILITY = "250m_16_days_pixel_reliability"
    RED_REFLECTANCE = "250m_16_days_red_reflectance"
    RELATIVE_AZIMUTH_ANGLE = "250m_16_days_relative_azimuth_angle"
    SUN_ZENITH_ANGLE = "250m_16_days_sun_zenith_angle"
    VIEW_ZENITH_ANGLE = "250m_16_days_view_zenith_angle"
    VI_QUALITY = "250m_16_days_VI_Quality"
    ALL = 'all'


@unique
@stringformat
class _BandsMOD14A2(Enum):
    """Bands available for the product MODIS/Terra Thermal Anomalies/Fire (Fire)
        8-Day L3 Global 1 km SIN Grid.

        frequency: 8-Day

        resolution: 1000-m

        - FIRE_MASK: fire mask.
        - PIXEL_QUALITY: pixel quality.
        - ALL: all MOD14A2 bands.

    """
    FIRE_MASK = 'FireMask'
    PIXEL_QUALITY = 'pixel quality'
    ALL = 'all'


@unique
@stringformat
class _BandsMOD15A2H(Enum):
    """Bands available for the product MODIS/Terra Leaf Area Index/FPAR (LAI/FPAR)
        8-Day L4 Global 500 m SIN Grid.

        frequency: 8-Day

        resolution: 500-m

        - EXTRA_DETAIL_QUALITY_LAI_AND_FPAR: Extra detail Quality for LAI (Leaf Area Index) and FPAR (Fraction of photosynthetically active radiation).
        - QUALITY_LAI_AND_FPAR: Quality for LAI (Leaf Area Index) and FPAR (Fraction of photosynthetically active radiation).
        - STANDARD_DEVIATION_FPAR: Standard deviation for FPAR (Fraction of photosynthetically active radiation).
        - FPAR: Fraction of photosynthetically active radiation.
        - STANDARD_DEVIATION_LAI: Standard deviation for LAI.
        - LAI: Leaf Area Index.
        - ALL: all MOD15A2H bands.

    """
    EXTRA_DETAIL_QUALITY_LAI_AND_FPAR = 'FparExtra_QC'
    QUALITY_LAI_AND_FPAR = 'FparLai_QC'
    STANDARD_DEVIATION_FPAR = 'FparStdDev_500m'
    FPAR = 'Fpar_500m'
    STANDARD_DEVIATION_LAI = 'LaiStdDev_500m'
    LAI = 'Lai_500m'
    ALL = 'all'


@unique
@stringformat
class _BandsMOD16A2(Enum):
    """Bands available for the product MODIS/Terra Net Evapotranspiration (ET)
        8-Day L4 Global 500 m SIN Grid.

        frequency: 8-Day

        resolution: 500-m

        - EVAPOTRANSPIRATION: Evapotranspiration.
        - QUALITY_CONTROL_EVAPOTRANSPIRATION: QC for ET (Evapotranspiration)/LE (Latent heat flux).
        - LATENT_HEAT_FLUX: Latent heat flux (LE)
        - POTENTIAL_EVAPOTRANSPIRATION: Potential evapotranspiration.
        - POTENTIAL_LATENT_HEAT_FLUX: Potential latent heat flux (LE).
        - ALL: all MOD16A2 bands.

    """
    EVAPOTRANSPIRATION = 'ET_500m'
    QUALITY_CONTROL_EVAPOTRANSPIRATION = 'ET_QC_500m'
    LATENT_HEAT_FLUX = 'LE_500m'
    POTENTIAL_EVAPOTRANSPIRATION = 'PET_500m'
    POTENTIAL_LATENT_HEAT_FLUX = 'PLE_500m'
    ALL = 'all'


@unique
@stringformat
class _BandsMOD17A2H(Enum):
    """Bands available for the product MODIS/Terra Gross Primary Productivity (GPP)
        8-Day L4 Global 500 m SIN Grid.

        frequency: 8-Day

        resolution: 500-m

        - GROSS_PRIMARY_PRODUCTION: Gross Primary Production.
        - NET_PHOTOSYNTHESIS: Net Photosynthesis.
        - QUALITY_CONTROL_BITS: Quality Control bits.
        - ALL: all MOD17A2H bands.

    """
    GROSS_PRIMARY_PRODUCTION = 'Gpp_500m'
    NET_PHOTOSYNTHESIS = 'PsnNet_500m'
    QUALITY_CONTROL_BITS = 'Psn_QC_500m'
    ALL = 'all'


@unique
@stringformat
class _BandsMOD17A3HGF(Enum):
    """Bands available for the product MODIS/Terra Net Primary Production Gap-Filled (NPP)
        Yearly L4 Global 500 m SIN Grid.

        frequency: Yearly

        resolution: 500-m

        - NET_PRIMARY_PRODUCTIVITY: net Primary Productivity.
        - QUALITY_CONTROL_BITS: net Primary Productivity quality control bits.
        - ALL: all MOD17A3HGF bands.

    """
    NET_PRIMARY_PRODUCTIVITY = 'Npp_500m'
    QUALITY_CONTROL_BITS = 'Npp_QC_500m'
    ALL = 'all'


@unique
@stringformat
class _BandsMOD21A2(Enum):
    """Bands available for the product MODIS/Terra Land Surface Temperature/3-Band Emissivity (LSTE)
        8-Day L3 Global 1 km SIN Grid.

        frequency: 8-Day

        resolution: 1000-m

        - EMISSIVITY_BAND_29: band 29 emissivity.
        - EMISSIVITY_BAND_31: band 31 emissivity.
        - EMISSIVITY_BAND_32: band 32 emissivity.
        - DAY_LAND_SURFACE_TEMPERATURE: 8-day daytime 1km grid Land-surface Temperature
        - NIGHT_LAND_SURFACE_TEMPERATURE: 8-day nighttime 1km grid Land-surface Temperature
        - DAY_QUALITY_CONTROL: quality control for daytime LST and emissivity
        - NIGHT_QUALITY_CONTROL: quality control for nighttime LST and emissivity
        - DAY_VIEW_ZENITH_ANGLE_TEMPERATURE: average view zenith angle of daytime temperature
        - NIGHT_VIEW_ZENITH_ANGLE_TEMPERATURE: average view zenith angle of nighttime temperature
        - DAY_VIEW_TIME: average time of daytime observation
        - NIGHT_VIEW_TIME: average time of nighttime observation
        - ALL: all MOD21A2 bands.

    """
    EMISSIVITY_BAND_29 = 'Emis_29'
    EMISSIVITY_BAND_31 = 'Emis_31'
    EMISSIVITY_BAND_32 = 'Emis_32'
    DAY_LAND_SURFACE_TEMPERATURE = 'LST_Day_1KM'
    NIGHT_LAND_SURFACE_TEMPERATURE = 'LST_Night_1KM'
    DAY_QUALITY_CONTROL = 'QC_Day'
    NIGHT_QUALITY_CONTROL = 'QC_Night'
    DAY_VIEW_ZENITH_ANGLE_TEMPERATURE = 'View_Angle_Day'
    NIGHT_VIEW_ZENITH_ANGLE_TEMPERATURE = 'View_Angle_Night'
    DAY_VIEW_TIME = 'View_Time_Day'
    NIGHT_VIEW_TIME = 'View_Time_Night'
    ALL = 'all'


@unique
@stringformat
class _BandsMOD44B(Enum):
    """Bands available for the product MODIS/Terra Vegetation Continuous Fields (VCF)
        Yearly L3 Global 250 m SIN Grid.

        frequency: Yearly

        resolution: 250-m

        - CLOUD_COVER: cloud cover indicators.
        - PERCENT_NON_TREE_VEGETATION: percent nontree vegetation.
        - PERCENT_NON_VEGETATED: percent non-vegetated.
        - PERCENT_NON_VEGETATED_STANDARD_DEVIATION: percent non-vegetated standard deviation (SD).
        - PERCENT_TREE_COVER: percent tree cover.
        - PERCENT_TREE_COVER_STANDARD_DEVIATION: percent tree cover standard deviation (SD).
        - QUALITY_CONTROL: quality Control indicators.
        - ALL: all MOD44B bands.

    """
    CLOUD_COVER = 'Cloud'
    PERCENT_NON_TREE_VEGETATION = 'Percent_NonTree_Vegetation'
    PERCENT_NON_VEGETATED = 'Percent_NonVegetated'
    PERCENT_NON_VEGETATED_STANDARD_DEVIATION = 'Percent_NonVegetated_SD'
    PERCENT_TREE_COVER = 'Percent_Tree_Cover'
    PERCENT_TREE_COVER_STANDARD_DEVIATION = 'Percent_Tree_Cover_SD'
    QUALITY_CONTROL = 'Quality'
    ALL = 'all'


# --------------------------------------------------------------
# MODIS-Aqua
# --------------------------------------------------------------


@unique
@stringformat
class _BandsMYD09A1(Enum):
    """Bands available for the product MODIS/Aqua Surface Reflectance (SREF)
        8-Day L3 Global 500m SIN Grid.

        frequency: 8-Day

        resolution: 500-m

        - SURFACE_REFLECTANCE_BAND_01: surface reflectance for band 1.
        - SURFACE_REFLECTANCE_BAND_02: surface reflectance for band 2.
        - SURFACE_REFLECTANCE_BAND_03: surface reflectance for band 3.
        - SURFACE_REFLECTANCE_BAND_04: surface reflectance for band 4.
        - SURFACE_REFLECTANCE_BAND_05: surface reflectance for band 5.
        - SURFACE_REFLECTANCE_BAND_06: surface reflectance for band 6.
        - SURFACE_REFLECTANCE_BAND_07: surface reflectance for band 7.
        - SURFACE_REFLECTANCE_DAY_OF_YEAR: surface reflectance day of the year.
        - SURFACE_REFLECTANCE_QUALITY_CONTROL: surface reflectance 500m quality control flags.
        - SURFACE_REFLECTANCE_RELATIVE_AZIMUTH: surface reflectance relative azimuth.
        - SURFACE_REFLECTANCE_STATE_FLAGS: surface reflectance 500m state flags.
        - SURFACE_REFLECTANCE_SOLAR_ZENITH: surface reflectance solar zenith.
        - SURFACE_REFLECTANCE_VIEW_ZENITH: surface reflectance view zenith.
        - ALL: all MYD09A1 bands.

    """
    SURFACE_REFLECTANCE_BAND_01 = 'sur_refl_b01'
    SURFACE_REFLECTANCE_BAND_02 = 'sur_refl_b02'
    SURFACE_REFLECTANCE_BAND_03 = 'sur_refl_b03'
    SURFACE_REFLECTANCE_BAND_04 = 'sur_refl_b04'
    SURFACE_REFLECTANCE_BAND_05 = 'sur_refl_b05'
    SURFACE_REFLECTANCE_BAND_06 = 'sur_refl_b06'
    SURFACE_REFLECTANCE_BAND_07 = 'sur_refl_b07'
    SURFACE_REFLECTANCE_DAY_OF_YEAR = 'sur_refl_day_of_year'
    SURFACE_REFLECTANCE_QUALITY_CONTROL = 'sur_refl_qc_500m'
    SURFACE_REFLECTANCE_RELATIVE_AZIMUTH = 'sur_refl_raz'
    SURFACE_REFLECTANCE_STATE_FLAGS = 'sur_refl_state_500m'
    SURFACE_REFLECTANCE_SOLAR_ZENITH = 'sur_refl_szen'
    SURFACE_REFLECTANCE_VIEW_ZENITH = 'sur_refl_vzen'
    ALl = 'all'


@unique
@stringformat
class _BandsMYD11A2(Enum):
    """Bands available for the product MODIS/Aqua Land Surface Temperature and Emissivity (LST)
        8-Day L3 Global 1 km SIN Grid.

        frequency: 8-Day

        resolution: 1000-m

        - DAYS_CLEAR_SKY_COVERAGE: Day clear-sky coverage.
        - NIGHTS_CLEAR_SKY_COVERAGE: Night clear-sky coverage.
        - DAY_VIEW_ANGLE_OBSERVATION: View zenith angle of day observation.
        - DAY_LOCAL_TIME_OBSERVATION: Local time of day observation
        - EMISSIVITY_BAND_31: Band 31 emissivity.
        - EMISSIVITY_BAND_32: Band 32 emissivity.
        - DAY_LAND_SURFACE_TEMPERATURE:  Daytime Land Surface Temperature.
        - NIGHT_LAND_SURFACE_TEMPERATURE: Nighttime Land Surface Temperature.
        - NIGHT_VIEW_ANGLE_OBSERVATION: View zenith angle of night observation.
        - NIGHT_LOCAL_TIME_OBSERVATION: Local time of night observation.
        - DAY_LAND_SURFACE_TEMPERATURE_QUALITY_INDICATORS: daytime LST quality Indicators.
        - NIGHT_LAND_SURFACE_TEMPERATURE_QUALITY_INDICATORS: nighttime LST quality indicators.
        - ALL: all MYD11A2 bands.

    """
    DAYS_CLEAR_SKY_COVERAGE = 'Clear_sky_days'
    NIGHTS_CLEAR_SKY_COVERAGE = 'Clear_sky_nights'
    DAY_VIEW_ANGLE_OBSERVATION = 'Day_view_angl'
    DAY_LOCAL_TIME_OBSERVATION = 'Day_view_time'
    EMISSIVITY_BAND_31 = 'Emis_31'
    EMISSIVITY_BAND_32 = 'Emis_32'
    DAY_LAND_SURFACE_TEMPERATURE = 'LST_Day_1km'
    NIGHT_LAND_SURFACE_TEMPERATURE = 'LST_Night_1km'
    NIGHT_VIEW_ANGLE_OBSERVATION = 'Night_view_angl'
    NIGHT_LOCAL_TIME_OBSERVATION = 'Night_view_time'
    DAY_LAND_SURFACE_TEMPERATURE_QUALITY_INDICATORS = 'QC_Day'
    NIGHT_LAND_SURFACE_TEMPERATURE_QUALITY_INDICATORS = 'QC_Night'
    ALL = 'all'


@unique
@stringformat
class _BandsMYD13Q1(Enum):
    """Bands available for the product MODIS/Aqua Vegetation Indices (NDVI/EVI)
        16-Day L3 Global 250m SIN Grid.

            frequency: 16-Day

            resolution: 250-m

        - BLUE_REFLECTANCE: Surface Reflectance Band 3.
        - COMPOSITE_DAY_OF_THE_YEAR: Day of year VI pixel.
        - EVI: EVI 16 day average.
        - MIR_REFLECTANCE: Surface Reflectance Band 7.
        - NDVI: NDVI 16 day average.
        - NIR_REFLECTANCE: Surface Reflectance Band 2.
        - PIXEL_RELIABILITY: Quality reliability of VI pixel.
        - RED_REFLECTANCE: Surface Reflectance Band 1.
        - RELATIVE_AZIMUTH_ANGLE: relative azimuth angle of VI pixel.
        - SUN_ZENITH_ANGLE: Sun zenith angle of VI pixel.
        - VIEW_ZENITH_ANGLE: View zenith angle of VI Pixel.
        - VI_QUALITY: VI quality indicators.
        - ALL: all MYD13Q1 bands.

    """
    BLUE_REFLECTANCE = '250m_16_days_blue_reflectance'
    COMPOSITE_DAY_OF_THE_YEAR = '250m_16_days_composite_day_of_the_year'
    EVI = '250m_16_days_EVI'
    MIR_REFLECTANCE = '250m_16_days_MIR_reflectance'
    NDVI = '250m_16_days_NDVI'
    PIXEL_RELIABILITY = '250m_16_days_pixel_reliability'
    RED_REFLECTANCE = '250m_16_days_red_reflectance'
    RELATIVE_AZIMUTH_ANGLE = '250m_16_days_relative_azimuth_angle'
    SUN_ZENITH_ANGLE = '250m_16_days_sun_zenith_angle"'
    VIEW_ZENITH_ANGLE = '250m_16_days_view_zenith_angle'
    VI_QUALITY = '250m_16_days_VI_Quality'
    ALL = 'all'


@unique
@stringformat
class _BandsMYD14A2(Enum):
    """Bands available for the product MODIS/Aqua Thermal Anomalies/Fire (Fire)
        8-Day L3 Global 1 km SIN Grid.

        frequency: 8-Day

        resolution: 1000-m

        - FIRE_MASK: fire mask.
        - PIXEL_QUALITY: pixel quality.
        - ALL: all MYD14A2 bands.

    """
    FIRE_MASK = 'FireMask'
    PIXEL_QUALITY = 'QA'
    ALL = 'all'


@unique
@stringformat
class _BandsMYD15A2H(Enum):
    """Bands available for the product MODIS/Aqua Leaf Area Index/FPAR (LAI/FPAR)
        8-Day L4 Global 500 m SIN Grid.

        frequency: 8-Day

        resolution: 500-m

        - EXTRA_DETAIL_QUALITY_LAI_AND_FPAR: Extra detail Quality for LAI (Leaf Area Index) and FPAR (Fraction of photosynthetically active radiation).
        - QUALITY_LAI_AND_FPAR: Quality for LAI (Leaf Area Index) and FPAR (Fraction of photosynthetically active radiation).
        - STANDARD_DEVIATION_FPAR: Standard deviation for FPAR (Fraction of photosynthetically active radiation).
        - FPAR: Fraction of photosynthetically active radiation.
        - STANDARD_DEVIATION_LAI: Standard deviation for LAI.
        - LAI: Leaf Area Index.
        - ALL: all MYD15A2H bands.

    """
    EXTRA_DETAIL_QUALITY_LAI_AND_FPAR = 'FparExtra_QC'
    QUALITY_LAI_AND_FPAR = 'FparLai_QC'
    STANDARD_DEVIATION_FPAR = 'FparStdDev_500m'
    FPAR = 'Fpar_500m'
    STANDARD_DEVIATION_LAI = 'LaiStdDev_500m'
    LAI = 'Lai_500m'
    ALL = 'all'


@unique
@stringformat
class _BandsMYD16A2(Enum):
    """Bands available for the product MODIS/Aqua Net Evapotranspiration (ET)
        8-Day L4 Global 500 m SIN Grid.

        frequency: 8-Day

        resolution: 500-m

        - EVAPOTRANSPIRATION: Evapotranspiration.
        - QUALITY_CONTROL_EVAPOTRANSPIRATION: QC for ET (Evapotranspiration)/LE (Latent heat flux).
        - LATENT_HEAT_FLUX: Latent heat flux (LE)
        - POTENTIAL_EVAPOTRANSPIRATION: Potential evapotranspiration.
        - POTENTIAL_LATENT_HEAT_FLUX: Potential latent heat flux (LE).
        - ALL: all MYD16A2 bands.

    """
    EVAPOTRANSPIRATION = 'ET_500m'
    QUALITY_CONTROL_EVAPOTRANSPIRATION = 'ET_QC_500m'
    LATENT_HEAT_FLUX = 'LE_500m'
    POTENTIAL_EVAPOTRANSPIRATION = 'PET_500m'
    POTENTIAL_LATENT_HEAT_FLUX = 'PLE_500m'
    ALL = 'all'


@unique
@stringformat
class _BandsMYD17A2H(Enum):
    """Bands available for the product MODIS/Aqua Gross Primary Productivity (GPP)
        8-Day L4 Global 500 m SIN Grid.

        frequency: 8-Day

        resolution: 500-m

        - GROSS_PRIMARY_PRODUCTION: Gross Primary Production.
        - NET_PHOTOSYNTHESIS: Net Photosynthesis.
        - QUALITY_CONTROL_BITS: Quality Control bits.
        - ALL: all MYD17A2H bands.

    """
    GROSS_PRIMARY_PRODUCTION = 'Gpp_500m'
    NET_PHOTOSYNTHESIS = 'PsnNet_500m'
    QUALITY_CONTROL_BITS = 'Psn_QC_500m'
    ALL = 'all'


@unique
@stringformat
class _BandsMYD17A3HGF(Enum):
    """Bands available for the product MODIS/Aqua Net Primary Production Gap-Filled (NPP)
        Yearly L4 Global 500 m SIN Grid.

        frequency: Yearly

        resolution: 500-m

        - NET_PRIMARY_PRODUCTIVITY: net Primary Productivity.
        - QUALITY_CONTROL_BITS: net Primary Productivity quality control bits.
        - ALL: all MYD17A3HGF bands.

    """
    NET_PRIMARY_PRODUCTIVITY = 'Npp_500m'
    QUALITY_CONTROL_BITS = 'Npp_QC_500m'
    ALL = 'all'


@unique
@stringformat
class _BandsMYD21A2(Enum):
    """Bands available for the product MODIS/Aqua Land Surface Temperature/3-Band Emissivity (LSTE)
        8-Day L3 Global 1 km SIN Grid.

        frequency: 8-Day

        resolution: 1000-m

        - EMISSIVITY_BAND_29: band 29 emissivity.
        - EMISSIVITY_BAND_31: band 31 emissivity.
        - EMISSIVITY_BAND_32: band 32 emissivity.
        - DAY_LAND_SURFACE_TEMPERATURE: 8-day daytime 1km grid Land-surface Temperature
        - NIGHT_LAND_SURFACE_TEMPERATURE: 8-day nighttime 1km grid Land-surface Temperature
        - DAY_QUALITY_CONTROL: quality control for daytime LST and emissivity
        - NIGHT_QUALITY_CONTROL: quality control for nighttime LST and emissivity
        - DAY_VIEW_ZENITH_ANGLE_TEMPERATURE: average view zenith angle of daytime temperature
        - NIGHT_VIEW_ZENITH_ANGLE_TEMPERATURE: average view zenith angle of nighttime temperature
        - DAY_VIEW_TIME: average time of daytime observation
        - NIGHT_VIEW_TIME: average time of nighttime observation
        - ALL: all MYD21A2 bands.

    """
    EMISSIVITY_BAND_29 = 'Emis_29'
    EMISSIVITY_BAND_31 = 'Emis_31'
    EMISSIVITY_BAND_32 = 'Emis_32'
    DAY_LAND_SURFACE_TEMPERATURE = 'LST_Day_1KM'
    NIGHT_LAND_SURFACE_TEMPERATURE = 'LST_Night_1KM'
    DAY_QUALITY_CONTROL = 'QC_Day'
    NIGHT_QUALITY_CONTROL = 'QC_Night'
    DAY_VIEW_ZENITH_ANGLE_TEMPERATURE = 'View_Angle_Day'
    NIGHT_VIEW_ZENITH_ANGLE_TEMPERATURE = 'View_Angle_Night'
    DAY_VIEW_TIME = 'View_Time_Day'
    NIGHT_VIEW_TIME = 'View_Time_Night'
    ALL = 'all'


# --------------------------------------------------------------
# MODIS-TerraAqua
# --------------------------------------------------------------


@unique
@stringformat
class _BandsMCD12Q1(Enum):
    """Bands available for the product MODIS/Terra+Aqua Land Cover Type (LC)
        Yearly L3 Global 500 m SIN Grid.

        frequency: Yearly

        resolution: 500-m

        - LAND_COVER_FAO_COVER: FAO Land Cover Classification System 1 (LCCS1) land cover layer.
        - LAND_COVER_FAO_COVER_CONFIDENCE: FAO Land Cover Classification System 1 (LCCS1) land cover layer confidence.
        - LAND_COVER_FAO_USE: FAO Land Cover Classification System 2 (LCCS2) land use layer.
        - LAND_COVER_FAO_USE_CONFIDENCE: FAO Land Cover Classification System 2 (LCCS2) land use layer confidence.
        - LAND_COVER_FAO_SURFACE_HYDROLOGY: FAO Land Cover Classification System 3 (LCCS3) surface hydrology layer.
        - LAND_COVER_FAO_SURFACE_HYDROLOGY_CONFIDENCE: FAO Land Cover Classification System 3 (LCCS3) surface hydrology layer confidence.
        - LAND_COVER_TYPE_IGBP: Land Cover Type 1 Annual International Geosphere-Biosphere Programme (IGBP) classification.
        - LAND_COVER_TYPE_UMD: Land Cover Type 2 Annual University of Maryland (UMD) classification.
        - LAND_COVER_TYPE_LAI: Land Cover Type 3 Annual Leaf Area Index (LAI) classification.
        - LAND_COVER_TYPE_BGC: Land Cover Type 4 Annual BIOME-Biogeochemical Cycles (BGC) classification.
        - LAND_COVER_TYPE_PF: Land Cover Type 5 Annual Plant Functional Types classification.
        - LAND_WATER_CLASSIFICATION: Binary land (class 2) or water (class 1) mask derived from MOD44W.
        - QUALITY_CONTROL: product quality flags.
        - ALL: all MCD12Q1 bands.

    """
    LAND_COVER_FAO_COVER = 'LC_Prop1'
    LAND_COVER_FAO_COVER_CONFIDENCE = 'LC_Prop1_Assessment'
    LAND_COVER_FAO_USE = 'LC_Prop2'
    LAND_COVER_FAO_USE_CONFIDENCE = 'LC_Prop2_Assessment'
    LAND_COVER_FAO_SURFACE_HYDROLOGY = 'LC_Prop3'
    LAND_COVER_FAO_SURFACE_HYDROLOGY_CONFIDENCE = 'LC_Prop3_Assessment'
    LAND_COVER_TYPE_IGBP = 'LC_Type1'
    LAND_COVER_TYPE_UMD = 'LC_Type2'
    LAND_COVER_TYPE_LAI = 'LC_Type3'
    LAND_COVER_TYPE_BGC = 'LC_Type4'
    LAND_COVER_TYPE_PF = 'LC_Type5'
    LAND_WATER_CLASSIFICATION = 'LW'
    QUALITY_CONTROL = 'QC'
    ALL = 'all'


@unique
@stringformat
class _BandsMCD12Q2(Enum):
    """Bands available for the product MODIS/Terra+Aqua Land Cover Dynamics (LCD)
        Yearly L3 Global 500 m SIN Grid.

        frequency: Yearly

        resolution:500-m

        - ONSET_DORMANCY_MODES_01: Onset Dormancy number modes 1.
        - ONSET_DORMANCY_MODES_02: Onset Dormancy number modes 2.
        - EVI_AMPLITUDE_MODES_01: EVI Amplitude number modes 1.
        - EVI_AMPLITUDE_MODES_02: EVI Amplitude number modes 2.
        - EVI_AREA_MODES_01: EVI Area number modes 1.
        - EVI_AREA_MODES_02: EVI Area number modes 2.
        - EVI_MINIMUM_MODES_01: EVI Minimum number modes 1.
        - EVI_MINIMUM_MODES_02: EVI Minimum number modes 2.
        - GREEN_INCREASE_MODES_01: Onset Greenness Increase number modes 1.
        - GREEN_INCREASE_MODES_02: Onset Greenness Increase number modes 2.
        - MATURITY_MODES_01: Onset Maturity number number modes 1.
        - MATURITY_MODES_02: Onset Maturity number number modes 2.
        - MIDGREEN_DECREASE_MODES_01: Middle Greenness Decrease number modes 1.
        - MIDGREEN_DECREASE_MODES_02: Middle Greenness Decrease number modes 2.
        - MIDGREEN_INCREASE_MODES_01: Middle Greenness Increase number modes 1.
        - MIDGREEN_INCREASE_MODES_02: Middle Greenness Increase number modes 2.
        - NUMBER_CYCLES: number of cycles.
        - QUALITY_ASSESSMENT_DETAILED_MODES_01: Quality Assessment Detailed number modes 1.
        - QUALITY_ASSESSMENT_DETAILED_MODES_02: Quality Assessment Detailed number modes 2.
        - QUALITY_ASSESSMENT_OVERALL_MODES_01: Quality Assessment Overall number modes 1.
        - QUALITY_ASSESSMENT_OVERALL_MODES_02: Quality Assessment Detailed number modes 2.
        - ALL: all MCD12Q2 bands.
    """
    ONSET_DORMANCY_MODES_01 = 'Dormancy.Num_Modes_01'
    ONSET_DORMANCY_MODES_02 = 'Dormancy.Num_Modes_02'
    EVI_AMPLITUDE_MODES_01 = 'EVI_Amplitude.Num_Modes_01'
    EVI_AMPLITUDE_MODES_02 = 'EVI_Amplitude.Num_Modes_02'
    EVI_AREA_MODES_01 = 'EVI_Area.Num_Modes_01'
    EVI_AREA_MODES_02 = 'EVI_Area.Num_Modes_02'
    EVI_MINIMUM_MODES_01 = 'EVI_Minimum.Num_Modes_01'
    EVI_MINIMUM_MODES_02 = 'EVI_Minimum.Num_Modes_02'
    GREEN_INCREASE_MODES_01 = 'Greenup.Num_Modes_01'
    GREEN_INCREASE_MODES_02 = 'Greenup.Num_Modes_02'
    MATURITY_MODES_01 = 'Maturity.Num_Modes_01'
    MATURITY_MODES_02 = 'Maturity.Num_Modes_02'
    MIDGREEN_DECREASE_MODES_01 = 'MidGreendown.Num_Modes_01'
    MIDGREEN_DECREASE_MODES_02 = 'MidGreendown.Num_Modes_02'
    MIDGREEN_INCREASE_MODES_01 = 'MidGreenup.Num_Modes_01'
    MIDGREEN_INCREASE_MODES_02 = 'MidGreenup.Num_Modes_02'
    NUMBER_CYCLES = 'NumCycles'
    QUALITY_ASSESSMENT_DETAILED_MODES_01 = 'QA_Detailed.Num_Modes_01'
    QUALITY_ASSESSMENT_DETAILED_MODES_02 = 'QA_Detailed.Num_Modes_02'
    QUALITY_ASSESSMENT_OVERALL_MODES_01 = 'QA_Overall.Num_Modes_01'
    QUALITY_ASSESSMENT_OVERALL_MODES_02 = 'QA_Overall.Num_Modes_02'
    ALL = 'all'


@unique
@stringformat
class _BandsMCD15A2H(Enum):
    """Bands available for the product MODIS/Terra+Aqua Leaf Area Index/FPAR (LAI/FPAR)
        8-Day L4 Global 500 m SIN Grid.

        frequency: 8-Day

        resolution: 500-m

        - EXTRA_QUALITY_CONTROL_LAI_AND_FPAR: Extra detail Quality for LAI (Leaf Area Index) and FPAR (Fraction of photosynthetically active radiation).
        - QUALITY_CONTROL_LAI_AND_FPAR: Quality for LAI (Leaf Area Index) and FPAR (Fraction of photosynthetically active radiation).
        - FPAIR_STANDARD_DEVIATION: Standard deviation of FPAR (Fraction of photosynthetically active radiation).
        - FPAIR: Fraction of photosynthetically active radiation (FPAIR).
        - LAI_STANDARD_DEVIATION: Standard deviation for LAI (Leaf Area Index).
        - LAI: Leaf area index (LAI).
        - ALL: all MCD15A2H bands.

    """
    EXTRA_QUALITY_CONTROL_LAI_AND_FPAR = 'FparExtra_QC'
    QUALITY_CONTROL_LAI_AND_FPAR = 'FparLai_QC'
    FPAIR_STANDARD_DEVIATION = 'FparStdDev_500m'
    FPAIR = 'Fpar_500m'
    LAI_STANDARD_DEVIATION = 'LaiStdDev_500m'
    LAI = 'Lai_500m'
    ALL = 'all'


@unique
@stringformat
class _BandsMCD15A3H(Enum):
    """Bands available for the product MODIS/Terra+Aqua Leaf Area Index/FPAR (LAI/FPAR)
        4-Day L4 Global 500 m SIN Grid.

        frequency: 4-Day

        resolution: 500-m

        - EXTRA_QUALITY_CONTROL_LAI_AND_FPAR: Extra detail Quality for LAI (Leaf Area Index) and FPAR (Fraction of photosynthetically active radiation).
        - QUALITY_CONTROL_LAI_AND_FPAR: Quality for LAI (Leaf Area Index) and FPAR (Fraction of photosynthetically active radiation).
        - FPAIR_STANDARD_DEVIATION: Standard deviation of FPAR (Fraction of photosynthetically active radiation).
        - FPAIR: Fraction of photosynthetically active radiation (FPAIR).
        - LAI_STANDARD_DEVIATION: Standard deviation for LAI (Leaf Area Index).
        - LAI: Leaf area index (LAI).
        - ALL: all MCD15A3H bands.

    """
    EXTRA_QUALITY_CONTROL_LAI_AND_FPAR = 'FparExtra_QC'
    QUALITY_CONTROL_LAI_AND_FPAR = 'FparLai_QC'
    FPAIR_STANDARD_DEVIATION = 'FparStdDev_500m'
    FPAIR = 'Fpar_500m'
    LAI_STANDARD_DEVIATION = 'LaiStdDev_500m'
    LAI = 'Lai_500m'
    ALL = 'all'


@unique
@stringformat
class _BandsMCD19A3(Enum):
    """Bands available for the product MODIS/Terra+Aqua BRDF Model Parameters (MAIAC)
        8-Day L3 Global 1 km SIN Grid.

        frequency: 8-Day

        resolution: 1000-m

        - RTLS_GEOMETRIC_KERNEL_PARAMETER: RTLS geometric kernel parameter for bands 1-8.
        - RTLS_ISOTROPIC_KERNEL_PARAMETER: RTLS isotropic kernel parameter for bands 1-8.
        - RTLS_VOLUMETRIC_KERNEL_PARAMETER: RTLS volumetric kernel parameter for bands 1-8.
        - SURFACE_ALBEDO: Surface albedo for bands 1-8.
        - UPDATE_DAY_INTERVAL: Number of days since last update to the current day.
        - ALL: all MCD19A3 bands.

    """
    RTLS_GEOMETRIC_KERNEL_PARAMETER = 'Kgeo'
    RTLS_ISOTROPIC_KERNEL_PARAMETER = 'Kiso'
    RTLS_VOLUMETRIC_KERNEL_PARAMETER = 'Kvol'
    SURFACE_ALBEDO = 'Sur_albedo'
    UPDATE_DAY_INTERVAL = 'UpdateDay'
    ALL = 'all'


@unique
@stringformat
class _BandsMCD43A(Enum):
    """Bands available for the product MODIS/Terra+Aqua BRDF and Calculated Albedo (BRDF/MCD43A)
        16-Day L3 Global 500m SIN Grid.

        frequency: 16-Day

        resolution: 500-m

        - NIR_ALBEDO_ACTUAL: blue sky albedo nir.
        - NIR_ALBEDO_BLACK: black sky albedo nir.
        - NIR_ALBEDO_WHITE: white sky albedo nir.
        - SHORTWAVE_ALBEDO_ACTUAL: blue sky albedo shortwave.
        - SHORTWAVE_ALBEDO_BLACK: black sky albedo shortwave.
        - SHORTWAVE_ALBEDO_WHITE: white sky albedo shortwave.
        - VIS_ALBEDO_ACTUAL: blue sky albedo vis.
        - VIS_ALBEDO_BLACK: black sky albedo vis.
        - VIS_ALBEDO_WHITE: white sky albedo vis.
        - ALL: all MCD43A bands.

    """
    NIR_ALBEDO_ACTUAL = 'nir_actual'
    NIR_ALBEDO_BLACK = 'nir_black'
    NIR_ALBEDO_WHITE = 'nir_white'
    SHORTWAVE_ALBEDO_ACTUAL = 'shortwave_actual'
    SHORTWAVE_ALBEDO_BLACK = 'shortwave_black'
    SHORTWAVE_ALBEDO_WHITE = 'shortwave_white'
    VIS_ALBEDO_ACTUAL = 'vis_actual'
    VIS_ALBEDO_BLACK = 'vis_black'
    VIS_ALBEDO_WHITE = 'vis_white'
    ALL = 'all'


@unique
@stringformat
class _BandsMCD43A1(Enum):
    """Bands available for the product MODIS/Terra+Aqua BRDF/Albedo Model Parameters (BRDF)
        16-Day L3 Global 500m SIN Grid.

        frequency: 16-Day

        resolution: 500-m

        - BRDF_ALBEDO_MANDATORY_QUALITY_BAND_01: BDRF (Bidirectional Reflectance Distribution Function) and Albedo Band mandatory quality Band 1.
        - BRDF_ALBEDO_MANDATORY_QUALITY_BAND_02: BDRF (Bidirectional Reflectance Distribution Function) and Albedo Band mandatory quality Band 2.
        - BRDF_ALBEDO_MANDATORY_QUALITY_BAND_03: BDRF (Bidirectional Reflectance Distribution Function) and Albedo Band mandatory quality Band 3.
        - BRDF_ALBEDO_MANDATORY_QUALITY_BAND_04: BDRF (Bidirectional Reflectance Distribution Function) and Albedo Band mandatory quality Band 4.
        - BRDF_ALBEDO_MANDATORY_QUALITY_BAND_05: BDRF (Bidirectional Reflectance Distribution Function) and Albedo Band mandatory quality Band 5.
        - BRDF_ALBEDO_MANDATORY_QUALITY_BAND_06: BDRF (Bidirectional Reflectance Distribution Function) and Albedo Band mandatory quality Band 6.
        - BRDF_ALBEDO_MANDATORY_QUALITY_BAND_07: BDRF (Bidirectional Reflectance Distribution Function) and Albedo Band mandatory quality Band 7.
        - BRDF_ALBEDO_MANDATORY_QUALITY_NIR: BDRF (Bidirectional Reflectance Distribution Function) and Albedo Band mandatory quality NIR (near infrared).
        - BRDF_ALBEDO_MANDATORY_QUALITY_SHORTWAVE: BDRF (Bidirectional Reflectance Distribution Function) and Albedo Band mandatory quality shortwave.
        - BRDF_ALBEDO_MANDATORY_QUALITY_VIR: BDRF (Bidirectional Reflectance Distribution Function) and Albedo Band mandatory quality VIR (visible and infrared).
        - BRDF_ALBEDO_PARAMETERS_BAND_01: BDRF (Bidirectional Reflectance Distribution Function) and Albedo parameters Band 1.
        - BRDF_ALBEDO_PARAMETERS_BAND_02: BDRF (Bidirectional Reflectance Distribution Function) and Albedo parameters Band 2.
        - BRDF_ALBEDO_PARAMETERS_BAND_03: BDRF (Bidirectional Reflectance Distribution Function) and Albedo parameters Band 3.
        - BRDF_ALBEDO_PARAMETERS_BAND_04: BDRF (Bidirectional Reflectance Distribution Function) and Albedo parameters Band 4.
        - BRDF_ALBEDO_PARAMETERS_BAND_05: BDRF (Bidirectional Reflectance Distribution Function) and Albedo parameters Band 5.
        - BRDF_ALBEDO_PARAMETERS_BAND_06: BDRF (Bidirectional Reflectance Distribution Function) and Albedo parameters Band 6.
        - BRDF_ALBEDO_PARAMETERS_BAND_07: BDRF (Bidirectional Reflectance Distribution Function) and Albedo parameters Band 7.
        - BRDF_ALBEDO_PARAMETERS_NIR: BDRF (Bidirectional Reflectance Distribution Function) and Albedo parameters NIR (near infrared).
        - BRDF_ALBEDO_PARAMETERS_SHORTWAVE: BDRF (Bidirectional Reflectance Distribution Function) and Albedo parameters shortwave.
        - BRDF_ALBEDO_PARAMETERS_VIR: BDRF (Bidirectional Reflectance Distribution Function) and Albedo parameters VIR (visible and infrared).
        - ALL: all MCD43A1 bands.

    """
    BRDF_ALBEDO_MANDATORY_QUALITY_BAND_02 = 'BDRF_Albedo_Band_Mandatory_Quality_Band2'
    BRDF_ALBEDO_MANDATORY_QUALITY_BAND_03 = 'BDRF_Albedo_Band_Mandatory_Quality_Band3'
    BRDF_ALBEDO_MANDATORY_QUALITY_BAND_04 = 'BDRF_Albedo_Band_Mandatory_Quality_Band4'
    BRDF_ALBEDO_MANDATORY_QUALITY_BAND_05 = 'BDRF_Albedo_Band_Mandatory_Quality_Band5'
    BRDF_ALBEDO_MANDATORY_QUALITY_BAND_06 = 'BDRF_Albedo_Band_Mandatory_Quality_Band6'
    BRDF_ALBEDO_MANDATORY_QUALITY_BAND_07 = 'BDRF_Albedo_Band_Mandatory_Quality_Band7'
    BRDF_ALBEDO_MANDATORY_QUALITY_NIR = 'BDRF_Albedo_Band_Mandatory_Quality_nir'
    BRDF_ALBEDO_MANDATORY_QUALITY_SHORTWAVE = 'BDRF_Albedo_Band_Mandatory_Quality_shortwave'
    BRDF_ALBEDO_MANDATORY_QUALITY_VIR = 'BDRF_Albedo_Band_Mandatory_Quality_vis'
    BRDF_ALBEDO_PARAMETERS_BAND_01 = 'BRDF_Albedo_Parameters_Band1'
    BRDF_ALBEDO_PARAMETERS_BAND_02 = 'BRDF_Albedo_Parameters_Band2'
    BRDF_ALBEDO_PARAMETERS_BAND_03 = 'BRDF_Albedo_Parameters_Band3'
    BRDF_ALBEDO_PARAMETERS_BAND_04 = 'BRDF_Albedo_Parameters_Band4'
    BRDF_ALBEDO_PARAMETERS_BAND_05 = 'BRDF_Albedo_Parameters_Band5'
    BRDF_ALBEDO_PARAMETERS_BAND_06 = 'BRDF_Albedo_Parameters_Band6'
    BRDF_ALBEDO_PARAMETERS_BAND_07 = 'BRDF_Albedo_Parameters_Band7'
    BRDF_ALBEDO_PARAMETERS_NIR = 'BRDF_Albedo_Parameters_nir'
    BRDF_ALBEDO_PARAMETERS_SHORTWAVE = '"BRDF_Albedo_Parameters_shortwave'
    BRDF_ALBEDO_PARAMETERS_VIR = 'BRDF_Albedo_Parameters_vis'
    ALL = 'all'


@unique
@stringformat
class _BandsMCD43A4(Enum):
    """Bands available for the product MODIS/Terra+Aqua Nadir BRDF-Adjusted Reflectance (NBAR)
        Daily L3 Global 500 m SIN Grid.

        frequency: Daily

        resolution: 500-m

        - BRDF_ALBEDO_MANDATORY_QUALITY_BAND_01: BDRF (Bidirectional Reflectance Distribution Function) and Albedo Band mandatory quality Band 1.
        - BRDF_ALBEDO_MANDATORY_QUALITY_BAND_02: BDRF (Bidirectional Reflectance Distribution Function) and Albedo Band mandatory quality Band 2.
        - BRDF_ALBEDO_MANDATORY_QUALITY_BAND_03: BDRF (Bidirectional Reflectance Distribution Function) and Albedo Band mandatory quality Band 3.
        - BRDF_ALBEDO_MANDATORY_QUALITY_BAND_04: BDRF (Bidirectional Reflectance Distribution Function) and Albedo Band mandatory quality Band 4.
        - BRDF_ALBEDO_MANDATORY_QUALITY_BAND_05: BDRF (Bidirectional Reflectance Distribution Function) and Albedo Band mandatory quality Band 5.
        - BRDF_ALBEDO_MANDATORY_QUALITY_BAND_06: BDRF (Bidirectional Reflectance Distribution Function) and Albedo Band mandatory quality Band 6.
        - BRDF_ALBEDO_MANDATORY_QUALITY_BAND_07: BDRF (Bidirectional Reflectance Distribution Function) and Albedo Band mandatory quality Band 7.
        - NADIR_REFLECTANCE_BAND_01: nadir reflectance band 1.
        - NADIR_REFLECTANCE_BAND_02: nadir reflectance band 2.
        - NADIR_REFLECTANCE_BAND_03: nadir reflectance band 3.
        - NADIR_REFLECTANCE_BAND_04: nadir reflectance band 4.
        - NADIR_REFLECTANCE_BAND_05: nadir reflectance band 5.
        - NADIR_REFLECTANCE_BAND_06: nadir reflectance band 6.
        - NADIR_REFLECTANCE_BAND_07: nadir reflectance band 7.
        - ALL: all MCD43A4 bands.

    """
    BRDF_ALBEDO_MANDATORY_QUALITY_BAND_01 = 'BRDF_Albedo_Band_Mandatory_Quality_Band1'
    BRDF_ALBEDO_MANDATORY_QUALITY_BAND_02 = 'BRDF_Albedo_Band_Mandatory_Quality_Band2'
    BRDF_ALBEDO_MANDATORY_QUALITY_BAND_03 = 'BRDF_Albedo_Band_Mandatory_Quality_Band3'
    BRDF_ALBEDO_MANDATORY_QUALITY_BAND_04 = 'BRDF_Albedo_Band_Mandatory_Quality_Band4'
    BRDF_ALBEDO_MANDATORY_QUALITY_BAND_05 = 'BRDF_Albedo_Band_Mandatory_Quality_Band5'
    BRDF_ALBEDO_MANDATORY_QUALITY_BAND_06 = 'BRDF_Albedo_Band_Mandatory_Quality_Band6'
    BRDF_ALBEDO_MANDATORY_QUALITY_BAND_07 = 'BRDF_Albedo_Band_Mandatory_Quality_Band7'
    NADIR_REFLECTANCE_BAND_01 = 'Nadir_Reflectance_Band1'
    NADIR_REFLECTANCE_BAND_02 = 'Nadir_Reflectance_Band2'
    NADIR_REFLECTANCE_BAND_03 = 'Nadir_Reflectance_Band3'
    NADIR_REFLECTANCE_BAND_04 = 'Nadir_Reflectance_Band4'
    NADIR_REFLECTANCE_BAND_05 = 'Nadir_Reflectance_Band5'
    NADIR_REFLECTANCE_BAND_06 = 'Nadir_Reflectance_Band6'
    NADIR_REFLECTANCE_BAND_07 = 'Nadir_Reflectance_Band7'
    ALL = 'all'


@unique
@stringformat
class _BandsMCD64A1(Enum):
    """Bands available for the product MODIS/Terra+Aqua Burned Area (Burned Area)
        Monthly L3 Global 500 m SIN Grid.

        frequency: Monthly

        resolution: 500-m

        - BURN_DATE: ordinal day of burn (from 0 to 366).
        - BURN_DATE_UNCERTAINTY: uncertainty in day of burn.
        - FIRST_DAY_RELIABLE_CHANGE_DETECTION: first day of reliable change detection (from 0 to 366).
        - LAST_DAY_RELIABLE_CHANGE_DETECTION: last day of reliable change detection (from 0 to 366).
        - QUALITY_ASSURANCE = quality assurance indicators.
        - ALL: all MCD64A1 bands.

        """
    BURN_DATE = 'Burn_Date'
    BURN_DATE_UNCERTAINTY = 'Burn_Date_Uncertainty'
    FIRST_DAY_RELIABLE_CHANGE_DETECTION = 'First_Day'
    LAST_DAY_RELIABLE_CHANGE_DETECTION = 'Last_Day'
    QUALITY_ASSURANCE = 'QA'
    ALL = 'all'


# --------------------------------------------------------------
# BANDS: The Band class represents a container of enumerations.
# --------------------------------------------------------------


class Bands:
    """List of all available bands by product.

        **MODIS TERRA**:

        - MOD09A1: MODIS/Terra Surface Reflectance (SREF) 8-Day L3 Global 500m SIN Grid.
        - MOD11A2: MODIS/Terra Land Surface Temperature and Emissivity (LST) 8-Day L3 Global 1 km SIN Grid.
        - MOD13Q1: MODIS/Terra Vegetation Indices (NDVI/EVI) 16-Day L3 Global 250m SIN Grid.
        - MOD14A2: MODIS/Terra Thermal Anomalies/Fire (Fire) 8-Day L3 Global 1 km SIN Grid.
        - MOD15A2H: MODIS/Terra Leaf Area Index/FPAR (LAI/FPAR) 8-Day L4 Global 500 m SIN Grid.
        - MOD16A2: MODIS/Terra Net Evapotranspiration (ET) 8-Day L4 Global 500 m SIN Grid.
        - MOD17A2H: MODIS/Terra Gross Primary Productivity (GPP) 8-Day L4 Global 500 m SIN Grid.
        - MOD17A3HGF: MODIS/Terra Net Primary Production Gap-Filled (NPP) Yearly L4 Global 500 m SIN Grid.
        - MOD21A2: MODIS/Terra Land Surface Temperature/3-Band Emissivity (LSTE) 8-Day L3 Global 1 km SIN Grid.
        - MOD44B: MODIS/Terra Vegetation Continuous Fields (VCF) Yearly L3 Global 250 m SIN Grid.

        **MODIS AQUA**:

        - MYD09A1: MODIS/Aqua Surface Reflectance (SREF) 8-Day L3 Global 500m SIN Grid.
        - MYD11A2: MODIS/Aqua Land Surface Temperature and Emissivity (LST) 8-Day L3 Global 1 km SIN Grid.
        - MYD13Q1: MODIS/Aqua Vegetation Indices (NDVI/EVI) 16-Day L3 Global 250m SIN Grid.
        - MYD14A2: MODIS/Aqua Thermal Anomalies/Fire (Fire) 8-Day L3 Global 1 km SIN Grid.
        - MYD15A2H: MODIS/Aqua Leaf Area Index/FPAR (LAI/FPAR) 8-Day L4 Global 500 m SIN Grid.
        - MYD16A2: MODIS/Aqua Net Evapotranspiration (ET) 8-Day L4 Global 500 m SIN Grid.
        - MYD17A2H: MODIS/Aqua Gross Primary Productivity (GPP) 8-Day L4 Global 500 m SIN Grid.
        - MYD17A3HGF: MODIS/Aqua Net Primary Production Gap-Filled (NPP) Yearly L4 Global 500 m SIN Grid.
        - MYD21A2: MODIS/Aqua Land Surface Temperature/3-Band Emissivity (LSTE) 8-Day L3 Global 1 km SIN Grid.

        **MODIS TERRA and AQUA**:

        - MCD12Q1: MODIS/Terra+Aqua Land Cover Type (LC) Yearly L3 Global 500 m SIN Grid.
        - MCD12Q2: MODIS/Terra+Aqua Land Cover Dynamics (LCD) Yearly L3 Global 500 m SIN Grid.
        - MCD15A2H: MODIS/Terra+Aqua Leaf Area Index/FPAR (LAI/FPAR) 8-Day L4 Global 500 m SIN Grid.
        - MCD15A3H: MODIS/Terra+Aqua Leaf Area Index/FPAR (LAI/FPAR) 4-Day L4 Global 500 m SIN Grid.
        - MCD19A3: MODIS/Terra+Aqua BRDF Model Parameters (MAIAC) 8-Day L3 Global 1 km SIN Grid.
        - MCD43A: MODIS/Terra+Aqua BRDF and Calculated Albedo (BRDF/MCD43A) 16-Day L3 Global 500m SIN Grid.
        - MCD43A1: MODIS/Terra+Aqua BRDF/Albedo Model Parameters (BRDF) 16-Day L3 Global 500m SIN Grid.
        - MCD43A4: MODIS/Terra+Aqua Nadir BRDF-Adjusted Reflectance (NBAR) Daily L3 Global 500 m SIN Grid.
        - MCD64A1: MODIS/Terra+Aqua Burned Area (Burned Area) Monthly L3 Global 500 m SIN Grid.

    """

    # MODIS-Terra

    MOD13Q1: Enum = _BandsMOD13Q1
    MOD11A2: Enum = _BandsMOD11A2
    MOD09A1: Enum = _BandsMOD09A1
    MOD14A2: Enum = _BandsMOD14A2
    MOD15A2H: Enum = _BandsMOD15A2H
    MOD16A2: Enum = _BandsMOD16A2
    MOD17A2H: Enum = _BandsMOD17A2H
    MOD17A3HGF: Enum = _BandsMOD17A3HGF
    MOD21A2: Enum = _BandsMOD21A2
    MOD44B: Enum = _BandsMOD44B

    # MODIS-Aqua

    MYD09A1: Enum = _BandsMYD09A1
    MYD11A2: Enum = _BandsMYD11A2
    MYD13Q1: Enum = _BandsMYD13Q1
    MYD14A2: Enum = _BandsMYD14A2
    MYD15A2H: Enum = _BandsMYD15A2H
    MYD16A2: Enum = _BandsMYD16A2
    MYD17A2H: Enum = _BandsMYD17A2H
    MYD17A3HGF: Enum = _BandsMYD17A3HGF
    MYD21A2: Enum = _BandsMYD21A2

    # MODIS-Terra and Aqua

    MCD12Q1: Enum = _BandsMCD12Q1
    MCD12Q2: Enum = _BandsMCD12Q2
    MCD15A2H: Enum = _BandsMCD15A2H
    MCD15A3H: Enum = _BandsMCD15A3H
    MCD19A3: Enum = _BandsMCD19A3
    MCD43A: Enum = _BandsMCD43A
    MCD43A1: Enum = _BandsMCD43A1
    MCD43A4: Enum = _BandsMCD43A4
    MCD64A1: Enum = _BandsMCD64A1
