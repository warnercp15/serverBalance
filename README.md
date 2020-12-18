# Server Balance

**Enlace de la aplicación Web: https://webscrapinggames.web.app/**

El objetivo del proyecto consiste en hacer uso de conceptos de sistemas distribuidos a través de orquestación de nodos y servidores de colas. Por lo cual se tomó como refencia el proyecto anterior: https://github.com/warnercp15/webScrapingGames

**Resultado**

![vistaWeb](<./assets/result.jpeg>)


En esta versión podemos encontrar los diferentes tipos de Scraping de forma modularizada e independiente, esto pues ahora  realizarán tareas específicas. Puedes ver los diferentes modulos en la carpeta 'modules', estos de igual manera están desarrollados en su mayoría en C#, pero ejecutados ahora desde clientes de SocketIO realizados en Python. La comunidación entre el servidor y los clientes se realiza por medio Sockets para aprovechar los eventos en tiempo real.

**El proyecto funciona de la siguiente manera:**

1. El servidor es el encargado de administrar las conexiones (clientes) y asignar tareas a quien esté disponible.

2. Cuando el servidor ordene realizar una tarea, cada cliente ejecutará el Scraping correspondiente y enviará los datos obtenidos al mismo servidor cuando estén disponibles.

3. Se pueden conectar los clientes que se deseen, sin importar que sean del mismo tipo, pues acá hablamos de tareas disponibles. Por lo que entre más clientes se conecten más rapido terminarán las tareas (las tareas serán distribuidas entre todos los clientes conectados). Cuando un cliente termine una tarea, verificará si existen más tareas para ejecutar, de no existir más tareas quedará en un modo disponible o en espera para cuando hayan más.

![multiClientes](<./assets/processing.jpeg>)

4. Conforme se están obteniendo los datos se va verificando qué paquetes están completos para ser agregados a la lista de juegos para consultar (desde la vista del Frontend).

5. Cada vez que se inicie la vista del Frontend se ejecutará el evento que pondrá a todos los clientes conectados a trabajar.

6. Se cuenta con un registro de los correos electrónicos que deseen ser notificados de las últimas actualizaciones, por lo que cuándo se actualicen los datos se les enviará una notificación via Gmail sobre los nuevos datos a todos los correos previamente registrados en el Frontend. 

![multiClientes](<./assets/register.jpeg>)

**Resultado de Gmail recibido**
![multiClientes](<./assets/mail.jpeg>)
