import "bootstrap/dist/css/bootstrap.css";
import _ from "lodash";
import mqtt from "mqtt/dist/mqtt";
import { nanoid } from "nanoid";
import React, { useEffect, useState } from "react";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { Col, Container, Row } from "reactstrap";
import "./App.css";
import { LoadingSpinner } from "./LoadingSpinner";

const MQTT_URL = process.env.REACT_APP_MQTT_URL || "mqtt://localhost:9001";
const TOPIC_NEW_CLIENT = "sensors-app/clients";

function App() {
  const [uniqueId, _setUniqueId] = useState(nanoid());

  const [navigatorInfo, _setNavigatorInfo] = useState(
    _.toPlainObject(navigator)
  );

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

    const clientInfo = { [uniqueId]: navigatorInfo };
    console.log("Client", clientInfo);
    mqttClient.publish(TOPIC_NEW_CLIENT, JSON.stringify(clientInfo));
  }, [mqttClient]);

  useEffect(() => {
    if (!mqttClient) {
      return;
    }

    if (!window.LinearAccelerationSensor) {
      console.warn("LinearAccelerationSensor is unavailable");
      return;
    }

    let theSensor = new window.LinearAccelerationSensor({ frequency: 1 });

    theSensor.addEventListener("reading", (e) => {
      console.log(`Linear acceleration along the X-axis ${theSensor.x}`);
      console.log(`Linear acceleration along the Y-axis ${theSensor.y}`);
      console.log(`Linear acceleration along the Z-axis ${theSensor.z}`);
    });

    theSensor.addEventListener("error", (e) => {
      console.warn("LinearAccelerationSensor", e.error);
    });

    theSensor.start();
  }, [mqttClient]);

  useEffect(() => {
    if (!mqttClient) {
      return;
    }

    if (!window.AmbientLightSensor) {
      console.warn("AmbientLightSensor is unavailable");
      return;
    }

    let theSensor = new window.AmbientLightSensor({ frequency: 1 });

    theSensor.addEventListener("reading", (e) => {
      console.log(e);
    });

    theSensor.addEventListener("error", (e) => {
      console.warn("AmbientLightSensor", e.error);
    });

    theSensor.start();
  }, [mqttClient]);

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
