gui/ (o presentation/) [Domain-Driven Design (DDD) y Arquitectura Hexagonal]

Es la capa que interactúa con el humano.

    - Views/Forms: Todo lo relacionado con botones, colores y layouts.
    - Styles: Todo lo relacionado con colores, fuentes y layouts.
    - Assets: Todo lo relacionado con imágenes, iconos y archivos estáticos como fuentes.
    - Controllers:  Todo lo relacionado con eventos y lógica de la GUI. Es la interfaz entre la GUI y el Servicio que entrega y recibe datos,
                    pero también observa los cambios para reflejarlos en la GUI que ahora en flet es reactiva en tiempo real.
    - Por qué se separa: Para que tu lógica de negocio sea "descabezada". Podrías ejecutar todo tu gimnasio desde una consola de comandos (terminal) sin tocar una sola línea de los Servicios, porque la lógica no depende de la ventana.