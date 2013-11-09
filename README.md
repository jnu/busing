# Urban Busing Data and Visualization

## What

This project aims to collect, typologize, and visualize data pertaining to urban bus systems across the world.

## Why

Becuase I've taken a lot of buses in a lot of cities across the globe and they always make me anxious. I never know how to pay, whether I'll get fined for not paying, or whether my sojourn will involve getting accosted by a babushka with a change purse.

## How

### Data

I'd love help collecting data, and it's very easy to do! All you need to do is open [this Google Doc](https://docs.google.com/spreadsheet/ccc?key=0AsnHpWihusbxdHY1NmpnZ2Q0bllNX3pXY2dFMVRFYWc&usp=sharing) and start filling in empty cells. There is a world full of cities with bus systems, and most of them are not entered yet, so feel free to append new cities from your own experience or knowledge.

### Code

Feel free to fork this repo and help out with the visualizations or data-slinging stuff.

The visualization aspect uses [d3](https://github.com/mbostock/d3) and [crossfilter](https://github.com/square/crossfilter) and it gets deployed on [my website](http://joenoodles.com/static/busing/) occasionally.

The data-slinging side connects to the Google Doc via the [Google Data Python Library](https://developers.google.com/gdata/articles/python_client_lib) every once in a while and compiles the data there into JSON for use in the Javascript stuff. There is also a geocoding tool that implements [server-side geocoding via Google's API](https://developers.google.com/maps/articles/geocodestrat) to resolve the human-readable location names from the spreadsheet into mappable coordinates. This is only run when necessary during the compilation of JSON data from the spreadsheet, and geocode results are saved in the spreadsheet.

## Who

Started for fun and for free by Joe Nudell, (c) 2013. Released under the MIT License.