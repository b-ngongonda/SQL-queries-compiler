use openmrs_warehouse;

set @endDate='2024-10-31';

set @location='neno district hospital';

call  create_last_art_outcome_at_facility(@endDate,@location);

select location, count(*) from last_facility_outcome
where state='on antiretrovirals'