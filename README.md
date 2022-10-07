# CTIC-CON'22: Web of Things Team

Servicios para la presentación de WoT en la CTIC-CON 2022.

* `PhysicMotor`: Firmware para el motor encargado de lanzar al gatín por los aires.
* `agent`: Programa encargado de monitorizar métricas en Influx para publicar eventos en el bróker MQTT.
* `sensors-app`: Aplicación Web que captura muestras de ruido, orientación y clicks de un botón para publicar en el bróker MQTT.
* `slides`: Aplicación Web basada en [Reveal.js](https://revealjs.com/) que contiene la presentación de WoT para la CTIC-CON'22.
* `sound-recognition`: Aplicación Web basada en [Teachable Machine](https://teachablemachine.withgoogle.com/) que expone dos modelos de reconocimiento de audio: uno para 1s y 0s y otro para notas de flauta.
* `temperature-sensor`: Firmware para un sensor de temperatura que escribe muestras en InfluxDB.
