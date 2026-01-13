application/ (El "Cómo funciona el negocio") [Domain-Driven Design (DDD) y Arquitectura Hexagonal]

Es la capa de los Casos de Uso. Aquí es donde se define el flujo de trabajo.

    - Services: Aquí vive la lógica que coordina. Por ejemplo: "Para registrar un cliente, primero busca si el instructor existe, luego verifica la rutina y, si todo está bien, guárdalo".
    - Por qué se separa: Porque esta capa actúa como un puente. No le importa si el clic vino de una App móvil, una web o la GUI de escritorio; el proceso de "Registrar Cliente" es siempre el mismo.