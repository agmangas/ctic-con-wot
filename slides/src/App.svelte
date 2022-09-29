<script>
  import Slides from './lib/Slides.svelte';
  import CatInDanger from './lib/CatInDanger.svelte';
</script>

<div class="container">
  <div class="side-item">
    <CatInDanger />
  </div>
  <div class="center-item">
    <Slides />
  </div>
</div>


<style>
  .center-item {
    flex-grow: 1;
    
  }
  .side-item {
    width: 20%;
    background-color: black;
  }
  .container {
    width: 100%;
    height: 100%;
    display: flex;
  }
</style>

