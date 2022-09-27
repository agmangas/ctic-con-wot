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
const NAME_CLICK = "click";
const NAME_NOISE = "noise";
const TOPIC_NEW_CLIENT = "sensors-app/clients";
const TOPIC_ORIENTATION = "sensors-app/orientation";
const TOPIC_CLICK = "sensors-app/click";
const TOPIC_NOISE = "sensors-app/noise";

function App() {
  const [uniqueId, _setUniqueId] = useState(nanoid());
  const [browserInfo, _setBrowserInfo] = useState(_.toPlainObject(UAParser()));
  const [isLoading, setIsLoading] = useState(false);
  const [mqttClient, setMqttClient] = useState(undefined);
  const [numClicks, setNumClicks] = useState(0);
  const [currOrientation, setCurrOrientation] = useState(undefined);
  const [audioActive, setAudioActive] = useState(false);
  const [audioMean, setAudioMean] = useState(undefined);
  const [audioError, setAudioError] = useState(undefined);

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

  const onAudioProcess = useCallback(
    (event) => {
      if (!mqttClient) {
        return;
      }

      const rawBuf = event.inputBuffer.getChannelData(0);
      const theAudioLevel = _.round(Math.abs(_.mean(rawBuf)) * 1e3, 6);

      const meas = buildMeasurement({
        name: NAME_NOISE,
        fields: { noise: theAudioLevel },
      });

      setAudioMean(theAudioLevel);

      console.log(TOPIC_NOISE, meas);
      mqttClient.publish(TOPIC_NOISE, JSON.stringify(meas));
    },
    [buildMeasurement, mqttClient]
  );

  useEffect(() => {
    if (numClicks <= 0 || audioActive || !mqttClient) {
      return;
    }

    setAudioActive(true);

    navigator.mediaDevices
      .getUserMedia({ video: false, audio: true })
      .then(function (stream) {
        const context = new AudioContext();
        const source = context.createMediaStreamSource(stream);
        const processor = context.createScriptProcessor(1024, 1, 1);
        source.connect(processor);
        processor.connect(context.destination);
        processor.onaudioprocess = _.throttle(onAudioProcess, 200);
      })
      .catch(function (error) {
        console.warn(error);
        setAudioError(error);
      });
  }, [numClicks, audioActive, onAudioProcess, mqttClient]);

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
          <Alert className="mt-3 me-5 ms-5" color="info">
            Número de clicks: <strong>{numClicks}</strong>
          </Alert>
          {!!currOrientation && (
            <Alert className="mt-3 me-5 ms-5" color="info">
              <code>Alpha:</code>&nbsp;
              <strong>{_.round(currOrientation.alpha, 2)}</strong>
              <br />
              <code>Beta:</code>&nbsp;
              <strong>{_.round(currOrientation.beta, 2)}</strong>
              <br />
              <code>Gamma:</code>&nbsp;
              <strong>{_.round(currOrientation.gamma, 2)}</strong>
            </Alert>
          )}
          {!_.isNil(audioMean) && (
            <Alert className="mt-3 me-5 ms-5" color="info">
              <span>Nivel de ruido:</span>&nbsp;
              <strong>{_.round(audioMean, 3)}</strong>
              <br />
            </Alert>
          )}
          {!currOrientation && (
            <Alert className="mt-3 me-5 ms-5" color="warning">
              No podemos leer el sensor de orientación 😔
            </Alert>
          )}
          {!!audioError && (
            <Alert className="mt-3 me-5 ms-5" color="warning">
              No podemos leer el micrófono 😔
            </Alert>
          )}
        </Col>
      </Row>
    </Container>
  );
}

export default App;
