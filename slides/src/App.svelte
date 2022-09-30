<script>
  import Slides from './lib/Slides.svelte';
  import CatInDanger from './lib/CatInDanger.svelte';
  import { fly } from 'svelte/transition';
  
  let visible = false;
</script>

<div class="container">
  {#if visible}
    <div class="side-item" transition:fly="{{ x: -200, duration: 1000 }}">
      <CatInDanger />
    </div>
  {/if}
  <div class="center-item">
    <Slides on:jeopardize-cat="{e => visible = e.detail.value}"/>
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

