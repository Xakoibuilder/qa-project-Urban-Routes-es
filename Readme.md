# Urban Routes - Pruebas Automatizadas

## Descripción del Proyecto

Este proyecto contiene pruebas automatizadas para la aplicación **Urban Routes**, una plataforma de transporte que permite a los usuarios solicitar taxis con diferentes servicios adicionales.

Las pruebas cubren el flujo completo de solicitud de un taxi, desde la configuración de la ruta hasta la asignación del conductor, incluyendo:
- Configuración de direcciones de origen y destino
- Selección de tarifa Comfort
- Registro de número de teléfono con verificación por SMS
- Agregación de método de pago (tarjeta de crédito)
- Especificación de preferencias (mensaje para conductor, manta y pañuelos, helados)
- Solicitud y seguimiento del taxi

## Tecnologías y Técnicas Utilizadas

### Tecnologías
- **Python 3.x**: Lenguaje de programación principal
- **Selenium WebDriver**: Automatización de navegador web
- **ChromeDriver**: Controlador para navegador Google Chrome
- **pytest**: Framework de pruebas (opcional para ejecución)

### Patrones y Técnicas
- **Page Object Model (POM)**: Patrón de diseño para organizar el código de pruebas
  - Separación clara entre lógica de página y casos de prueba
  - Reutilización de elementos y métodos
  - Mantenibilidad mejorada
  
- **Esperas Explícitas**: Uso de `WebDriverWait` para manejar tiempos de carga dinámicos
  
- **Localizadores**: Estrategias de localización mediante:
  - ID
  - XPath
  - CSS Selectors
  - Class Name

- **Interceptación de Logs**: Captura de código de verificación telefónico desde logs de rendimiento del navegador

## Estructura del Proyecto
urban-routes-tests/
main.py # Clases POM y casos de prueba
data.py # Datos de prueba (URLs, credenciales, etc.)
README.md # Documentación del proyecto
