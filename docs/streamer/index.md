# Overview
Este módulo fue diseñado para asistir al desarrollador, brindando un API para transmitir imágenes en tiempo real por internet, haciendo uso de la comunicación socketIO.

Pero antes de proseguir, quizás sea conveniente introducir algunos conceptos, que permitan al desarrollar contextualizar el presente módulo. Los apartados siguientes son de carácter opcional, y pretenden dar nociones básicas, de lo que implica la transmisión de video en tiempo real sobre una red.

## Introducción
Los transmisores de video, son algoritmos o programas encargados de enviar contenido multimedia a través de una red. Funcionan con dos apartados principalmente, un emisor y un receptor, de caracteristicas diversas. Los transmisores de video, pueden ser en tiempo real o proveedores de hosting.

!!! info

    En el presente contexto, nos referiremos a los transmisores de video en tiempo real.

El objetivo último de los transmisores de video es optimizar los recursos tanto de hardware como infraestructura de red para llevar a cabo su cometido. Siendo su principales contrincantes, los recursos de procesador, anchos de banda y la latencia.

!!! note "Nota"

    Entiendase como latencia, el retardo que existe en una red.

Los transmisores de video son programas complejos, cuyo soporte teórico posee una carga matemática elevada.

## Transcoders


## ¿Cómo se programa un transmisor de video?
Debido a que los programas de transmisión de video, requieren rápidez en sus computos, para lidiar así con la latencia, su programación se suele realizar en programas de bajo o medio nivel, compilados principalmente. Entre estos tenemos:

- C
- C++
- Java
- Golang

!!! info

    Python no es la mejor alternativa para desarrollar un transmisor de video, debido a la latencia que implica un lenguaje interpretado para este tipo de aplicaciones.

Lo anterior no implica que no se puedan programar transmisores de video en python, pero si nos dice que su rendimiento no será el óptimo.

## Formatos de Transmisión de video
Existen diversas técnicas para transmitir el video; en general los algoritmos con el mencionado fin, emplean métodos de comprensión y descompresión, para reducir así los recursos de red, y mejor la respuesta en latencia. 

Existen aquí algoritmos públicos y patentes que se adquieren dependiendo del uso.

## MJPEG
Motion - JPEG es un un protocolo/codec de transmisión de imágenes/video através de una red. Como su nombre indica, consiste en enviar secuencialmente cuadros en formato JPEG, que es un estándar de compresión de imágenes muy común. Por lo tanto es un codec relativamente simple, de fácil acceso, diversidad de ejemplos de uso en internet, y cuyo coste computacional es bajo.

Existen diversad formas de implementar este transmisor; algunas con servidores y demás

#### Pros
- Fácil de implementar
- Soportado por python.
- Permite implementar algoritmos de procesamiento de imágenes en tiempo real de forma sencilla.

#### Contras
- El uso ancho de banda puede ser excesivo.
- No permite la transmisión de audio.

