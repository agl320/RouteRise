// MainComponent.js
import React, { useState } from "react";
import MapComponent from "./components/MapComponent";
import RouteComponent from "./components/RouteComponent";
import { QueryClient, QueryClientProvider } from "react-query";
import { Menu } from "./components/Menu";
import { Stack } from "@mui/material";
import {useMap} from "react-leaflet";

const MainComponent = () => {
  const startPoint = [49.2827, -123.1207];
  const endPoint = [49.26411700132184, -123.21537018955787];
  const [open, setOpen] = useState(false);
  const [respData, setRespData] = useState();

  // const [coords, setCoords] = useState(null);
  const [center, setCenter] = useState(null);

  const queryClient = new QueryClient();

  return (
    <Stack alignItems="center">
      <QueryClientProvider client={queryClient}>
        <MapComponent center={center} setCenter={setCenter}>
          <RouteComponent
            cords={respData}
            // coords={coords}
          />
        </MapComponent>
      </QueryClientProvider>
      <Menu
        center={center}
        //  setCoords={setCoords}
        setCenter={setCenter}
        open={open}
        setOpen={setOpen}
        setRespData={setRespData}
      />
    </Stack>
  );
};

export default MainComponent;
