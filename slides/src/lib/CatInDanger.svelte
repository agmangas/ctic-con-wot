<script>
    import catSprite from '/src/assets/cat.png';
    import trainSprite from '/src/assets/moving_train.png';
    import anime from 'animejs/lib/anime.es.js';
    import { onMount } from 'svelte';

    const TIME_TO_DEATH = 61e3;

    // Binded to elements in the DOM
    let trainWrapperEl;
    let trainEl;
    let catLabelEl;

    let countdown = "100%";
    let progress = 0;

    onMount(()=>{
        anime({
            targets: trainWrapperEl,
            top: "100%",
            translateY: "-100%",
            duration: TIME_TO_DEATH,
            easing: 'linear',
            update: function(anim) {
                let secondsToDeath = (anim.duration - (anim.duration * anim.progress / 100.0)) / 1e3;
                let seconds = Math.floor(secondsToDeath % 60);
                let minutes = Math.floor(secondsToDeath / 60.0);
                countdown = `${minutes}:${("0" + seconds).slice(-2)}`;
            }
        });
        anime({
            targets: trainEl,
            scaleX: ["1.05","0.9"],
            loop: true,
            direction: 'alternate',
            easing: 'linear',
        });

        anime({
            targets: ".cat",
            scale: ["1.05","0.9"],
            rotate: ['10deg', '-10deg'],
            loop: true,
            direction: 'alternate',
            easing: 'linear',
        });
    })

    
</script>

<div class="container">
    <div class="train-track">
        <p bind:this={catLabelEl} class="cat-label">{countdown}</p>
        <div bind:this={trainWrapperEl} class="train-wrapper">
            <img bind:this={trainEl} class="train" src={trainSprite} alt="train drawing"/>
        </div>
    </div>
    <div class="cat-wrapper">
        <img class="cat" src={catSprite} alt="train drawing"/>
    </div>
</div>

<style>

.cat-label{
    width: 100%;
    text-align: center;
    margin: 20px;
    font-size: xx-large;
    font-family: monospace;
    z-index: 2;
    color: white;
}
.container {
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
}

.train-track {
    position: relative;
    display: flex;
    flex-grow: 1;
}

.cat-wrapper {
    height: 180px;
    display: flex;
    justify-content: center;
    align-items: flex-start;
}

.train-wrapper { 
    position: absolute;
    top: 0%;
}

img { 
    width: 80%; 
    height: auto;
    overflow: hidden;
}
</style>
    
