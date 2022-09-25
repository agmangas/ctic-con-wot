import "bootstrap/dist/css/bootstrap.css";
import _ from "lodash";
import mqtt from "mqtt/dist/mqtt";
import { nanoid } from "nanoid";
import React, { useCallback, useEffect, useState } from "react";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { Col, Container, Row } from "reactstrap";
import UAParser from "ua-parser-js";
import "./App.css";
import { LoadingSpinner } from "./LoadingSpinner";

const MQTT_URL = process.env.REACT_APP_MQTT_URL || "mqtt://localhost:9001";
const NAME_ORIENTATION = "orientation";
const NAME_ACCELERATION = "acceleration";
const TOPIC_NEW_CLIENT = "sensors-app/clients";
const TOPIC_ORIENTATION = "sensors-app/orientation";
const TOPIC_ACCELERATION = "sensors-app/acceleration";

function App() {
  const [uniqueId, _setUniqueId] = useState(nanoid());
  const [browserInfo, _setBrowserInfo] = useState(_.toPlainObject(UAParser()));
  const [isLoading, setIsLoading] = useState(false);
  const [mqttClient, setMqttClient] = useState(undefined);

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

      console.log(TOPIC_ORIENTATION, meas);
      mqttClient.publish(TOPIC_ORIENTATION, JSON.stringify(meas));
    },
    [mqttClient, buildMeasurement]
  );

  useEffect(() => {
    if (!mqttClient) {
      return () => {};
    }

    window.addEventListener("deviceorientation", handleOrientation);

    return () => {
      window.removeEventListener("deviceorientation", handleOrientation);
    };
  }, [mqttClient, handleOrientation]);

  useEffect(() => {
    if (!mqttClient) {
      return;
    }

    if (!window.LinearAccelerationSensor) {
      console.warn("LinearAccelerationSensor is unavailable");
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
    });

    theSensor.start();
  }, [mqttClient, buildMeasurement]);

  return (
    <Container fluid={true} className="d-flex h-100">
      <LoadingSpinner show={isLoading} />
      <ToastContainer />
      <Row className="justify-content-center align-self-center">
        <Col xs={12}></Col>
      </Row>
    </Container>
  );
}

export default App;
