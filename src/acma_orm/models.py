from datetime import date

from peewee import (
    Model,
    CharField,
    DateField,
    ForeignKeyField,
    IntegerField,
    FloatField,
    BigIntegerField,
    AutoField,
    SqliteDatabase,
    TextField,
)

# Initialize the SQLite database (filename can be configured later)
db = SqliteDatabase("acma.db")


class BaseModel(Model):
    class Meta:
        database = db


# 1. site.csv → Site
class Site(BaseModel):
    site_id = IntegerField(primary_key=True)  # SITE_ID
    latitude = FloatField(null=True)
    longitude = FloatField(null=True)
    name = CharField(null=True)
    state = CharField(null=True)
    # LICENSING_AREA_ID references licencing_area.csv; see LicencingArea model below.
    licensing_area = ForeignKeyField(
        "LicencingArea", field="licensing_area_id", null=True, backref="sites"
    )
    postcode = CharField(null=True)
    site_precision = CharField(null=True)
    elevation = FloatField(null=True)
    hcis_l2 = CharField(null=True)


# 2. satellite.csv → Satellite
class Satellite(BaseModel):
    sa_id = IntegerField(primary_key=True)  # SA_ID
    sa_sat_name = CharField(null=True)
    sa_sat_long_nom = CharField(null=True)  # Could be numeric but stored as text here
    sa_sat_incexc = CharField(null=True)
    sa_sat_geo_pos = CharField(null=True)
    sa_sat_merit_g_t = CharField(null=True)


# 3. reports_text_block.csv → ReportsTextBlock
class ReportsTextBlock(BaseModel):
    rtb_item = CharField(primary_key=True)  # RTB_ITEM
    rtb_category = CharField(null=True)
    rtb_description = CharField(null=True)
    rtb_start_date = DateField(null=True)
    rtb_end_date = DateField(null=True)
    rtb_text = TextField(null=True)


# 4. nature_of_service.csv → NatureOfService
class NatureOfService(BaseModel):
    code = CharField(primary_key=True)  # CODE
    description = CharField(null=True)


# 5. licencing_area.csv → LicencingArea
class LicencingArea(BaseModel):
    licensing_area_id = IntegerField(primary_key=True)  # LICENSING_AREA_ID
    description = CharField(null=True)


# 6. licence.csv → Licence
class Licence(BaseModel):
    licence_no = CharField(primary_key=True)  # LICENCE_NO
    # CLIENT_NO references client.csv (defined in Client below)
    client = ForeignKeyField("Client", field="client_no", null=True, backref="licences")
    # SV_ID references licence_service.csv (see LicenceService below)
    sv_id = ForeignKeyField(
        "LicenceService", field="sv_id", null=True, backref="licences"
    )
    # SS_ID references licence_subservice.csv (see LicenceSubservice below)
    ss_id = ForeignKeyField(
        "LicenceSubservice", field="ss_id", null=True, backref="licences"
    )
    licence_type_name = CharField(null=True)
    licence_category_name = CharField(null=True)
    date_issued = DateField(null=True)
    date_of_effect = DateField(null=True)
    date_of_expiry = DateField(null=True)
    # STATUS and STATUS_TEXT might also be modeled as a foreign key to LicenceStatus
    status = CharField(null=True)
    status_text = CharField(null=True)
    ap_id = CharField(null=True)
    ap_prj_ident = CharField(null=True)
    ship_name = CharField(null=True)
    # BSL_NO references bsl.csv (see Bsl below)
    bsl_no = ForeignKeyField("Bsl", field="bsl_no", null=True, backref="licences")


# 7. licence_subservice.csv → LicenceSubservice
class LicenceSubservice(BaseModel):
    ss_id = IntegerField(primary_key=True)  # SS_ID
    # SV_SV_ID references licence_service.csv
    sv_sv_id = ForeignKeyField(
        "LicenceService", field="sv_id", null=True, backref="subservices"
    )
    ss_name = CharField(null=True)


# 8. licence_status.csv → LicenceStatus
class LicenceStatus(BaseModel):
    status = CharField(primary_key=True)  # STATUS
    status_text = CharField(null=True)


# 9. licence_service.csv → LicenceService
class LicenceService(BaseModel):
    sv_id = IntegerField(primary_key=True)  # SV_ID
    sv_name = CharField(null=True)


# 10. industry_cat.csv → IndustryCat
class IndustryCat(BaseModel):
    cat_id = IntegerField(primary_key=True)  # CAT_ID
    description = CharField(null=True)
    name = CharField(null=True)


# 11. fee_status.csv → FeeStatus
class FeeStatus(BaseModel):
    fee_status_id = IntegerField(primary_key=True)  # FEE_STATUS_ID
    fee_status_text = CharField(null=True)


