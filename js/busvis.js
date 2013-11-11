/**
 * @license See README.md in the repo for license information
 * https://github.com/jnu/busing
 */


// helpers
function dot(key) {
    return function(d) {
        return d[key];
    };
}

function val(key) {
    return function(d) {
        return d.value && d.value[d];
    };
}





/**
 * Init charts with dc.js
 * @param  {Error} error [description]
 * @param  {Array} rows  [description]
 */
function init() {
    var cf;
    var dims = {};
    var groups = window.groups = {};
    var charts = {
        country: countryChart,
        year: yearChart
    };

    // helpers
    function initChart(chartConstructor, key) {
        // dom containers are expected to have proper ids
        var selector = '#vis-' + key;
        return chartConstructor(selector)
            .dimension(dims[key])
            .group(groups[key]);
    }

    // charts
    function countryChart(key) {
        return initChart(dc.rowChart, key)
            .width(400)
            .height(200)
            .margins({top: 20, left: 10, right: 10, bottom: 20})
            .label(dot('key'))
            .title(dot('value'))
            .elasticX(true)
            .xAxis().ticks(4);
    }

    function yearChart(key) {
        return initChart(dc.bubbleChart, key)
            .width(600)
            .height(250)
            .x(d3.scale.linear().domain([1900, 2015]))
            .elasticY(true)
            .keyAccessor(dot('key'))
            .radiusValueAccessor(val('population'))
            .valueAccessor(val('count'));

    }

    // returns callback 
    return function(error, rows) {
        window.rows = rows;
        var cfVars = {
            country : 'country',
            method : 'fare_method',
            otherTransit: 'has_other_transit',
            year: 'founded'
        };
        cf = crossfilter(rows);

        // create crossfilter dimensions and groups
        for (var cfVar in cfVars) {
            var csvCol = cfVars[cfVar];
            var dim = dims[cfVar] = cf.dimension(dot(csvCol));
            groups[cfVar] = dim.group();
        }

        // apply special reductions as necessary to groups
        groups.year.reduce(function add(p, v) {
            ++p.count;
            p.population += v.population;
            return p;
        }, function remove(p, v) {
            --p.count;
            p.population -= v.population;
            return p;
        }, function initial() {
            return {
                count: 0,
                population: 0
            };
        });

        // invoke all charts
        for (var c in charts) {
            charts[c] = charts[c](c);
        }

        // render
        dc.renderAll();
    };
}


/**
 * Row formatter
 * @param  {DataRow} d  An object representing a row of a CSV
 * @return {Object}     The formatted row object
 */
function formatRows(d) {
    d.population = +d.population;
    d.fleet_size = +d.fleet_size;
    d.load = +d.load;
    d.capacity = +d.capacity;
    d.founded = +d.founded;
    d.has_other_transit = d.has_other_transit == 'Y';
    d.lat = +d.lat;
    d.long = +d.long;
    return d;
}


// init
$(function() {
    d3.csv('../data/busing.csv', formatRows, init());
});