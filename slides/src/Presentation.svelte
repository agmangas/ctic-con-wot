<script>
    import Reveal from "reveal.js";

    //Slides
    export let slideHandler;
    import Intro from "./slides/Intro.svelte"
    //

    import { onMount } from "svelte";
    import { createEventDispatcher } from 'svelte';
    import MqttClient from "./lib/MQTTClient.svelte";
  
    const GRAFANA_URL = import.meta.env.VITE_SLIDES_APP_GRAFANA_URL || "http://localhost:3000";
  
    // Event dispatcher
    const dispatch = createEventDispatcher();
  
    // Binded to DOM
    let deckCanvas;
  
    // Initalize deck canvas
    let deck;

    let previousIndexh = 0;
  
    onMount(() => {
      deck = Reveal(deckCanvas, {
        minScale: 0.2,
      });
      deck.initialize();
      deck.on('slidechanged', slideChangeHandler);
      
    });
  
    const slideChangeHandler = (() => {
      
      return (event)=> {
        console.log("Slide change handler: ")
        console.log(event)
        dispatch('slide-changed', {
            previousIndexh: previousIndexh,
            indexh: event.indexh,
            totalSlides: deck.getTotalSlides()
          });
        previousIndexh = event.indexh;
      }
      })();
  
  </script>

<MqttClient on:command="{e => {
    let command = JSON.parse(e.detail.command)
    console.log("MQTT Event! ")
    console.log(e)
    if(command.method === "slide" && Math.abs(command.args[0]-previousIndexh)===1){
        console.log("Command method is "+command.method+" and the slide is the next or previous one (previous: "+previousIndexh+" | next: "+command.args[0]+"), so come on!")
        window.postMessage(e.detail.command)
    }
    else if(command.method === "slide")
        console.log("The slide inside command is not the next one, lets ignore event")
}}"/>

    <div class="reveal" bind:this={deckCanvas}>
        <div class="slides">
            <Intro {GRAFANA_URL}/>
        </div>
    </div>
    
    <style>
      div {
        table-layout: fixed;
      }
    </style>
    