# 12. device_details.csv → DeviceDetail
class DeviceDetail(BaseModel):
    sdd_id = BigIntegerField(primary_key=True)  # SDD_ID
    # LICENCE_NO references Licence
    licence = ForeignKeyField(
        Licence, field="licence_no", null=True, backref="device_details"
    )
    device_registration_identifier = CharField(null=True)
    former_device_identifier = CharField(null=True)
    authorisation_date = DateField(null=True)
    certification_method = CharField(null=True)
    group_flag = CharField(null=True)
    site_radius = FloatField(null=True)
    frequency = BigIntegerField(null=True)
    bandwidth = BigIntegerField(null=True)
    carrier_freq = BigIntegerField(null=True)
    emission = CharField(null=True)
    device_type = CharField(null=True)
    transmitter_power = FloatField(null=True)
    transmitter_power_unit = CharField(null=True)
    # SITE_ID references Site
    site = ForeignKeyField(Site, field="site_id", null=True, backref="device_details")
    # ANTENNA_ID references Antenna (defined below)
    antenna = ForeignKeyField(
        "Antenna", field="antenna_id", null=True, backref="device_details"
    )
    polarisation = CharField(null=True)
    azimuth = FloatField(null=True)
    height = FloatField(null=True)
    tilt = FloatField(null=True)
    feeder_loss = FloatField(null=True)
    level_of_protection = CharField(null=True)
    eirp = FloatField(null=True)
    eirp_unit = CharField(null=True)
    # SV_ID and SS_ID also reference LicenceService and LicenceSubservice respectively
    licence_service = ForeignKeyField(
        LicenceService, field="sv_id", null=True, backref="device_details"
    )
    licence_subservice = ForeignKeyField(
        LicenceSubservice, field="ss_id", null=True, backref="device_details"
    )
    efl_id = CharField(null=True)
    efl_freq_ident = CharField(null=True)
    efl_system = CharField(null=True)
    leqd_mode = CharField(null=True)
    receiver_threshold = FloatField(null=True)
    # AREA_AREA_ID is left as an IntegerField; it could be linked to AccessArea if desired.
    area_area_id = IntegerField(null=True)
    call_sign = CharField(null=True)
    area_description = CharField(null=True)
    ap_id = CharField(null=True)
    # CLASS_OF_STATION_CODE references ClassOfStation (see below)
    class_of_station_code = ForeignKeyField(
        "ClassOfStation", field="code", null=True, backref="device_details"
    )
    supplimental_flag = CharField(null=True)
    eq_freq_range_min = FloatField(null=True)
    eq_freq_range_max = FloatField(null=True)
    # NATURE_OF_SERVICE_ID references NatureOfService
    nature_of_service = ForeignKeyField(
        NatureOfService, field="code", null=True, backref="device_details"
    )
    hours_of_operation = CharField(null=True)
    # SA_ID references Satellite
    satellite = ForeignKeyField(
        Satellite, field="sa_id", null=True, backref="device_details"
    )
    related_efl_id = CharField(null=True)
    eqp_id = CharField(null=True)
    antenna_multi_mode = CharField(null=True)
    power_ind = CharField(null=True)
    lpon_center_longitude = FloatField(null=True)
    lpon_center_latitude = FloatField(null=True)
    tcs_id = CharField(null=True)
    tech_spec_id = CharField(null=True)
    dropthrough_id = CharField(null=True)
    station_type = CharField(null=True)
    station_name = CharField(null=True)


# 13. client.csv → Client
class Client(BaseModel):
    client_no = IntegerField(primary_key=True)  # CLIENT_NO
    licencee = CharField(null=True)
    trading_name = CharField(null=True)
    acn = CharField(null=True)
    abn = CharField(null=True)
    postal_street = CharField(null=True)
    postal_suburb = CharField(null=True)
    postal_state = CharField(null=True)
    postal_postcode = CharField(null=True)
    # CAT_ID references IndustryCat
    industry_cat = ForeignKeyField(
        IndustryCat, field="cat_id", null=True, backref="clients"
    )
    # CLIENT_TYPE_ID references ClientType (see below)
    client_type = ForeignKeyField(
        "ClientType", field="type_id", null=True, backref="clients"
    )
    # FEE_STATUS_ID references FeeStatus
    fee_status = ForeignKeyField(
        FeeStatus, field="fee_status_id", null=True, backref="clients"
    )


# 14. client_type.csv → ClientType
class ClientType(BaseModel):
    type_id = IntegerField(primary_key=True)  # TYPE_ID
    name = CharField(null=True)


