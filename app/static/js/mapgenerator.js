function mapgenerate(data){
    console.log(data);
    var col = 'students';
    var sliderValue = 2014;
    var div = d3.select("#mainWrapper");
    var svg = div.append("svg")
        .attr("id", "map13")
        .attr("height", 500)
        .attr("width", 960);
    var localV = valueIs();
    letter = 'Students Enrolled';
    //colorMap13(localV,letter);
    d3.select('#variableText').text(letterIs());
    map = d3.geomap.choropleth()
        .geofile('../static/d3-geomap/topojson/countries/USA.json')
        .colors(colorbrewer.Reds[9])
        .projection(d3.geo.albersUsa)
        .column(col)
        .unitId("FIPS")
        .scale(1000)
        .legend(true);
    var dataArray = [];
    //for(var i=2014; i<2015; i++) {
        var newD = [];
        var count = 0;

        for(var prop in data) {
            console.log(prop);
                newD.push(data[prop]);

        }
        dataArray = newD;
    //}
    console.log(dataArray);

    data1  = {}
    d3.select("#map13")
        .datum(dataArray)
        .call(map.draw, map);

}

function valueIs() {
    //console.log(sliderValue);
    return 2014;
}
function letterIs() {
    console.log('letter is: ' + letter);
    return letter;
}