<script>
  import Reveal from "reveal.js";
  import * as mqtt from "mqtt"
  import { onMount } from "svelte";
  import { createEventDispatcher } from 'svelte';

  // Event dispatcher
	const dispatch = createEventDispatcher();

	const slideHandler = (() => {
    let previousIndexh = 0;
    return (event)=> {
      dispatch('slide-changed', {
          previousIndexh: previousIndexh,
          indexh: event.indexh,
          totalSlides: deck.getTotalSlides()
        });
      previousIndexh = event.indexh;
    }
	})();

  // MQTT Initialization and configuration
  const TOPIC_SLIDES_COMMAND = "slides/command";

  const MQTT_URL = import.meta.env.VITE_SLIDES_APP_MQTT_URL || "ws://localhost:9001";
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
      window.postMessage(message.toString());
    }
  })

  // Initalize deck canvas
  let deck;
  let deckCanvas;
  const redrawSlides = ()=>{
    console.log("redrawing")
    deck.layout();
  }

  onMount(() => {
    deck = Reveal(deckCanvas, {
      minScale: 0.2,
    });
    deck.initialize();
    deck.on('slidechanged', slideHandler);
  });
</script>

<div class="reveal" bind:this={deckCanvas}>
  <div class="slides">
    <section>
      <h1>WoT</h1>
      <h2>Web of Things</h2>
      <span class="fragment">
        <p>es... como Internet de las Cosas</p>
      </span>
      <p class="fragment">(pero mejor)</p>
    </section>
    <section>
      <h2>IoT</h2>
      <p>Dispositivos que se comunican con ordenadores y entre sí</p>
      <p>Ordenadores que se comunican entre sí</p>
      <p>Servicios para usar los datos obtenidos</p>
    </section>
    <section>
      <h2>¿Y WoT?</h2>
      <p>Estándar para saber cómo se tienen que comunicar entre sí</p>
    </section>
    <section>
      <div class="r-fit-text">
        <table style="width: 100%">
          <tr>
            <th>Andrés</th>
            <th>Santi</th>
            <th>Dani</th>
            <th>Aser</th>
            <th>Javi</th>
            <th>Sergio</th>
          </tr>
          <tr>
            <td>Arquitecturas</td>
            <td>Cacharrear</td>
            <td>Microcontroladores</td>
            <td>Lo que haya en la pila</td>
            <td>Desarrollo software</td>
            <td>Integración IA chachi</td>
          </tr>
          <tr>
            <td>Cosas difíciles</td>
            <td>Bajar cosas a tierra</td>
            <td>Cosas puntiagudas</td>
            <td>Chaquetero de visión</td>
            <td>Amotinarse y ser Andrés</td>
            <td>Le hace ojitos a IA</td>
          </tr>
        </table>
      </div>
    </section>

    <section>
      WAPO WAPO
      <iframe
        title="Dashboard"
        class="r-stretch"
        src="http://localhost:3000/d-solo/0atAxsnVk/new-dashboard?orgId=1&refresh=5s&panelId=6"
        width="250"
        frameborder="0"
      />
    </section>
    <section>
      WAPO WAPO 2
      <iframe
        title="Dashboard"
        src="http://localhost:3000/d-solo/0atAxsnVk/new-dashboard?orgId=1&refresh=5s&panelId=6"
        width="450"
        height="200"
        frameborder="0"
      />
    </section>
    <section>
      Slide 3
      <aside class="notes">
        <p>Some notes</p>
      </aside>
      <p>Some slide text</p>
      <aside class="notes">
        <p>and some more notes</p>
      </aside>
    </section>
  </div>
</div>

<style>
  div {
    table-layout: fixed;
  }
</style>
