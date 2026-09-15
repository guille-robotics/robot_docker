# Entorno de Teleoperación y RL con ROS 2 (Raspberry Pi 5)

Este repositorio contiene la infraestructura basada en Docker para ejecutar un entorno de ROS 2 (Humble) de forma nativa en una Raspberry Pi 5. Está preparado para el desarrollo de agentes de Reinforcement Learning en Python, manejo de cámara y teleoperación remota.

---

## 💻 1. Conexión Remota desde el PC (VS Code)

Para desarrollar cómodamente sin conectar un monitor a la Raspberry Pi, utilizamos la conexión remota por SSH a través de Visual Studio Code.

### Requisitos previos en tu PC principal:
1. Instalar **Visual Studio Code**.
2. Instalar la extensión **Remote - SSH** (desarrollada por Microsoft).

### Paso a paso para conectar:
1. Abre VS Code en tu PC.
2. Haz clic en el ícono verde con los símbolos `><` en la esquina inferior izquierda.
3. Selecciona **Connect to Host...** > **Add New SSH Host...**
4. Ingresa el comando de conexión. Por ejemplo:
   `ssh robotpilot@192.168.1.78` *(Asegúrate de usar la IP actual de tu Raspberry).*
5. Selecciona el archivo de configuración por defecto y haz clic en **Connect** en la notificación emergente.
6. Selecciona el sistema operativo **Linux** e ingresa la contraseña de tu usuario cuando se solicite.
7. Una vez conectado, ve al menú **File > Open Folder...** y escribe la ruta exacta del proyecto: `/home/robotpilot/robot_docker`.

---

## 🐳 2. Uso del Entorno Docker (ROS 2)

El código fuente (Python, Nodos de ROS 2) se almacena en la Raspberry Pi, pero se compila y ejecuta dentro del contenedor de Docker para mantener el sistema operativo base limpio.

### Iniciar el contenedor
Abre una terminal integrada en VS Code (`Ctrl + ñ` o `Terminal > New Terminal`) y ejecuta:
```bash
# Construye y levanta el contenedor en segundo plano
docker compose up -d --build