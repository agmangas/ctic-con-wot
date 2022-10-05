<script>
  import Slides from './Presentation.svelte';
  import CatInDanger from './lib/CatInDanger.svelte';
  import { fly } from 'svelte/transition';
  
  let presentationState = "idle";

  function slideHandler(e)
  {
    if (e.detail.indexh === 0) {
      presentationState = "idle"
    }
    else if (e.detail.indexh === 4 && e.detail.previousIndexh === 3){
      presentationState = "running" //Cat appears
    }
    else if (e.detail.indexh === (e.detail.totalSlides - 1)){
      presentationState = "done"
    }
  }
</script>

<div class="container">
  {#if presentationState !== "idle"}
    <div class="side-item" transition:fly="{{ x: -200, duration: 1000 }}">
      <CatInDanger presentationState={presentationState}/>
    </div>
  {/if}
  <div class="center-item">
    <Slides on:slide-changed={slideHandler}/>
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

