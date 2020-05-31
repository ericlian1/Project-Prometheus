// import L from 'leaflet';
// import 'leaflet/dist/leaflet.css';
// import styled from 'styled-components';
// import county_data from './gz_2010_us_050_00_500k';
// import corona_cases from './jhu_covid19_filled.csv';

// import { geoJSON } from "leaflet";

var mymap = L.map('interactive-map').setView([39.0119, -96.4842], 4);
var mapboxAccessToken = 'pk.eyJ1IjoiZ2dhcmZpbmsiLCJhIjoiY2thc25uOGVvMDBydTJxbjQ1YnFiZ3lnMCJ9.9sEk0vjedqQplRO3bx-L8w';
var covid_deaths;
var geoJSON;
//var county_data = $.get("https://eric.clst.org/assets/wiki/uploads/Stuff/gz_2010_us_050_00_500k.json");

//TO USE THE JSON: JUST REFERENCE county_data

//getting the jhu data now:
// Papa.parse('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/05-29-2020.csv', {
//     download: true,
//     step: function(result) {
//         alert()
//     }
// });

function getColor(d) {
    var ca = ['#d73027','#f46d43','#fdae61','#fee090','#ffffbf','#e0f3f8','#abd9e9','#74add1','#4575b4'];
    return d > 2 ? ca[0]: 
           d > 1.75  ? ca[1]:
           d > 1.5  ? ca[2]:
           d > 1.25    ? ca[3]:
           d > 1    ? ca[4]:
           d > .75    ? ca[5]:
           d > .5    ? ca[6]:
           d > 0.25     ? ca[7]:
                       ca[8];
}

function style(feature) {
    return {
        fillColor: getColor(feature.properties.index),
        weight: .5,
        opacity: 1,
        color: 'white',
        fillOpacity: 0.7
    };
}

//defines what happens on mouseover and mouseout
function highlightFeature(e) {
    var layer = e.target;

    layer.setStyle({
        weight: 4,
        color: '#ffffff',
        fillOpacity: 0.7
    });

    if(!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
        layer.bringToFront();
    }
}

function resetHighlight(e) {
    geoJSON.resetStyle(e.target);
}

function onClickSettings(e) {
    mymap.fitBounds(e.target.getBounds().pad(2.5));
}

function onEachFeature(feature, layer) {
    layer.on({
        mouseover: highlightFeature,
        mouseout: resetHighlight,
        click: onClickSettings
    });
    
    var county_name = feature.properties.NAME; 
    var str_len = feature.properties.GEO_ID.length; 
    var now_fips = parseInt(feature.properties.GEO_ID.slice(str_len-5, str_len)); 

    layer.bindPopup('<p id="popup">County Name: ' + county_name + '<br> Population: ' + feature.properties.pop +'<br> Hotspot Index Value: ' + feature.properties.index + '<br> Cases per 1000: ' + feature.properties.cases_1000 + '</p>');
}

L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=' + mapboxAccessToken, {
    maxZoom: 20,
    id: 'mapbox/light-v9',
    tileSize: 512,
    zoomOffset: -1,
    stroke: false
}).addTo(mymap);

geoJSON = L.geoJSON(county_data, {
    style:style,
    onEachFeature: onEachFeature
}).addTo(mymap);

var myStyle = {
    "opacity": 0.5,
    "interactive": false,
    "weight": 3,
    "fillOpacity": 0,
    "color": '#000000'
};

L.geoJSON(state_data, {
    style: myStyle
}).addTo(mymap);

//CODE THAT CAN BE USED TO SAVE JSON FILE IF NECESSARY
// function saveText(text, filename) {
//     var a = document.createElement('a');
//     a.setAttribute('href', 'data:text/plain;charset=utf-8,'+encodeURIComponent(text));
//     a.setAttribute('download', filename);
//     a.click();
// }

// saveText(JSON.stringify(county_data), 'test_save.json');