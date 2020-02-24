# Famine Project Backend
## Installation/usage
This needs python 3 along with the following modules:
* Pystan: https://pystan.readthedocs.io/en/latest/getting_started.html
* numpy, pandas
* flask, flask-restful

To use simply run the `server.py` script from the src directory

## Endpoints
### Data
* `/data/all` - Returns all data and predicted data for every region
* `/data/region/<region>` - Returns all data and predicted data for a given region
* `/data/region_list` - Returns list of all regions and fitted regions