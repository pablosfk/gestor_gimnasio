infrastructure/ (El "Con qué tecnología") [Domain-Driven Design (DDD) y Arquitectura Hexagonal]

Aquí vive todo lo que es ajeno a tu lógica de negocio y que depende de librerías externas.

    - Repositories: Las implementaciones reales (SQLite, PostgreSQL, Firestore).
    - Por qué se separa: Es la capa más volátil. Las tecnologías mueren o se actualizan. Al tenerlas aquí, si SQLite deja de ser útil, "se extirpa" este archivo y se pone otro sin romper el cerebro (Application) ni el corazón (Domain) de tu app.