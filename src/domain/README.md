domain/ (El "Qué") [Domain-Driven Design (DDD) y Arquitectura Hexagonal]

Es el núcleo de tu negocio. Si mañana decides dejar de ser un gimnasio y pasar a ser una escuela, esta es la única carpeta que borrarías por completo.

    - Entities: Son los modelos de datos @dataclass. Representan los conceptos puros (Instructor, Rutina, Cliente). No saben nada de bases de datos ni de interfaces.
    - Interfaces (Repository ABCs): Aquí se definen las "reglas del juego": "Para que mi gimnasio funcione, necesito poder guardar rutinas", pero no se dice 'cómo'.

