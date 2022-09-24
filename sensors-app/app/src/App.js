import "bootstrap/dist/css/bootstrap.css";
import React, { useState } from "react";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { Col, Container, Row } from "reactstrap";
import "./App.css";
import { LoadingSpinner } from "./LoadingSpinner";

function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [loadingMsg, setLoadingMsg] = useState(undefined);

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
