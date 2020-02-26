# Famine Project Backend
## Installation/usage
This needs python 3 along with the following modules:
* Pystan: https://pystan.readthedocs.io/en/latest/getting_started.html
* numpy, pandas
* flask, flask-restful

To use simply run the `server.py` script from the src directory

## Endpoints
### Data
* GET `/data/all` - Returns all data and predicted data for every region
* GET `/data/region/<region>` - Returns all data and predicted data for a given region
* GET `/data/region_list` - Returns list of all regions and fitted regions

### Predictions
```json
{
  "changes" : [
    {
      "source"  : "Maize (white) - Borama | Awdal - Fatalities due to Conflict | ...",
      "year"    : 2015,
      "month"   : 5,
      "column"  : "Price | Temperature | Fatalities",
      "value"   : 123.456
    }, ...
  ]
}
```

* GET `/prediction/summary` - Returns predictions for every region (no changes)
* GET `/prediction/region/<region>` -  Returns predictions for a specific region (no changes)
* POST `/prediction/region/<region>` - Returns predictions for a specific region with the specified changes array as defined above
    * Within the changes list, `source` refers to the feature name, that is the key to a given data frame returned by `/data/` endpoints
        * These names can be found in the `_feature_names list`
    * The column field specifies the type of data being changed
        * Food data - "Price"
        * Temperature data - "Temperature"
        * Conflict data - "Fatalities"
        * The mapping from feature names to columns can be found in the `_value_columns` list