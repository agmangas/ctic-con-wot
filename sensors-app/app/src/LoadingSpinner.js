import React from "react";
import { Modal, ModalBody, Spinner } from "reactstrap";
import "./LoadingSpinner.css";

export function LoadingSpinner({ show, message }) {
  return (
    <Modal
      isOpen={show}
      className="loading-modal"
      autoFocus={false}
      backdrop="static"
    >
      <ModalBody className="text-center p-4">
        <Spinner style={{ width: "3rem", height: "3rem" }} color="light" />
        {message && <p className="lead mt-3 text-light">{message}</p>}
      </ModalBody>
    </Modal>
  );
}
