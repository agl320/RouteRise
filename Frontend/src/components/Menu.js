import KeyboardArrowUpIcon from "@mui/icons-material/KeyboardArrowUp";
import {
  IconButton,
  TextField,
  styled,
  Drawer,
  Stack,
  InputAdornment,
  Collapse,
  Typography,
  Slider,
  Button,
} from "@mui/material";
import { useEffect, useRef, useState } from "react";
import SearchIcon from "@mui/icons-material/Search";
import axios from 'axios';
import {
  useMap,
} from "react-leaflet";

const MenuOpenButton = styled(IconButton)`
  position: absolute;
  bottom: 1%;
  z-index: 999;
  background-color: white;

  @media (prefers-color-scheme: dark) {
    filter: var(--leaflet-tile-filter, none);
    :hover {
      background-color: rgba(256, 256, 256, 0.9);
    }
  }
`;

const SearchButton = styled(IconButton)`
  width: 40px;
  height: 40px;
  margin: 8px;
  padding: 0;
  @media (prefers-color-scheme: dark) {
    filter: var(--leaflet-tile-filter, none);
    :hover {
      background-color: rgba(256, 256, 256, 0.1);
    }
  }
`;

const CustomDrawer = styled(Drawer)`
  .MuiDrawer-paper {
    width: 50%;
    margin: auto;
    padding-bottom: 16px;
    @media (prefers-color-scheme: dark) {
      filter: var(--leaflet-tile-filter, none);
    }
  }
`;

const DrawerContainer = styled(Stack)`
  flex-direction: column;
`;

const MainDrawerContainer = styled(Stack)`
  padding-left: 16px;
  padding-top: 16px;
  flex-direction: row;
`;

const CollapseButton = styled(Button)`
  width: fit-content;
  padding: 0;
  padding-top: 5px;
  padding-bottom: 5px;
  margin-left: 16px;
`;

