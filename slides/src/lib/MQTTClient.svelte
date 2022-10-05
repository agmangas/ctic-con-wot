<script>
    import { createEventDispatcher } from "svelte";
    import * as mqtt from "mqtt"

    // Event dispatcher
	const dispatch = createEventDispatcher();

    const TOPIC_SLIDES_COMMAND = "slides/command";

    const MQTT_URL = import.meta.env.VITE_SLIDES_APP_MQTT_URL || "ws://localTESThost:9001";
    const client = mqtt.connect(MQTT_URL);
    console.log(`Connecting to: ${MQTT_URL}`);

    client.on("connect", () => {
        console.log("MQTT", client);
        client.subscribe(TOPIC_SLIDES_COMMAND, (err)=>{
        if (!err) {
            console.log("Subscribed");
        }
        });
    })

    client.on('message', function (topic, message) {
        if (topic == TOPIC_SLIDES_COMMAND){
            console.log(message.toString());
            dispatch('command', {
                command: message.toString()
            });
        }
    })
</script>