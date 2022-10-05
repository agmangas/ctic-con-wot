<script>
    import Reveal from "reveal.js";

    //Slides
    export let slideHandler;
    import Intro from "./slides/1.Intro.svelte"
    import Team from "./slides/2.Team.svelte"
    import Cat from "./slides/3.CatInDanger.svelte"
    import WoT from "./slides/4.WoT.svelte"
    import Collaboration from "./slides/5.Collaboration.svelte"
    import TeamGame from "./slides/6.TeamGame.svelte"
    import FinishConclusions from "./slides/7.FinishConclusions.svelte"
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
    if(command.method === "slide" && (command.args[0]-previousIndexh)===1){
        console.log("Command method is "+command.method+" and the slide is the next or previous one (previous: "+previousIndexh+" | next: "+command.args[0]+"), so come on!")
        window.postMessage(e.detail.command)
    }
    else if(command.method === "slide")
        console.log("The input slide ["+ command.args[0] +"] inside command is not the next one [current is: "+(previousIndexh)+"], lets ignore event")
}}"/>

    <div class="reveal" bind:this={deckCanvas}>
        <div class="slides">
            <Intro/>
            <Team/>
            <Cat/>
            <WoT/> 
            <Collaboration/>
            <TeamGame {GRAFANA_URL}/>
            <FinishConclusions/>
        </div>
    </div>
    
    <style>
      div {
        table-layout: fixed;
      }
    </style>
    