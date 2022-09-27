<script>
    import Reveal from 'reveal.js'
    import Markdown from 'reveal.js/plugin/markdown/markdown.js'
    import { onMount } from 'svelte';
    
    export let markdown_content;

    let deck_canvas;

    onMount(() => {
        let deck = Reveal(deck_canvas, {
            plugins: [ Markdown ]
        });
        deck.initialize();
    });
</script>

<div class="reveal" bind:this={deck_canvas}>
    <div class="slides">
        <section data-markdown={markdown_content}>
        </section>
    </div>
</div>