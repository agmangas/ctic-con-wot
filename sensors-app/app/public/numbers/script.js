// more documentation available at
// https://github.com/tensorflow/tfjs-models/tree/master/speech-commands

// the link to your model provided by Teachable Machine export panel
// const URL = "https://teachablemachine.withgoogle.com/models/2_NUkWnkK/";
const URL = `${window.location.origin}/numbers/model/`;

async function createModel() {
    const checkpointURL = URL + "model.json"; // model topology
    const metadataURL = URL + "metadata.json"; // model metadata

    const recognizer = speechCommands.create(
        "BROWSER_FFT", // fourier transform type, not useful to change
        undefined, // speech commands vocabulary feature, not useful for your models
        checkpointURL,
        metadataURL
    );

    // check that model and metadata are loaded via HTTPS requests.
    await recognizer.ensureModelLoaded();

    return recognizer;
}

async function init() {
    document.getElementById("btnAction").innerHTML = "🤖 Cargando"
    const recognizer = await createModel();
    const classLabels = recognizer.wordLabels(); // get class labels
    const labelContainer = document.getElementById("label-container");
    let counter = 0;
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
        document.getElementById("label-container").childNodes[winnerIndex].className = "winner"

        // if winner class is "Flauta" with score > 0.75, then increment counter
        if (classLabels[winnerIndex] === "Flauta" && result.scores[winnerIndex] > 0.80) {
            counter++;
            document.getElementById("counter-container").innerHTML = "Numero de hits: " + counter;
        }

        // if the counter is 10, then stop listening
        if (counter === 10) {
            recognizer.stopListening();
            document.getElementById("btnAction").innerHTML = "🎉 Fin"
        }

    }, {
        includeSpectrogram: true, // in case listen should return result.spectrogram
        probabilityThreshold: 0.75,
        invokeCallbackOnNoiseAndUnknown: true,
        overlapFactor: 0.50 // probably want between 0.5 and 0.75. More info in README
    });
    // recognizer.listen(result => {
    //     const scores = result.scores; // probability of prediction for each class

    //     // render the probability scores per class
    //     for (let i = 0; i < classLabels.length; i++) {
    //         const classPrediction = classLabels[i] + ": " + result.scores[i].toFixed(2);

    //         labelContainer.childNodes[i].innerHTML = classPrediction;
    //         labelContainer.childNodes[i].removeAttribute('class');
    //     }

    //         counter++;
    //         document.getElementById("counter-container").innerHTML = "Numero de hits: " + counter;

    // }, {
    //     includeSpectrogram: true, // in case listen should return result.spectrogram
    //     probabilityThreshold: 0.75,
    //     invokeCallbackOnNoiseAndUnknown: false,
    //     overlapFactor: 0.50 // probably want between 0.5 and 0.75. More info in README
    // });

    // Stop the recognition in 5 seconds.
    // setTimeout(() => recognizer.stopListening(), 5000);
}