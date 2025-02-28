# Gestor de Pomodoros para NVDA

## Descripción

**Gestor de Pomodoros** es un complemento para el lector de pantalla NVDA que implementa la técnica Pomodoro, ayudando a los usuarios a gestionar su tiempo de trabajo y descanso de forma efectiva. La técnica Pomodoro consiste en dividir el tiempo de trabajo en bloques (tradicionalmente de 25 minutos), separados por breves descansos. Este complemento es ideal para usuarios que buscan mejorar su productividad y manejar mejor su tiempo mientras utilizan NVDA.

## Cómo Funciona

Una vez activado, el complemento permite al usuario iniciar, pausar, reanudar o detener el temporizador Pomodoro mediante atajos de teclado específicos. Además, proporciona retroalimentación auditiva y verbal al inicio y al final de cada sesión de trabajo o descanso. El complemento administra automáticamente los ciclos de trabajo y descanso, incluyendo descansos largos después de cada cuatro ciclos de trabajo completados.

### Atajos de teclado
Los atajos de teclado deben assignarse desde la opción gestos de entrada del menú Preferencias de NVDA. Las opciones se pueden encontrar bajo la categoría Gestor de pomodoros.

## Lista de cambios
### 1.15
- Actualizada la traducción al ruso. [PR #3](https://github.com/jpavonabian/gestor-de-Pomodoros/pull/3)

### 1.14
- Añadida la traducción al ruso. Gracias, [Валентин Куприянов: Русский язык](https://nvda.ru/)
### 1.13
Añadida documentación en inglés.
### 1.12
Añadida traducción al inglés.
### 1.11
Actualizada la versión última de testeo de NVDA.
### 1.10
- Arreglado un eror que seguía haciendo avanzar el tiempo aunque un pomodoro estuviese pausado.

### 1.9
- Cambiado el nombre interno del complemento para evitar problemas con la tienda oficial.

### 1.8
- Solucionado un error de Braille y los mensajes.
- Solucionado un error con la gestión de tiempo.
- Cambiado mucho código interno.

### 1.7
- Arreglado un error con el canal de distribución.
- Arreglado un bug cuando intentabas detener un pomodoro que no había sido iniciado antes.

### 1.6
- Cambiada la duración y la frecuencia de los tonos.
- Ahora los mensajes del complemento tienen prioridad alta, de forma que no se pierdan si se está haciendo otra cosa.
- Ahora los tonos no se escuchan por el canal derecho, era un error.

### 1.5
- Los atajos de teclado se han eliminado. Deben asignarse por el usuario.

### 1.4
- Cambiados los atajos de teclado para que sea más intuitivo.
- Retocado un poco el código interno.
- Ahora los atajos aparecen bien en las categorías de gestos.

### 1.3
- Ahora los gestos de entrada pueden reasignarse bajo la categoría "Gestor de pomodoros". [PR #1](https://github.com/jpavonabian/Gestor-de-Pomodoros/pull/1)
### 1.2
- Se arregla el tratamiento interno del complemento por NVDA.
### 1.1
- El complemento no se ejecuta en pantallas seguras.
- Se automatiza la liberación con GitHub Actions.

### 1.0

- Versión inicial del complemento.
- Implementación de la funcionalidad básica de Pomodoro, incluyendo inicio, pausa, reanudación, y detención del temporizador.
- Anuncios auditivos y verbales para el inicio y fin de las sesiones de trabajo y descanso.

## Agradecimientos especiales
- A Sukil Etxenike <sukiletxe@yahoo.es> por ponerme en el camino correcto cuando por falta de experiencia en el desarrollo de complementos no sabía por dónde tirar.
- A Ángel Alcántar <rayoalcantar@gmail.com> por echarle un ojo al código.
- A Noelia Ruiz Martínez <nrm1977@gmail.com> por el Feedback que está dando con respecto al código y por aguantar tantísima duda de novato.

