import "bootstrap/dist/css/bootstrap.css";
import _ from "lodash";
import mqtt from "mqtt/dist/mqtt";
import { nanoid } from "nanoid";
import React, { useCallback, useEffect, useState } from "react";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { Alert, Button, Col, Container, Row } from "reactstrap";
import UAParser from "ua-parser-js";
import "./App.css";
import { LoadingSpinner } from "./LoadingSpinner";

const MQTT_URL = process.env.REACT_APP_MQTT_URL || "mqtt://localhost:9001";
const NAME_ORIENTATION = "orientation";
const NAME_ACCELERATION = "acceleration";
const NAME_CLICK = "click";
const TOPIC_NEW_CLIENT = "sensors-app/clients";
const TOPIC_ORIENTATION = "sensors-app/orientation";
const TOPIC_ACCELERATION = "sensors-app/acceleration";
const TOPIC_CLICK = "sensors-app/click";

function App() {
  const [uniqueId, _setUniqueId] = useState(nanoid());
  const [browserInfo, _setBrowserInfo] = useState(_.toPlainObject(UAParser()));
  const [isLoading, setIsLoading] = useState(false);
  const [mqttClient, setMqttClient] = useState(undefined);
  const [numClicks, setNumClicks] = useState(0);
  const [currOrientation, setCurrOrientation] = useState(undefined);
  const [errorAcc, setErrorAcc] = useState(undefined);

  useEffect(() => {
    setIsLoading(true);

    const theMqttClient = mqtt.connect(MQTT_URL);

    theMqttClient.on("connect", () => {
      console.log("MQTT", theMqttClient);
      setMqttClient(theMqttClient);
      setIsLoading(false);
    });
  }, []);

  useEffect(() => {
    if (!mqttClient) {
      return;
    }

    const clientInfo = { [uniqueId]: browserInfo };
    console.log("Client", clientInfo);
    mqttClient.publish(TOPIC_NEW_CLIENT, JSON.stringify(clientInfo));
  }, [mqttClient, uniqueId, browserInfo]);

  const buildMeasurement = useCallback(
    ({ name, fields }) => {
      return Object.assign(
        {
          name,
          time: Date.now(),
          device: uniqueId,
          tag_browser: browserInfo.browser.name,
          tag_os: browserInfo.os.name,
          tag_vendor: browserInfo.device.vendor,
          tag_model: browserInfo.device.model,
        },
        fields
      );
    },
    [uniqueId, browserInfo]
  );

  const handleOrientation = useCallback(
    (event) => {
      if (!mqttClient) {
        return;
      }

      const meas = buildMeasurement({
        name: NAME_ORIENTATION,
        fields: { alpha: event.alpha, beta: event.beta, gamma: event.gamma },
      });

      setCurrOrientation({
        alpha: event.alpha,
        beta: event.beta,
        gamma: event.gamma,
      });

      console.log(TOPIC_ORIENTATION, meas);
      mqttClient.publish(TOPIC_ORIENTATION, JSON.stringify(meas));
    },
    [mqttClient, buildMeasurement]
  );

  useEffect(() => {
    if (!mqttClient) {
      return () => {};
    }

    const throttledHandler = _.throttle(handleOrientation, 200);

    window.addEventListener("deviceorientation", throttledHandler);

    return () => {
      window.removeEventListener("deviceorientation", throttledHandler);
    };
  }, [mqttClient, handleOrientation]);

  useEffect(() => {
    if (!mqttClient) {
      return;
    }

    if (!window.LinearAccelerationSensor) {
      console.warn("LinearAccelerationSensor is unavailable");
      setErrorAcc("El navegador no nos deja leer el acelerómetro");
      return;
    }

    let theSensor = new window.LinearAccelerationSensor({ frequency: 10 });

    theSensor.addEventListener("reading", (event) => {
      const meas = buildMeasurement({
        name: NAME_ACCELERATION,
        fields: { x: event.x, y: event.y, z: event.z },
      });

      console.log(TOPIC_ACCELERATION, meas);
      mqttClient.publish(TOPIC_ACCELERATION, JSON.stringify(meas));
    });

    theSensor.addEventListener("error", (e) => {
      console.warn("LinearAccelerationSensor", e.error);
      setErrorAcc(
        <span>
          El acelerómetro hizo <i>puf</i>: <strong>{e.error.name}</strong>
        </span>
      );
    });

    theSensor.start();
  }, [mqttClient, buildMeasurement]);

  const onClick = useCallback(() => {
    if (!mqttClient) {
      return;
    }

    const meas = buildMeasurement({
      name: NAME_CLICK,
      fields: { click: 1 },
    });

    setNumClicks(numClicks + 1);

    console.log(TOPIC_CLICK, meas);
    mqttClient.publish(TOPIC_CLICK, JSON.stringify(meas));
  }, [mqttClient, buildMeasurement, numClicks]);

  return (
    <Container fluid={true}>
      <LoadingSpinner show={isLoading} />
      <ToastContainer />
      <Row className="mt-3">
        <Col xs={12} className="text-center">
          <h1 className="mb-3">The WoT Team presents</h1>
          <h3 className="mb-3 text-muted">CTIC-CON 2022</h3>
          <Button className="mb-3" color="primary" size="lg" onClick={onClick}>
            Dai click ahí ho
          </Button>
          <Alert className="mt-3 me-5 ms-5" color="secondary">
            Número de clicks: <strong>{numClicks}</strong>
          </Alert>
          {!!currOrientation && (
            <Alert className="mt-3 me-5 ms-5" color="secondary">
              Alpha: <strong>{_.round(currOrientation.alpha, 2)}</strong>
              <br />
              Beta: <strong>{_.round(currOrientation.beta, 2)}</strong>
              <br />
              Gamma: <strong>{_.round(currOrientation.gamma, 2)}</strong>
            </Alert>
          )}
          {!!errorAcc && (
            <Alert className="mt-3 me-5 ms-5" color="warning">
              😭😭 &nbsp; {errorAcc}
            </Alert>
          )}
        </Col>
      </Row>
    </Container>
  );
}

export default App;
