# Project Architecture Rules

## Feature Definition

- A feature represents a business capability and must be identified by its directory name, for example `auth` or `user`.
- Organize each feature into three layers: `api`, `application`, and `infrastructure`.

## Feature Structure

Use the following structure for every feature:

```text
<feature>/
├── api/
│   ├── <version>/                 # For example, v1
│   │   ├── schemas/               # Pydantic schemas
│   │   ├── router.py              # FastAPI APIRouter and endpoint registration
│   │   └── converters/            # Pydantic schemas -> application DTOs
│   └── depends/                   # Shared FastAPI dependencies
├── application/
│   ├── converters/                # Conversion of DTOs imported from shared features
│   ├── dto/                       # Application DTOs
│   ├── ports/                     # Service interfaces
│   └── use_cases/                 # Use cases
└── infrastructure/
    ├── adapters/                   # Implementations of application ports
    ├── models/                     # SQLAlchemy models
    ├── converters/                 # Infrastructure models -> application DTOs
    └── di/
        └── register.py             # Interface-to-implementation registration
```

### API Layer

- Put every API version in its own directory, for example `api/v1`.
- Put Pydantic request and response schemas in `api/<version>/schemas`.
- Define the FastAPI `APIRouter` and register endpoints in `api/<version>/router.py`.
- Put conversions from Pydantic schemas to `application.dto` objects in `api/<version>/converters`.
- Put reusable FastAPI `Depends` providers in `api/depends`. These are normally guards, request-parameter dependencies, and utility dependencies that are specific to FastAPI.

### Application Layer

- Put DTOs in `application/dto`.
- Put service interfaces in `application/ports`.
- Put use cases in `application/use_cases`.
- Use `application/converters` only when a DTO imported from a shared feature must be converted into the current feature's DTO.
- Name cross-feature DTO converter files `<source_feature>_<target_feature>.py`. For example, a converter from an `auth` DTO to a `user` DTO must be named `auth_user.py`.

### Infrastructure Layer

- Put concrete implementations of application ports in `infrastructure/adapters`.
- Put SQLAlchemy models in `infrastructure/models`.
- Register SQLAlchemy models centrally in `setup.db.models`.
- Put conversions from infrastructure models to `application.dto` objects in `infrastructure/converters`.
- Register concrete implementations against their interfaces in `infrastructure/di/register.py`.

## Import Rules

1. Code in the `application` layer must not import from the `api` or `infrastructure` layers.
2. A feature must not import from another feature.
3. The only exception to the cross-feature import rule is an import from a feature located under `shared`.
4. Even for shared features, a feature's `application` layer may import only:
   - ports, normally from code in `application/use_cases`;
   - DTOs, and only from code in `application/converters`.
5. Modules in `shared.contrib.utils` may be imported freely by layers other than `application`. The `application` layer may import only application-specific utilities from `shared.contrib.application`.
6. `contrib` is the common location for shared foundations such as base classes and other reusable building blocks.
7. Whenever possible, code in the `api` and `infrastructure` layers must import shared code only from the corresponding layer of a shared feature:
   - `api` imports from shared `api`;
   - `infrastructure` imports from shared `infrastructure`.
8. If following the same-layer import rule is not practical, ask the developer for permission or architectural guidance before introducing the import.

## Dependency Inversion Rules

1. Every use case must depend on an interface for each service it requires, rather than on a concrete implementation.
2. Every service interface must be defined in the feature's `application/ports` directory.
3. Every service interface must have a corresponding implementation in the same feature's `infrastructure/adapters` directory.
4. For every feature outside `shared`, register each service interface and its concrete implementation in:

   ```python
   def register_dependencies(container: Container) -> None: ...
   ```

   Define this function in `features/<feature>/infrastructure/di/register.py`.
5. Invoke every feature's `register_dependencies` function from `setup.di.ioc`.
