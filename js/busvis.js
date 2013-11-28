/**
 * @license See README.md in the repo for license information
 * https://github.com/jnu/busing
 */


// helpers
function dot() {
    var args = arguments;
    return function(d) {
        function _dot(v, args) {
            if (!(args && args.length)) return v;
            else return _dot(v[args[0]], Array.prototype.slice.call(args, 1));
        }
        return _dot(d, args);
    };
}

function val(key) {
    return function(d) {
        return d.value && d.value[d];
    };
}

function nest(f) {
    return function(d) {
        return f(d);
    };
}

function fixWidth(selector) {
    var selection = d3.selectAll(selector);
    var node = selection.node();
    var $node = $(node);
    var $parent = $node.parent();

    return function() {
        $node.hide();
        var targetWidth = $parent.width();
        $node.width(targetWidth).show();
        $node.trigger({
            type: 'update',
            width: targetWidth,
            height: $node.height()
        });
    };
} 

function project(projector) {
    var projection = projector();
    return function(chart, width, height) {
        var node = chart.anchor();
        var $node = $(node);
        width = (width === undefined) ? $node.parent().width() : width;
        height = (height === undefined) ? chart.height() : height;

        return chart
            .projection(projection.translate([width / 2, height / 2]));
    };
}



/**
 * Init charts with dc.js
 * @param  {Error} error [description]
 * @param  {Array} rows  [description]
 */
function init(opts) {
    var cf;
    var dims = {};
    var groups = {};
    // map chart name to [type, dim]
    var charts = window.charts = {
        country: [countryChart, 'country'],
        year: [yearChart, 'year'],
        map: [worldMap, 'country']
    };
    var worldJson = opts.worldJson;
    var $window = $(window);

    // helpers
    function initChart(chartConstructor, key, dim) {
        // dom containers are expected to have proper ids
        var selector = '#vis-' + key;
        $window.resize(fixWidth(selector));
        return chartConstructor(selector)
            .dimension(dims[dim])
            .group(groups[dim]);
    }

    // charts
    function countryChart(key, dim) {
        return initChart(dc.rowChart, key, dim)
            .margins({top: 20, left: 10, right: 10, bottom: 20})
            .height(250)
            .label(dot('key'))
            .title(dot('value'))
            .elasticX(true)
            .xAxis().ticks(4);
    }

    function yearChart(key, dim) {
        return initChart(dc.bubbleChart, key, dim)
            .height(250)
            .x(d3.scale.linear().domain([1900, 2015]))
            .elasticY(true)
            .keyAccessor(dot('key'))
            .radiusValueAccessor(val('population'))
            .valueAccessor(val('count'));
    }

    function worldMap(key, dim) {
        var chart = initChart(dc.geoChoroplethChart, key, dim)
            .height(400)
            .overlayGeoJson(worldJson.features, "countries", dot('properties', 'name'));
        var projector = project(d3.geo.equirectangular);
        $(chart.anchor()).on('update', function(e) {
            projector(chart, e.width, e.height);
        });
        return projector(chart);
    }

    // returned function is actually init logic 
    return function(error, rows) {
        // map of crossfilter vars to csv column headers
        var cfVars = {
            country : 'country',
            method : 'fare_method',
            otherTransit: 'has_other_transit',
            year: 'founded'
        };
        cf = crossfilter(rows);

        // create crossfilter dimensions and groups
        _(cfVars).map(function(csvCol, cfVar) {
            var dim = dims[cfVar] = cf.dimension(dot(csvCol));
            groups[cfVar] = dim.group();
        });

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
        _(charts).map(function(vars, key) {
            charts[key] = vars[0](key, vars[1]);
        });

        // render
        var doRender = function() { dc.renderAll(); };
        $window.resize(_.debounce(doRender, 150));
        doRender();
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
    d3.json('../data/world.geojson', function(mapData) {
        var opts = {
            worldJson: mapData
        };

        d3.csv('../data/busing.csv', formatRows, init(opts));
    });
});