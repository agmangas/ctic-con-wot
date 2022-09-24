import "bootstrap/dist/css/bootstrap.css";
import _ from "lodash";
import mqtt from "mqtt/dist/mqtt";
import React, { useEffect, useState } from "react";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { Col, Container, Row } from "reactstrap";
import "./App.css";
import { LoadingSpinner } from "./LoadingSpinner";

const MQTT_URL = process.env.REACT_APP_MQTT_URL || "mqtt://localhost:9001";
const TOPIC_NEW_CONNECTION = "sensors-app/connections";

function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [loadingMsg, setLoadingMsg] = useState(undefined);
  const [mqttClient, setMqttClient] = useState(undefined);
  const [navigatorInfo, setNavigatorInfo] = useState(undefined);

  useEffect(() => {
    setIsLoading(true);

    const theClient = mqtt.connect(MQTT_URL);

    theClient.on("connect", () => {
      console.log("MQTT client", theClient);
      setMqttClient(theClient);
      setIsLoading(false);
    });
  }, []);

  useEffect(() => {
    const theInfo = _.toPlainObject(navigator);
    setNavigatorInfo(theInfo);
    console.log("Client info", theInfo);
  }, []);

  useEffect(() => {
    if (mqttClient && navigatorInfo) {
      mqttClient.publish(TOPIC_NEW_CONNECTION, JSON.stringify(navigatorInfo));
    }
  }, [mqttClient, navigatorInfo]);

  return (
    <Container fluid={true} className="d-flex h-100">
      <LoadingSpinner show={isLoading} message={loadingMsg} />
      <ToastContainer />
      <Row className="justify-content-center align-self-center">
        <Col xs={12}></Col>
      </Row>
    </Container>
  );
}

export default App;
