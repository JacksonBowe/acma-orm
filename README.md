# ACMA ORM

ACMA ORM is a Python library designed to quickly import the AMCA specrta_rrl data dump into a termporary SQLite database and provide an intuitive Peewee ORM interface for querying records. This library is intended to be used locally for data analytics.

## Features

-   **Bulk CSV Import**: Efficiently load ACMA CSV dumps into a SQLite database using Pandas
-   **ORM Interface**: Query your data using Peewee ORM. Examples provided below

## Installation and Usage

```sh
pip install acma-orm
```

Download [spectra_rrl](https://web.acma.gov.au/rrl-updates/spectra_rrl.zip) and extract all files into `path/to/spectra_rrl_directory` (wherever you want, as long as Python can find it)

Once installed use like below:

```py
from acma_orm.importer import import_all_data
from acma_orm.models import Licence, Client
from playhouse.shortcuts import model_to_dict

# Import your CSV dump (ensure your CSV files are in the specified folder)
import_all_data("path/to/spectra_rrl_directory")

# Query licences for a specific client.
query = (Licence
         .select(Licence)
         .join(Client)
         .where((Client.licencee == "TELSTRA LIMITED") &
                (Client.trading_name == "Telstra - Commerical Engineering - Spectrum Strategy")))
for licence in query:
    print(model_to_dict(licence, recurse=True))

```

## Contributing

1. **Install UV**:

    ```sh
    pip install uv
    ```

2. Close the Repo and sync environment

    ```sh
    git clone https://github.com/jacksonbowe/acma-orm.git
    cd acma-orm

    uv sync
    ```

3. Download [spectra_rrl](https://web.acma.gov.au/rrl-updates/spectra_rrl.zip) and extract all files into `examples/spectral_rrl`

4. Run Example Scripts:  
   The `examples/` directory contains individual scripts that demonstrate various query types. For instance, run:

    ```sh
    uv run examples/init.py
    uv run examples/simple_query.py
    uv run examples/join_query.py
    uv run examples/aggregation_query.py
    uv run examples/complex_query.py
    ```

## Project Structure

```
acma-orm/
├── pyproject.toml            # Build configuration for UV (and PyPI metadata)
├── README.md                # This file
├── LICENSE                  # License file (MIT License)
├── examples/                # Example scripts demonstrating package usage
│   ├── spectra_rrl/
│   │   ├── <put_spectra_rrl_data_in_here>
│   ├── init.py              # Run me first
│   ├── simple_query.py
│   ├── join_query.py
│   ├── aggregation_query.py
│   └── complex_query.py
├── src/
│   └── acma_orm/            # Package source code
│       ├── __init__.py      # Exposes package API (including enable_debug_logging)
│       ├── database.py      # Database connection and initialization logic
│       ├── importer.py      # Functions to import CSV data
│       └── models.py        # Peewee ORM model definitions
```

## License

This project is licensed under the MIT License

## GPT Prompt to Bootstrap Context

If you're like me and you want ChatGPT to write your queries you can either copy the entire contents of `models.py` into the session, or you can use the summarised version below.

<details>
    <summary>Prompt</summary>

    You have access to the following Peewee models and their relationships. Use this information to construct queries as needed:

    Models:
    LicensingArea(licensing_area_id, description)
    Site(site_id, latitude, longitude, name, state, licensing_area, postcode, site_precision, elevation, hcis_l2)
    Satellite(sa_id, sa_sat_name, sa_sat_long_nom, sa_sat_incexc, sa_sat_geo_pos, sa_sat_merit_g_t)
    ReportsTextBlock(rtb_item, rtb_category, rtb_description, rtb_start_date, rtb_end_date, rtb_text)
    NatureOfService(code, description)
    LicenceStatus(status, status_text)
    IndustryCat(cat_id, description, name)
    FeeStatus(fee_status_id, fee_status_text)
    ClientType(type_id, name)
    Client(client_no, licencee, trading_name, acn, abn, postal_street, postal_suburb, postal_state, postal_postcode, cat_id, client_type, fee_status_id)
    LicenceService(sv_id, sv_name)
    LicenceSubservice(ss_id, sv_sv_id, ss_name)
    BslArea(area_code, area_name)
    Bsl(bsl_no, medium_category, region_category, community_interest, bsl_state, date_commenced, on_air_id, call_sign, ibl_target_area, area_code, reference)
    Licence(licence_no, client, sv_id, ss_id, licence_type_name, licence_category_name, date_issued, date_of_effect, date_of_expiry, status, status_text, ap_id, ap_prj_ident, ship_name, bsl, awl_type)
    AntennaPolarity(polarisation_code, polarisation_text)
    AccessArea(area_id, area_code, area_name, area_category)
    Antenna(antenna_id, gain, front_to_back, h_beamwidth, v_beamwidth, band_min_freq, band_min_freq_unit, band_max_freq, band_max_freq_unit, antenna_size, antenna_type, model, manufacturer)
    ClassOfStation(code, description)
    DeviceDetail(sdd_id, licence, device_registration_identifier, former_device_identifier, authorisation_date, certification_method, group_flag, site_radius, frequency, bandwidth, carrier_freq, emission, device_type, transmitter_power, transmitter_power_unit, site, antenna, polarisation, azimuth, height, tilt, feeder_loss, level_of_protection, eirp, eirp_unit, licence_service, licence_subservice, efl_id, efl_freq_ident, efl_system, leqd_mode, receiver_threshold, area_area_id, call_sign, area_description, ap_id, class_of_station_code, supplimental_flag, eq_freq_range_min, eq_freq_range_max, nature_of_service, hours_of_operation, satellite, related_efl_id, eqp_id, antenna_multi_mode, power_ind, lpon_center_longitude, lpon_center_latitude, tcs_id, tech_spec_id, dropthrough_id, station_type, station_name)
    AuthSpectrumFreq(id, licence, area_code, area_name, lw_frequency_start, lw_frequency_end, up_frequency_start, up_frequency_end)
    AuthSpectrumArea(id, licence_no, area_code, area_name, area_description)
    ApplicTextBlock(aptb_id, aptb_table_prefix, aptb_table_id, licence_no, aptb_description, aptb_category, aptb_text, aptb_item)
    AntennaPattern(id, antenna, az_type, angle_ref, angle, attenuation)
    Key Relationships:
    Site.licensing_area → LicensingArea.licensing_area_id
    Client.cat_id → IndustryCat.cat_id
    Client.client_type → ClientType.type_id
    Client.fee_status_id → FeeStatus.fee_status_id
    LicenceSubservice.sv_sv_id → LicenceService.sv_id
    Bsl.area_code → BslArea.area_code
    Licence.client → Client.client_no
    Licence.sv_id → LicenceService.sv_id
    Licence.ss_id → LicenceSubservice.ss_id
    Licence.status → LicenceStatus.status
    DeviceDetail.site → Site.site_id
    DeviceDetail.antenna → Antenna.antenna_id
    DeviceDetail.polarisation → AntennaPolarity.polarisation_code
    DeviceDetail.area_area_id → AccessArea.area_id
    DeviceDetail.class_of_station_code → ClassOfStation.code
    DeviceDetail.nature_of_service → NatureOfService.code
    DeviceDetail.sa_id → Satellite.sa_id
    AuthSpectrumFreq.licence → Licence.licence_no
    AuthSpectrumArea.licence_no → Licence.licence_no
    ApplicTextBlock.licence_no → Licence.licence_no
    AntennaPattern.antenna → Antenna.antenna_id
    Notes:
    DeviceDetail.device_type is either 'T' (Transmitter) or 'R' (Receiver).
    LicenceStatus.status and LicenceStatus.status_text represent status codes and their human-readable texts.
    Antenna.band_min_freq and Antenna.band_max_freq include units stored in band_min_freq_unit and band_max_freq_unit.
    Site.site_precision indicates the precision of the site coordinates.
    Licence.date_of_expiry can be null, indicating an active or perpetual license.
    Example Request:
    "Find all sites in a specific licensing area with latitude and longitude information."

</details>
