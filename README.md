# SystemCarpet

## Instalación

Para instalar y ejecutar este proyecto, sigue los siguientes pasos:

1. Clona el repositorio en tu máquina local:

```bash
git clone https://github.com/Kurai2610/system-carpet
```

2. Navega al directorio del proyecto:

```bash
cd system-carpet
```

3. Asegúrate de estar en la rama correcta del proyecto:

```bash
git checkout backend/django_graphql
```

4. A continuación, navega a la carpeta `server` donde se encuentra el archivo `requirements.txt`:

```bash
cd server
```

5. Crea un entorno virtual para el proyecto:

```bash
python -m venv venv
```

6. Activa el entorno virtual:

- En Windows:

```bash
.\venv\Scripts\activate
```

- En Unix o MacOS:

```bash
source venv/bin/activate
```

7. Instala las dependencias del proyecto utilizando `pip`:

```bash
pip install -r requirements.txt
```

8. Copia el archivo `.env.example` a un nuevo archivo llamado `.env` y modifica las variables de entorno según sea necesario para tu configuración local:

- En Windows:

```bash
copy .env.example .env
```

- En Unix o MacOS:

```bash
cp .env.example .env
```

9. Realiza las migraciones necesarias para configurar la base de datos de Django:

```bash
python manage.py makemigrations
python manage.py migrate
```

10. Crea los grupos de permisos necesarios para el proyecto:

```bash
python manage.py create_groups_permissions
```

## API GraphQL

La API GraphQL está disponible en `/graphql/` y puedes explorarla usando GraphiQL.

### Filtros Comunes

Al trabajar con las consultas de la API, puedes usar los siguientes filtros para refinar tus resultados. Estos filtros son aplicables a muchas consultas y proporcionan flexibilidad en la búsqueda de datos. El nombre `field` en cada filtro es un ejemplo y va a depender del modelo al que se le haga la consulta.

- **`field_Icontains`**: Filtra los resultados para que incluyan valores en el campo especificado que contengan la cadena dada. La búsqueda no es sensible a mayúsculas o minúsculas.

  - **Ejemplo:** `field_Icontains: "valor"`

- **`field`**: Filtra los resultados para que incluyan valores en el campo especificado que sean exactamente iguales al valor dado.

  - **Ejemplo:** `field: "valor"`

- **`field_Gt`**: Filtra los resultados para que incluyan valores en el campo especificado que sean mayores que el valor dado.

  - **Ejemplo:** `field_Gt: 10`

- **`field_Gte`**: Filtra los resultados para que incluyan valores en el campo especificado que sean mayores o iguales al valor dado.

  - **Ejemplo:** `field_Gte: 10`

- **`field_Lt`**: Filtra los resultados para que incluyan valores en el campo especificado que sean menores que el valor dado.

  - **Ejemplo:** `field_Lt: 10`

- **`field_Lte`**: Filtra los resultados para que incluyan valores en el campo especificado que sean menores o iguales al valor dado.

  - **Ejemplo:** `field_Lte: 10`

- **`offset`**: Especifica el número de elementos a omitir antes de empezar a retornar resultados. Esto puede ser útil en combinación con la paginación para obtener resultados a partir de un punto específico.
  - **Ejemplo:** `offset: 10`

## Paginación y Estructura de Resultados

La API utiliza un sistema de paginación basado en cursors para facilitar la navegación a través de grandes conjuntos de datos.

### Paginación

La paginación se maneja a través de los argumentos `after`, `before`, `first`, y `last`:

- **`after`** (opcional): Cursor que indica el punto a partir del cual empezar a retornar los resultados. Utilizado para la paginación hacia adelante.
- **`before`** (opcional): Cursor que indica el punto hasta el cual retornar los resultados. Utilizado para la paginación hacia atrás.
- **`first`** (opcional): Número máximo de elementos a retornar después del cursor `after`. Utilizado para limitar la cantidad de resultados hacia adelante.
- **`last`** (opcional): Número máximo de elementos a retornar antes del cursor `before`. Utilizado para limitar la cantidad de resultados hacia atrás.

### Estructura de Resultados

Las respuestas de las consultas paginadas tienen la siguiente estructura:

- **`edges`**: Una lista de objetos `Edge` que contienen:

  - **`cursor`**: Un string que representa la posición del elemento en la lista. Este cursor puede ser usado para paginación en consultas posteriores.
  - **`node`**: El objeto real con los datos solicitados.

- **`pageInfo`**: Información sobre el estado de la paginación:
  - **`endCursor`**: Cursor al final de la página actual. Puede ser utilizado como argumento `before` en una consulta siguiente para obtener los resultados anteriores.
  - **`hasNextPage`**: Booleano que indica si hay más resultados disponibles hacia adelante.
  - **`hasPreviousPage`**: Booleano que indica si hay más resultados disponibles hacia atrás.
  - **`startCursor`**: Cursor al inicio de la página actual. Puede ser utilizado como argumento `after` en una consulta siguiente para obtener los resultados siguientes.

### Consultas

#### Direcciones

