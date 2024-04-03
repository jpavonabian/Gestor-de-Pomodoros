# Gestor de Pomodoros para NVDA

## Descripción

**Gestor de Pomodoros** es un complemento para el lector de pantalla NVDA que implementa la técnica Pomodoro, ayudando a los usuarios a gestionar su tiempo de trabajo y descanso de forma efectiva. La técnica Pomodoro consiste en dividir el tiempo de trabajo en bloques (tradicionalmente de 25 minutos), separados por breves descansos. Este complemento es ideal para usuarios que buscan mejorar su productividad y manejar mejor su tiempo mientras utilizan NVDA.

## Cómo Funciona

Una vez activado, el complemento permite al usuario iniciar, pausar, reanudar o detener el temporizador Pomodoro mediante atajos de teclado específicos. Además, proporciona retroalimentación auditiva y verbal al inicio y al final de cada sesión de trabajo o descanso.

- Para **iniciar o reanudar** el Pomodoro, y para **reportar el estado** del temporizador si ya está en marcha pulse el atajo de teclado `NVDA + SHIFT + P`.
- Para **pausar** el Pomodoro, pulse `NVDA + SHIFT + P` dos veces rápidamente.
- Para **detener** el Pomodoro pulse el atajo de teclado `NVDA + CTRL + SHIFT + P`.

El complemento administra automáticamente los ciclos de trabajo y descanso, incluyendo descansos largos después de cada cuatro ciclos de trabajo completados.

## Changelog

### 1.1
- El complemento no se ejecuta en pantallas seguras.
- Se automatiza la liberación con GitHub Actions.

### 1.0

- Versión inicial del complemento.
- Implementación de la funcionalidad básica de Pomodoro, incluyendo inicio, pausa, reanudación, y detención del temporizador.
- Anuncios auditivos y verbales para el inicio y fin de las sesiones de trabajo y descanso.