# 15. class_of_station.csv → ClassOfStation
class ClassOfStation(BaseModel):
    code = CharField(primary_key=True)  # CODE
    description = CharField(null=True)


# 16. bsl.csv → Bsl
class Bsl(BaseModel):
    bsl_no = IntegerField(primary_key=True)  # BSL_NO
    medium_category = CharField(null=True)
    region_category = CharField(null=True)
    community_interest = CharField(null=True)
    bsl_state = CharField(null=True)
    date_commenced = DateField(null=True)
    on_air_id = CharField(null=True)
    call_sign = CharField(null=True)
    ibl_target_area = CharField(null=True)
    # AREA_CODE might be linked to BslArea below
    area_code = CharField(null=True)
    reference = CharField(null=True)


# 17. bsl_area.csv → BslArea
class BslArea(BaseModel):
    area_code = CharField(primary_key=True)  # AREA_CODE
    area_name = CharField(null=True)


# 18. auth_spectrum_freq.csv → AuthSpectrumFreq
class AuthSpectrumFreq(BaseModel):
    # Using a surrogate primary key; composite keys can be set up via Meta.unique_together if needed.
    id = AutoField()
    licence = ForeignKeyField(
        Licence, field="licence_no", null=True, backref="auth_spectrum_freqs"
    )
    area_code = CharField(null=True)
    area_name = CharField(null=True)
    lw_frequency_start = BigIntegerField(null=True)
    lw_frequency_end = BigIntegerField(null=True)
    up_frequency_start = BigIntegerField(null=True)
    up_frequency_end = BigIntegerField(null=True)


# 19. auth_spectrum_area.csv → AuthSpectrumArea
class AuthSpectrumArea(BaseModel):
    id = AutoField()
    licence = ForeignKeyField(
        Licence, field="licence_no", null=True, backref="auth_spectrum_areas"
    )
    area_code = CharField(null=True)
    area_name = CharField(null=True)
    area_description = CharField(null=True)


# 20. applic_text_block.csv → ApplicTextBlock
class ApplicTextBlock(BaseModel):
    aptb_id = BigIntegerField(primary_key=True)  # APTB_ID
    aptb_table_prefix = CharField(null=True)
    aptb_table_id = CharField(null=True)
    licence = ForeignKeyField(
        Licence, field="licence_no", null=True, backref="applic_text_blocks"
    )
    aptb_description = CharField(null=True)
    aptb_category = CharField(null=True)
    aptb_text = TextField(null=True)
    aptb_item = CharField(null=True)


# 21. antenna.csv → Antenna
class Antenna(BaseModel):
    antenna_id = IntegerField(primary_key=True)  # ANTENNA_ID
    gain = FloatField(null=True)
    front_to_back = FloatField(null=True)
    h_beamwidth = FloatField(null=True)
    v_beamwidth = FloatField(null=True)
    band_min_freq = FloatField(null=True)
    band_min_freq_unit = CharField(null=True)
    band_max_freq = FloatField(null=True)
    band_max_freq_unit = CharField(null=True)
    antenna_size = FloatField(null=True)
    antenna_type = CharField(null=True)
    model = CharField(null=True)
    manufacturer = CharField(null=True)


# 22. antenna_polarity.csv → AntennaPolarity
class AntennaPolarity(BaseModel):
    polarisation_code = CharField(primary_key=True)  # POLARISATION_CODE
    polarisation_text = CharField(null=True)


# 23. antenna_pattern.csv → AntennaPattern
class AntennaPattern(BaseModel):
    id = AutoField()
    antenna = ForeignKeyField(Antenna, field="antenna_id", backref="patterns")
    az_type = CharField(null=True)
    angle_ref = FloatField(null=True)
    angle = FloatField(null=True)
    attenuation = FloatField(null=True)


# 24. access_area.csv → AccessArea
class AccessArea(BaseModel):
    area_id = IntegerField(primary_key=True)  # AREA_ID
    area_code = CharField(null=True)
    area_name = CharField(null=True)
    area_category = CharField(null=True)


# (Optional) Create tables in the database
if __name__ == "__main__":
    db.connect()
    db.create_tables(
        [
            Site,
            Satellite,
            ReportsTextBlock,
            NatureOfService,
            LicencingArea,
            Licence,
            LicenceSubservice,
            LicenceStatus,
            LicenceService,
            IndustryCat,
            FeeStatus,
            DeviceDetail,
            Client,
            ClientType,
            ClassOfStation,
            Bsl,
            BslArea,
            AuthSpectrumFreq,
            AuthSpectrumArea,
            ApplicTextBlock,
            Antenna,
            AntennaPolarity,
            AntennaPattern,
            AccessArea,
        ]
    )
    print("Tables created successfully.")