##### `localities`

Retorna una lista paginada de localidades con soporte para filtros.

**Argumentos de consulta:**

- `after`
- `before`
- `first`
- `last`
- `name_Icontains`
- `name`
- `offset`

Para más información revisar [Filtros Comunes](#filtros-comunes) y [Paginación](#paginación).

**Datos que retorna:**

- `edges`
  - `cursor`
  - `node`
    - `id`: ID de la localidad en formato Global ID.
    - `name`: Nombre de la localidad.
  - `pageInfo`
    - `endCursor`
    - `hasNextPage`
    - `hasPreviousPage`
    - `startCursor`

Para más información revisar [Estructura de resultados](#estructura-de-resultados).

**Ejemplo de consulta:**

```graphql
query {
  localities(
    after: ""
    before: ""
    first: 10
    last: 10
    name_Icontains: ""
    name: ""
    offset: 10
  ) {
    edges {
      cursor
      node {
        id
        name
      }
    }
    pageInfo {
      endCursor
      hasNextPage
      hasPreviousPage
      startCursor
    }
  }
}
```

##### `locality`

Retorna una localidad especifica.

**Datos que retorna**

- `id`: id de la localidad.
- `name`: nombre de la localidad.

**Argumentos de consulta**

- `id`: id de la localidad a consultar.

**Ejemplo de consulta:**

```graphql
query {
  locality(id: 1) {
    id
    name
  }
}
```

##### `neighborhoods`

Retorna una lista paginada de barrios con soporte para filtros.

**Argumentos de consulta:**

- `after`
- `before`
- `first`
- `last`
- `locality`: Filtra por el `id` de una localidad.
- `name_Icontains`
- `name`
- `offset`

Para más información revisar [Filtros Comunes](#filtros-comunes) y [Paginación](#paginación).

**Datos que retorna:**

- `edges`
  - `cursor`
  - `node`
    - `id`: ID del barrio en formato Global ID.
    - `locality`: Datos de la [localidad](#locality) asociada.
    - `name`: Nombre del barrio.
  - `pageInfo`
    - `endCursor`
    - `hasNextPage`
    - `hasPreviousPage`
    - `startCursor`

Para más información revisar [Estructura de resultados](#estructura-de-resultados).

**Ejemplo de consulta:**

```graphql
query {
  neighborhoods(
    after: ""
    before: ""
    first: 10
    last: 10
    locality: ""
    name: ""
    name_Icontains: ""
    offset: 10
  ) {
    edges {
      cursor
      node {
        id
        locality {
          id
          name
        }
        name
      }
    }
    pageInfo {
      endCursor
      hasNextPage
      hasPreviousPage
      startCursor
    }
  }
}
```

##### `neighborhood`

Retorna un barrio especifica.

**Datos que retorna**

- `id`: id del barrio.
- `locality`: Datos de la [localidad](#locality) asociada.
- `name`: nombre del barrio.

**Argumentos de consulta**

- `id`: id del barrio a consultar.

**Ejemplo de consulta:**

```graphql
query {
  neighborhood(id: "") {
    id
    locality {
      id
      name
    }
    name
  }
}
```

##### `addresses`

Retorna una lista paginada de direcciones con soporte para filtros.

**Argumentos de consulta:**

- `after`
- `before`
- `details`: Filtra por los detalles de la dirección.
- `details_Icontains`: Filtra por los detalles de la dirección que contengan la cadena dada.
- `first`
- `last`
- `neighborhood`: Filtra por el `id` de un barrio.
- `offset`

Para más información revisar [Filtros Comunes](#filtros-comunes) y [Paginación](#paginación).

**Datos que retorna:**

- `edges`
  - `cursor`
  - `node`
    - `id`: ID de la dirección en formato Global ID.
    - `details`: Detalles de la dirección.
    - `neighborhood`: Datos del [barrio](#neighborhood) asociado.
  - `pageInfo`
    - `endCursor`
    - `hasNextPage`
    - `hasPreviousPage`
    - `startCursor`

Para más información revisar [Estructura de resultados](#estructura-de-resultados).

**Ejemplo de consulta:**

```graphql
query MyQuery {
  addresses(
    after: ""
    before: ""
    details: ""
    details_Icontains: ""
    first: 10
    last: 10
    neighborhood: ""
    offset: 10
  ) {
    edges {
      cursor
      node {
        details
        id
        neighborhood {
          id
          locality {
            id
            name
          }
          name
        }
      }
    }
    pageInfo {
      endCursor
      hasNextPage
      hasPreviousPage
      startCursor
    }
  }
}
```

##### `address`

Retorna una dirección especifica.

**Datos que retorna**

- `id`: id de la dirección.
- `details`: detalles de la dirección.
- `neighborhood`: Datos del [barrio](#neighborhood) asociado.

**Argumentos de consulta**

- `id`: id de la dirección a consultar.

**Ejemplo de consulta:**

```graphql
query {
  address(id: "") {
    details
    id
    neighborhood {
      id
      locality {
        id
        name
      }
      name
    }
  }
}
```
