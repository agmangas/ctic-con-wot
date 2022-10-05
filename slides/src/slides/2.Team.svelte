<script>
	const wot_traits = [
		{ name: 'Andrés', img: "/images/slack/Andres.png", traits: [
      'El Dr. Dre', 'Arquitectura', 'Y todo lo difícil'
    ]},
    { name: 'Santi', img: "/images/slack/Santi.png", traits: [
      'El del sótano', 'Cacharrea con cosas', 'Baja cosas a tierra'
    ]},
    { name: 'Dani', img: "/images/slack/Dani.png", traits: [
      'Microcontroladores en Peón', 'Cosas puntiagudas', 'Lamentamos su pérdida (hoy no está 😢)'
    ]},
    { name: 'Aser', img: "/images/slack/Aser.png", traits: [
      'El otro de Peón', 'Lo que haya en la pila', 'Chaquetero (también está en Inmersivas)'
    ]},
    { name: 'Javi', img: "/images/slack/Javi.png", traits: [
      'El ex-becario', 'Desarrollo de software', 'Intenta ser Andrés'
    ]},
    { name: 'Sergio', img: "/images/slack/Sergio.png", traits: [
      'Nueva incorporación en WoT', 'Chachi integración con IA', 'Pero le hace ojitos a IA'
    ]},
    { name: 'Wotito', img: "/images/slack/Wotito.jpg", traits: [
      'El jefe de WoT en la sombra', 'Sí, es un gatito 🐱', 'Y es muy mono'
    ]}
	];
</script>



<section>
  <h1 class="fragment step-fade-in-then-out">EL EQUIPO</h1>
  <section>
    <h2>💪🏼 El equipo 💪🏼</h2>
  </section>
    {#each wot_traits as { name, img, traits }}
    <section>
      <div class="r-stack">
        <img class="fragment semi-fade-out" data-fragment-index="1" src={img} alt="member_image" width="400" height="400"/>
        <div>
          <h1 class="fragment fade-in" data-fragment-index="1">{name}</h1>
          <dl>
            {#each traits as trait}
            <dt class="fragment fade-in">{trait}</dt>
            {/each}
          </dl>
        </div>
      </div>
    </section>
    {/each}
</section>