export const Menu = (props) => {
  const [distVal, setDistVal] = useState("");
  const [coordinates, setCoordinates] = useState("");
  const [eleVal, setEleVal] = useState("");
  const [numRoutes, setNumRoutes] = useState("");
  const [expandCollapse, setExpandCollapse] = useState(false);

  const [distSliderVal, setDistSliderVal] = useState(0);
  const [eleSliderVal, setEleSliderVal] = useState(0);

  const { center, setCenter, open, setOpen, setRespData } = props;

  useEffect(() => {
    if (center !== null) {
      setCoordinates(String(center[0]) + ", " + String(center[1]));
    }
  }, [center]);

  const updateValue = (e) => {
    setCoordinates(e.target.value);
  };

  const updateDistVal = (e) => {
    if (
      e.target.value === "" ||
      e.target.value.match(
        /[a-z || A-Z || .,\/#!$%\^&\*;:{}=\-_`~()\'\[\]\+\\\"\?\>\< || \s]/
      )
    ) {
      setDistVal(distVal);
    } else {
      setDistVal(Number(e.target.value));
    }
  };

  const updateEleValue = (e) => {
    if (
      e.target.value === "" ||
      e.target.value.match(
        /[a-z || A-Z || .,\/#!$%\^&\*;:{}=\-_`~()\'\[\]\+\\\"\?\>\< || \s]/
      )
    ) {
      setEleVal(eleVal);
    } else {
      setEleVal(Number(e.target.value));
    }
  };

  const updateNumRoutes = (e) => {
    if (
      e.target.value === "" ||
      e.target.value.match(
        /[a-z || A-Z || .,\/#!$%\^&\*;:{}=\-_`~()\'\[\]\+\\\"\?\>\< || \s]/
      )
    ) {
      setNumRoutes(numRoutes);
    } else {
      setNumRoutes(Number(e.target.value));
    }
  };

  const fetchRoutes = async () => {


    getCoordinates().then(response=>{


      setOpen(false)
      setCenter([response[0], response[1]])
      axios.get(`http://127.0.0.1:5000/get/${response[0]}/${response[1]}`).then(response => {
        console.log(response)
        setRespData(response.data)
    });})
  };

  const getCoordinates = async () => {
    try {
      const response = await axios.get(
        `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(
          coordinates
        )}`
      );

      if (response.data.length > 0) {
        const { lat, lon } = response.data[0];
        // setCoordinates({ latitude: lat, longitude: lon });
        console.log(lat, lon)
        return([lat, lon]);
      } else {
        console.error('No results found for the given address.');
      }
    } catch (error) {
      console.error('Error fetching coordinates:', error);
    }
  };

  const handleCollapse = () => {
    setExpandCollapse(!expandCollapse);
  };

  const distMarks = [
    {
      value: 0,
      label: "+/- 0",
    },
    {
      value: 0.1,
    },
    {
      value: 0.2,
    },
    {
      value: 0.3,
    },
    {
      value: 0.4,
    },
    {
      value: 0.5,
      label: "+/- 0.5",
    },
    {
      value: 0.6,
    },
    {
      value: 0.7,
    },
    {
      value: 0.8,
    },
    {
      value: 0.9,
    },
    {
      value: 1,
      label: "+/- 1",
    },
  ];

  const eleMarks = [
    {
      value: 0,
      label: "+/- 0",
    },
    {
      value: 5,
    },
    {
      value: 10,
    },
    {
      value: 15,
    },
    {
      value: 20,
    },
    {
      value: 25,
      label: "+/- 25",
    },
    {
      value: 30,
    },
    {
      value: 35,
    },
    {
      value: 40,
    },
    {
      value: 45,
    },
    {
      value: 50,
      label: "+/- 50",
    },
  ];

  return (
    <>
      <MenuOpenButton
        onClick={() => {
          setOpen(true);
        }}
      >
        <KeyboardArrowUpIcon />
      </MenuOpenButton>
      <CustomDrawer
        open={open}
        anchor="bottom"
        onClose={() => {
          setOpen(false);
        }}
      >
        <DrawerContainer>
          <MainDrawerContainer>
            <TextField
              label="Distance"
              value={distVal}
              onChange={updateDistVal}
              fullWidth
              InputProps={{
                endAdornment: (
                  <InputAdornment position="end">km</InputAdornment>
                ),
              }}
              required
              sx={{ mr: "16px" }}
            />
            <TextField
              label="Starting Point"
              value={coordinates}
              onChange={updateValue}
              fullWidth
              required
            />
            <SearchButton
              sx={{ color: "#1976d2" }}
              disabled={coordinates === "" || distVal === ""}
              onClick={fetchRoutes}
            >
              <SearchIcon />
            </SearchButton>
          </MainDrawerContainer>
          <CollapseButton onClick={handleCollapse} size="small">
            Other Options
          </CollapseButton>
          <Collapse in={expandCollapse}>
            <Stack spacing={1} sx={{ pl: "16px", pr: "16px", mt: "8px" }}>
              <Stack direction="row">
                <TextField
                  label="Elevation"
                  value={eleVal}
                  onChange={updateEleValue}
                  fullWidth
                  InputProps={{
                    endAdornment: (
                      <InputAdornment position="end">m</InputAdornment>
                    ),
                  }}
                  sx={{ mr: "16px" }}
                />
                <TextField
                  label="Number of Running Routes"
                  value={numRoutes}
                  onChange={updateNumRoutes}
                  fullWidth
                />
              </Stack>
              <Stack
                direction="row"
                sx={{ justifyContent: "space-between", pl: "16px", pr: "16px" }}
              >
                <Stack sx={{ width: "40%" }}>
                  <Typography>Distance Margin of Error</Typography>
                  <Slider
                    step={0.1}
                    marks={distMarks}
                    min={0}
                    max={1}
                    value={distSliderVal}
                    onChange={(e, val) => setDistSliderVal(val)}
                    valueLabelDisplay="auto"
                  />
                </Stack>
                <Stack sx={{ width: "40%" }}>
                  <Typography>Elevation Margin of Error</Typography>
                  <Slider
                    defaultValue={0}
                    step={5}
                    marks={eleMarks}
                    min={0}
                    max={50}
                    value={eleSliderVal}
                    onChange={(e, val) => setEleSliderVal(val)}
                    valueLabelDisplay="auto"
                  />
                </Stack>
              </Stack>
              <Stack direction="row"></Stack>
            </Stack>
          </Collapse>
        </DrawerContainer>
      </CustomDrawer>
    </>
  );
};
