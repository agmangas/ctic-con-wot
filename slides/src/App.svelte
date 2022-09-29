<script>
  import Slides from './lib/Slides.svelte';
  import CatInDanger from './lib/CatInDanger.svelte';
  import anime from 'animejs/lib/anime.es.js';
  import { onMount } from 'svelte';

  const MQTT_URL = import.meta.env.VITE_SLIDES_APP_MQTT_URL || "ws://localhost:9001";

  onMount(()=>{
    var tl = anime.timeline({
        targets: ".side-item",
        duration: 2000,
        width: ["0%","12%"],
        easing: 'easeOutExpo',
        delay: 2000,
    });
    tl.add({
        targets: ".side-item",
        opacity: [0, 1],
        easing: 'linear',
    })
  })

</script>

<div class="container">
  <div class="side-item">
    <CatInDanger />
  </div>
  <div class="center-item">
    <Slides mqttURL={MQTT_URL}/>
  </div>
</div>


<style>
  .center-item {
    flex-grow: 1;
    justify-content: center;    
  }
  .side-item {
    width: 15%;
    background-color: rgb(25, 34, 39);
  }
  .container {
    width: 100%;
    height: 100%;
    display: flex;
  }
</style>

