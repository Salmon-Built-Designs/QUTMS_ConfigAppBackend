import { Line } from 'react-chartjs-2';
import {React, useState, useEffect} from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';
import Grid from '@material-ui/core/Grid';
import { Typography } from '@material-ui/core';
import Checkbox from '@material-ui/core/Checkbox';
import Divider from '@material-ui/core/Divider';
import LinearProgress from '@material-ui/core/LinearProgress';
import { io, httpServer, socket } from 'socket.io';

const cors = require('cors');
// App.use(cors())
// const sio = require('socket.io-client');
// const socket = io("http://0.0.0.0:8000");
const sio = require("socket.io")(httpServer, {
  cors: {
    origin: "http://172.19.61.246:5000",
    methods: ["GET", "POST"]
  }
});
httpServer.listen(3000)

socket.on("connection", (socket) => {
  console.log(socket.id);
});

var d = [];
var t = [0];
const rand = () => (Math.random() * 0.7 + 3.1);

function getData() {
  d.push(rand())
  return d;
}

var start = new Date().getTime() / 1000;

function getDataT() {
  t.push((new Date().getTime() / 1000 - start).toFixed(3));
  return t;
}

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
  },
  paper: {
    padding: theme.spacing(2),
    textAlign: 'center',
    color: theme.palette.text.secondary,
  },
}));

function genData() {
  return ({
    labels: getDataT(),
    datasets: [
      {
        label: 'Voltage',
        data: getData(),
        options: {
          animation: {
              duration: 0
          }
        },
        backgroundColor: [
          'rgba(255, 99, 132, 0.2)',
        ],
        borderColor: [
          'rgba(255, 99, 132, 1)',
        ],
        borderWidth: 1,
      },
    ],
  });
}

const opt = {
  animation: {
    duration: 0
}
}

function App() {

  const [data, setData] = useState(genData);

  useEffect(() => {
    const interval = setInterval(() => 
    {
      setData(genData())
      // console.log("fuck can they run")
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  const classes = useStyles();

  const v = 0;

  return (
    <div className={classes.root}>
      <Grid container>
        <Grid item xs={3}>
          <Paper>
            {/* Column 1 */}
            <Line data={data} options={opt} />
            <Line data={data} options={opt} />
            <Line data={data} options={opt} />
            <Line data={data} options={opt} />
          </Paper>
        </Grid>
        <Grid item xs={3}>
          <Paper>
            {/* Column 3 */}
            <Line data={data} options={opt} />
            <Line data={data} options={opt} />
            <Line data={data} options={opt} />
            <Line data={data} options={opt} />
          </Paper>
        </Grid>
        <Grid item xs={6}>
          <Paper className={classes.paper}>
            {/* Column 2 */}
            <Grid container>
              <Grid item xs={4}>
                <Checkbox color="secondary" checked={true} indeterminate />
                <Typography>PRECHARGE</Typography>
              </Grid>
              <Grid item xs={4}>
                <Checkbox color="primary" checked={false} indeterminate/>
                <Typography>HV+</Typography>
              </Grid>
              <Grid item xs={4}>
                <Checkbox color="primary" checked={false} indeterminate />
                <Typography>HV-</Typography>  
              </Grid>
              <Grid item xs={6}>
                <Divider />
                <Typography>VSTATE: {false}</Typography>
              </Grid>
              <Grid item xs={6}>
                <Divider />
                <Typography>SHDNS: OK</Typography>
              </Grid>
              <Grid item xs={12}>
                <Divider />
                <Typography>ACCELERATION: </Typography>
                <LinearProgress variant="determinate" value={35} />
                <Typography>BRAKING: </Typography>
                <LinearProgress variant="determinate" color="secondary" value={20} />
                <br></br>
                <Divider />
                <Typography align="left">SVOLTAGE: {v}</Typography>
                <Typography align="left">BMSVOLTAGE: {v}</Typography>
                <Typography align="left">BMSTEMPERATURE: {v}</Typography>
                <Typography align="left">COLOUMBCOUNT: {v}</Typography>
                <Typography align="left">SOC: {v}</Typography>
                <Typography align="left">HVAC: {v}</Typography>
                <Typography align="left">HVBC: {v}</Typography>
                <Divider />
                <Typography align="left">GBTEMPERATURE: {v}</Typography>
                <Typography align="left">RADTEMPL: {v}</Typography>
                <Typography align="left">RADTEMPR: {v}</Typography>
                <Typography align="left">RADPRESL: {v}</Typography>
                <Typography align="left">RADPRESR: {v}</Typography>
              </Grid>
            </Grid>
          </Paper>
        </Grid>
      </Grid>
    </div>
  );
}

export default App;
