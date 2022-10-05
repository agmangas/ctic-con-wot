<script>
    import catSprite from '/src/assets/cat.png';
    import trainSprite from '/src/assets/moving_train.png';
    import terminatedCat from '/src/assets/terminated_cat.png';
    import savedCatSprite from '/src/assets/saved_cat.png'
    
    import anime from 'animejs/lib/anime.es.js';

    import { fade } from 'svelte/transition';
    import { onMount } from 'svelte';

    const TIME_TO_DEATH = 510e3;

    // Binded to elements in the DOM
    let trainWrapperEl;
    let trainEl;
    let catLabelEl;
    
    // Variables
    let countdown = "100%";
    
    // Possible states of the animation
    const catStates = {
        idle: "idle",
        danger: "danger",
        terminated: "terminated",
        saved: "saved"
    }

    let catState = catStates.idle;

    // Props
    export let presentationState = "idle";

    // State management
    $: if (presentationState === "done") {
        if(catState === catStates.terminated){ }
        else { catState = catStates.saved; }
    }
    else if (presentationState === "running"){
        if(catState === catStates.terminated){ }
        else{ catState = catStates.danger;}
    }
    else {
        catState = catStates.idle;
    }

    onMount(()=>{
        // Train movement
        let trainAnimation = anime({
            targets: trainWrapperEl,
            top: "100%",
            translateY: "-100%",
            duration: TIME_TO_DEATH,
            easing: 'linear',
            update: function(anim) {
                let secondsToTermination = (anim.duration - (anim.duration * anim.progress / 100.0)) / 1e3;
                let seconds = Math.floor(secondsToTermination % 60);
                let minutes = Math.floor(secondsToTermination / 60.0);
                countdown = `${minutes}:${("0" + seconds).slice(-2)}`;
            }
        });
        trainAnimation.finished.then(() => {
            if (presentationState !== "done") {
                catState=catStates.terminated;
            }
        });


        // Animation of sprites
        anime({
            targets: ".train",
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

{#if catState === catStates.danger}
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
{:else if catState === catStates.terminated}
    <div transition:fade class="terminated cat-container">
        <img src={terminatedCat} alt="cat terminated"/>
    </div>

{:else }
    <div transition:fade class="saved cat-container">
        <img src={savedCatSprite} alt="cat terminated"/>
    </div>
{/if}


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

.cat-container {
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}
.terminated{
    background-color: rgb(207, 74, 51);
}
.saved{
    background-color: rgb(36, 214, 116);
}
</style>
    
