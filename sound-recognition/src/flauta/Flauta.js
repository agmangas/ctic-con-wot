import React from "react";
import soundRecognizer from "../soundRecognizer";
import * as mqtt from "../mqtt-client";

class Flauta extends React.Component {

    constructor(props) {
        super(props);
        this.state = {counter: 0};

        this.callback = this.callback.bind(this);
    }

    componentDidMount() {
        document.body.style = 'background: antiquewhite;';
        mqtt.connect();
    }

    callback(result, classLabels, winnerIndex) {
        // if winner class is "Flauta" with score > x , then increment counter
        if (classLabels[winnerIndex] === "Flauta" && result.scores[winnerIndex] > 0.80) {
            this.setState({counter: this.state.counter + 1});
            document.getElementById("counter-container").innerHTML = "Numero de hits: " + this.state.counter;
        }

        // if the counter is 10, then stop listening
        if (this.state.counter === this.props.maxNumberOfHits) {
            soundRecognizer.end()
            mqtt.next()
        }
    }

    render() {
        return (
            <div id="flauta">
                <h1>🎸 Teachable Machine Audio Model</h1>
                <button id="btnAction" type="button"
                        onClick={() => soundRecognizer.start(this.props.url, this.callback)}>🎤 Empezar
                </button>
                <div id="label-container"></div>
                <div id="counter-container"></div>
            </div>
        );
    }
}


export default Flauta;