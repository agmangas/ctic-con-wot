<script>
    import cat_sprite from '/src/assets/cat.png';
    import train_sprite from '/src/assets/train.png';
</script>

<div class="container">
    <div class="train-wrapper">
        <img class="train" src={train_sprite} alt="train drawing"/>
    </div>
    <div class="cat-wrapper">
        <img class="cat" src={cat_sprite} alt="train drawing"/>
    </div>
</div>

<style>
@keyframes crying-cat {
  0%   {width: 96%; transform: rotate(1deg);}
  25% {width: 100%; transform: rotate(0deg);}
  50% {width: 96%; transform: rotate(-1deg);}
  75% {width: 100%; transform: rotate(0deg);}
  100% {width: 96%; transform: rotate(1deg);}
}
@keyframes choo-choo-mf {
  0%   {width: 98%;}
  50%  {width: 100%;}
  100% {width: 98%;}
}
@keyframes choo-choo-mf-move {
    from {
        bottom: 100%;
        top: 0%;
    }
    to {
        transform: translateY(-100%);
        bottom: 0%;
        top: 100%;
    }
}

.container {
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
}

.train-wrapper {
    position: relative;
    display: flex;
    flex-grow: 1;
    background-color: rgb(175, 79, 79);
}

.cat-wrapper {
    height: 180px;
    display: flex;
    align-self: flex-end;
    align-items: center;
    background-color: rgb(176, 176, 255);
}

.train { 
    animation: choo-choo-mf-move 10s linear infinite, choo-choo-mf 1s linear infinite;
    animation-delay: 200ms;
    position: absolute;
    top: 0%;
}

.cat { animation: crying-cat 2s linear infinite;}

img { width: 80%; height: auto;}
</style>
    
