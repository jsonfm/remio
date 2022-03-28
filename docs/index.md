<div align="center"> <h1>RemIO</h1> </div>
## Introducción

<div style="text-align: justify">
<b>RemIO</b> es un módulo de python destinado al desarrollo de dispositivos IoT, basados en comunicación <i>serial</i>, comunicación socketIO y procesamiento de imágenes, que permite integrar hardware y software vario, con <u>interfaces gráficas</u>, <u>control remoto</u> y <u>transmisión de video</u>, empleando para ello, librerías tan comunes como:
</div>

<ul>
<li>OpenCV</li>
<li>PySerial</li>
<li>SocketIO</li>
</ul>

## Arquitectura
<div style="text-align: justify">
En el presente contexto, este software pretende agilizar la producción de dispositvos electrónicos cuya arquitectura sea afin a la siguiente propuesta:
</div>
<br>
<img src="/assets/images/arch-1.png" alt="arch-1">
<div align="center"><b>Figura.</b> Arquitectura propuesta para el uso de la librería</div>
<br>
<div style="text-align: justify">
<b>`COMPUTADOR`</b>: Se encarga de manejar la complejidad que pueda acarrear un cierto proyecto, como pueden ser sus algoritmos de procesamiento, o la comunicación con servidores en internet.
<br>
<br>
<b>`MICROCONTROLADOR`</b>: Interactúa con dipositivos de control, como pueden ser actuadores.
<br>
<br>
<b>`INTERFAZ GRÁFICA`</b>: Es un apartado visual que se puede desarrollar con varios frameworks como son PyQt5, Tkinter, Kivy.
<br>
<br>
<b>`PERIFÉRICOS`</b>: Son diversos dispositivos que se pueden conectar directamente al computador.
<br>
<br>
<b>`MICROCONTROLADOR`</b>: Interactúa con dipositivos de control, como pueden ser actuadores.
<hr>

</div>
<div style="text-align: justify">
Esta distribución de componentes es práctica para el desarrollo de prototipos que demandan cierta complejidad de procesamiento, como puede ser el caso de un <b>robot</b>, un algoritmo de <b>IA</b> y cualquier otra posibilidad que este al alcance de esta combinación.
</div>

## Caracteristicas

Las principales caracteristicas del software son:

<ul>
<li>Manejo de múltiples cámaras a través de hilos.</li>
<li>Uso de callbacks y eventos.</li>
<li>API para incluir funciones de procesamiento de video.</li>
<li>Manejo de múltiples dispositivos seriales a través de hilos.</li>
<li>Manejo síncrono y asíncrono de SocketIO.</li>
<li>Transmisión de video MJPEG a través de SocketIO.</li>

</ul>

## Instalación

1.- Cree un entorno virutal:
```sh
python3 -m venv venv
```
2.- Active el entorno virtual:
```
source venv/bin/activate
```
3.- Clone el repositorio e instale el paquete:
```
git clone https://github.com/Hikki12/camio && cd camio

pip install -U .
```

## Primeros Pasos
Realizada la instalación del presente módulo, te sugerimos revisar alguno de los siguientes apartados:
<ul>
<li>Ejemplos</li>
</ul>
<br>
<br>