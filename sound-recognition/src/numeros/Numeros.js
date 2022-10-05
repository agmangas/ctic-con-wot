import React from "react";
import soundRecognizer from "../soundRecognizer";
import * as mqtt from "../mqtt-client";

class Numeros extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            ceros: 0,
            unos: 0
        };

        this.callback = this.callback.bind(this);
    }

    componentDidMount() {
        document.body.style = 'background: rgb(194, 246, 255);';
        mqtt.connect();
    }

    callback(result, classLabels, winnerIndex) {

        if (classLabels[winnerIndex] !== "Ruido de fondo" && result.scores[winnerIndex] > 0.70)
            this.setState(winnerIndex === 0 ? {ceros: this.state.ceros + 1} : {unos: this.state.unos + 1});

        // stop condition defined in index.js
        if (this.state.ceros >= this.props.maxNumberOfHits.cero && this.state.unos >= this.props.maxNumberOfHits.uno) {
            soundRecognizer.end()
            mqtt.next()
        }
        
    }

    render() {
        return (
            <div id="nums">
                <h1>🔢 Teachable Machine Audio Model</h1>
                <button id="btnAction" type="button"
                        onClick={() => soundRecognizer.start(this.props.url, this.callback)}>🎤 Empezar
                </button>
                <div style={{display: "flex"}}>
                    <div id="label-container"></div>
                    <div id="counter-container" hidden={this.state.ceros <= 0 && this.state.unos <= 0}>
                        <div id="cero-container"
                             className={this.state.ceros >= this.props.maxNumberOfHits.cero ? "ended" : ""}>
                            ({this.state.ceros} hits)
                        </div>
                        <div id="uno-container"
                             className={this.state.unos >= this.props.maxNumberOfHits.uno ? "ended" : ""}>
                            ({this.state.unos} hits)
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}


export default Numeros;