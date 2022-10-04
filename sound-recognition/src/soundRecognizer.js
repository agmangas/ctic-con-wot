import * as speechCommands from "@tensorflow-models/speech-commands";

let recognizer = null;

function start(URL, callback) {
    async function createModel(URL) {

        const checkpointURL = URL + "model.json"; // model topology
        const metadataURL = URL + "metadata.json"; // model metadata

        const recognizer = speechCommands.create(
            "BROWSER_FFT", // fourier transform type, not useful to change
            undefined, // speech commands vocabulary feature, not useful for your models
            checkpointURL,
            metadataURL
        );
        // tf.test()
        // check that model and metadata are loaded via HTTPS requests.
        await recognizer.ensureModelLoaded();

        return recognizer;
    }

    async function init(URL) {
        document.getElementById("btnAction").innerHTML = "🤖 Cargando"
        recognizer = await createModel(URL);
        const classLabels = recognizer.wordLabels(); // get class labels
        const labelContainer = document.getElementById("label-container");

        for (let i = 0; i < classLabels.length; i++) {
            labelContainer.appendChild(document.createElement("div"));
        }

        document.getElementById("btnAction").innerHTML = "🐈 Escuchando"
        // listen() takes two arguments:
        // 1. A callback function that is invoked anytime a word is recognized.
        // 2. A configuration object with adjustable fields
        recognizer.listen(result => {
            const scores = result.scores; // probability of prediction for each class
            const winnerIndex = scores.indexOf(Math.max(...scores)); // the class with the highest probability

            // render the probability scores per class
            for (let i = 0; i < classLabels.length; i++) {
                const classPrediction = classLabels[i] + ": " + result.scores[i].toFixed(2);

                labelContainer.childNodes[i].innerHTML = classPrediction;
                labelContainer.childNodes[i].removeAttribute('class');
            }
            document.getElementById("label-container").childNodes[winnerIndex].className = "winner";

            callback(result, classLabels, winnerIndex);

        }, {
            includeSpectrogram: true, // in case listen should return result.spectrogram
            probabilityThreshold: 0.75,
            invokeCallbackOnNoiseAndUnknown: true,
            overlapFactor: 0.50 // probably want between 0.5 and 0.75. More info in README
        });
    }

    init(URL)
}

function end() {
    recognizer.stopListening();
    document.getElementById("btnAction").innerHTML = "🎉 Fin"
}

const soundRecognizer = {start, end, recognizer}
export default soundRecognizer