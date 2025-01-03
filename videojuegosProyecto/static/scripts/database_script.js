document.addEventListener("DOMContentLoaded", function () {
    let btnCargar = document.getElementById("btn-cargar");
    let btnEliminar = document.getElementById("btn-eliminar");
    let statusMessage = document.getElementById("status-message");

    // Función para verificar si hay datos en la base de datos
    function verificarEstadoBaseDatos() {
        fetch("/verificarEstadoBD/", {
            method: "GET",
            headers: {
                "X-Requested-With": "XMLHttpRequest"
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.hay_datos) {
                btnCargar.disabled = true;
                btnCargar.innerText = "Carga Completada";
                btnEliminar.innerText = "Eliminar base de datos";
                btnEliminar.disabled = false;

                document.getElementById("juegos-contador").innerText = "Juegos insertados: " + data.juegos;
                document.getElementById("plataformas-contador").innerText = "Plataformas insertadas: " + data.plataformas;
                document.getElementById("desarrolladores-contador").innerText = "Desarrolladores insertados: " + data.desarrolladores;
                document.getElementById("companias-contador").innerText = "Compañías insertadas: " + data.companias;
            } else {
                btnCargar.disabled = false;
                btnCargar.innerText = "Cargar Base de Datos";
                btnEliminar.innerText = "Base de datos eliminada";
                btnEliminar.disabled = true;

                document.getElementById("juegos-contador").innerText = "Juegos insertados: 0";
                document.getElementById("plataformas-contador").innerText = "Plataformas insertadas: 0";
                document.getElementById("desarrolladores-contador").innerText = "Desarrolladores insertados: 0";
                document.getElementById("companias-contador").innerText = "Compañías insertadas: 0";
            }
        })
        .catch(error => console.error("Error verificando la base de datos:", error));
    }

    verificarEstadoBaseDatos(); // Verificar el estado al cargar la página

    // Botón de carga de la base de datos
    btnCargar.addEventListener("click", function () {
        btnCargar.disabled = true;
        btnCargar.innerText = "Cargando...";

        fetch("/ejecutarCarga/", {
            method: "GET",
            headers: {
                "X-Requested-With": "XMLHttpRequest"
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                statusMessage.innerText = "✅ Base de datos cargada correctamente";
                statusMessage.style.color = "green";

                // Actualizar contadores
                document.getElementById("juegos-contador").innerText = "Juegos insertados: " + data.juegos;
                document.getElementById("plataformas-contador").innerText = "Plataformas insertadas: " + data.plataformas;
                document.getElementById("desarrolladores-contador").innerText = "Desarrolladores insertados: " + data.desarrolladores;
                document.getElementById("companias-contador").innerText = "Compañías insertadas: " + data.companias;

                // Bloquear botón de carga y habilitar el de eliminar
                btnCargar.innerText = "Carga Completada";
                btnEliminar.innerText = "Eliminar base de datos";
                btnEliminar.disabled = false;
            } else {
                statusMessage.innerText = "❌ Error: " + data.message;
                statusMessage.style.color = "red";
                btnCargar.innerText = "Intentar de nuevo";
                btnCargar.disabled = false;
            }
        })
        .catch(error => {
            console.error("Error en la carga:", error);
            statusMessage.innerText = "❌ Error al conectar con el servidor";
            btnCargar.innerText = "Intentar de nuevo";
            btnCargar.disabled = false;
        });
    });

    // Botón de eliminar base de datos
    btnEliminar.addEventListener("click", function () {
        if (!confirm("⚠️ ¿Estás seguro de eliminar todos los datos? Esta acción no se puede deshacer.")) {
            return;
        }

        btnEliminar.disabled = true;
        btnEliminar.innerText = "Eliminando...";

        fetch("/eliminarBaseDatos/", {
            method: "POST",
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": getCSRFToken()
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                statusMessage.innerText = "✅ Base de datos eliminada correctamente";
                statusMessage.style.color = "red";

                // Reiniciar contadores
                document.getElementById("juegos-contador").innerText = "Juegos insertados: 0";
                document.getElementById("plataformas-contador").innerText = "Plataformas insertadas: 0";
                document.getElementById("desarrolladores-contador").innerText = "Desarrolladores insertados: 0";
                document.getElementById("companias-contador").innerText = "Compañías insertadas: 0";

                // Deshabilitar botón de eliminar y reactivar el de carga
                btnEliminar.innerText = "Base de Datos Eliminada";
                btnCargar.disabled = false;
                btnCargar.innerText = "Cargar Base de Datos";
            } else {
                statusMessage.innerText = "❌ Error: " + data.message;
                statusMessage.style.color = "red";
                btnEliminar.innerText = "Intentar de nuevo";
                btnEliminar.disabled = false;
            }
        })
        .catch(error => {
            console.error("Error en la eliminación:", error);
            statusMessage.innerText = "❌ Error al conectar con el servidor";
            btnEliminar.innerText = "Intentar de nuevo";
            btnEliminar.disabled = false;
        });
    });

    // Función para obtener CSRF Token
    function getCSRFToken() {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.startsWith("csrftoken=")) {
                return cookie.substring("csrftoken=".length, cookie.length);
            }
        }
        return "";
    }
});
