// RouteComponent.js
import React, { useEffect } from "react";
import { useQuery } from "react-query";
import { Polyline } from "react-leaflet";

// cords is an array of tuples that are coordinates
const fetchRoute = async (cords) => {
  const apiKey =
    "pk.eyJ1IjoiY3dvbiIsImEiOiJjbHJtcDhucDQxMjY4MmtrZHA4cjY4Yzk0In0.pUcXee7umuJcGYPfes9kSQ"; // Replace with your Mapbox API key
  const response = await fetch(
    `https://api.mapbox.com/directions/v5/mapbox/walking/${cords.map((item, index) => {return index === 0 ? item[0]+"%C2"+item[1] : "%B3"+item[0]+"%C2"+item[1]})}?alternatives=true&continue_straight=true&geometries=geojson&language=en&overview=simplified&steps=true&access_token${apiKey}`
  );
  console.log(response);
  const data = await response.json();
  console.log(data);
  console.log(data.routes[0].geometry.coordinates);
  var retArr = [];
  data.routes[0].geometry.coordinates.map((route, index) => {
    retArr[index] = [route[1], route[0]];
  });
  return retArr;
};

const RouteComponent = (cords) => {
  // const { data: routeCoordinates } = useQuery(["route", start, end], () =>
  //   fetchRoute(start, end)
  // );

  useEffect(() => {
    // const { data: routeCoordinates } = useQuery(["route", cords], () =>
    // fetchRoute(cords)
    // );

    fetchRoute(cords)
  }, cords)
  const routeCoordinates = null;

  return routeCoordinates ? (
    <Polyline positions={routeCoordinates} color="red" />
  ) : null;
};

export default RouteComponent;
