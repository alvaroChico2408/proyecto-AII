document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("btn-cargar").addEventListener("click", function () {
        let button = this;
        button.disabled = true;  // Deshabilita el botón mientras se ejecuta la carga
        button.innerText = "Cargando...";

        fetch("/ejecutarCarga/", {
            method: "GET",
            headers: {
                "X-Requested-With": "XMLHttpRequest"
            }
        })
        .then(response => response.json())
        .then(data => {
            let statusMessage = document.getElementById("status-message");
            if (data.status === "success") {
                 // Actualizar contadores con los datos recibidos
                document.getElementById("juegos-contador").innerText = "Juegos insertados: " + data.juegos;
                document.getElementById("plataformas-contador").innerText = "Plataformas insertadas: " + data.plataformas;
                document.getElementById("desarrolladores-contador").innerText = "Desarrolladores insertados: " + data.desarrolladores;
                document.getElementById("companias-contador").innerText = "Compañías insertadas: " + data.companias;

                statusMessage.innerText = data.message;
                statusMessage.style.color = "green";
                button.innerText = "Carga completada";
            } else {
                statusMessage.innerText = "❌ Error: " + data.message;
                statusMessage.style.color = "red";
                button.innerText = "Intentar de nuevo";
                button.disabled = false;  // Reactiva el botón si hubo error
            }
        })
        .catch(error => {
            console.error("Error en la carga:", error);
            document.getElementById("status-message").innerText = "❌ Error al conectar con el servidor";
            button.innerText = "Intentar de nuevo";
            button.disabled = false;
        });
    });
});

// Botón de eliminar base de datos
document.getElementById("btn-eliminar").addEventListener("click", function () {
    let button = this;
    if (!confirm("¿Estás seguro de eliminar todos los datos de la base de datos? ¡Esta acción no se puede deshacer!")) {
        return;
    }

    button.disabled = true;
    button.innerText = "Eliminando...";

    fetch("/eliminarBaseDatos/", {
        method: "POST",
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCSRFToken()
        }
    })
    .then(response => response.json())
    .then(data => {
        let statusMessage = document.getElementById("status-message");
        if (data.status === "success") {
            statusMessage.innerText = "✅ Base de datos eliminada correctamente";
            statusMessage.style.color = "green";

            // Reiniciar contadores
            document.getElementById("juegos-contador").innerText = "Juegos insertados: 0";
            document.getElementById("plataformas-contador").innerText = "Plataformas insertadas: 0";
            document.getElementById("desarrolladores-contador").innerText = "Desarrolladores insertados: 0";
            document.getElementById("companias-contador").innerText = "Compañías insertadas: 0";

            button.innerText = "Base de Datos Eliminada";
        } else {
            statusMessage.innerText = "❌ Error al eliminar la base de datos: " + data.message;
            statusMessage.style.color = "red";
            button.innerText = "Intentar de nuevo";
            button.disabled = false;
        }
    })
    .catch(error => {
        console.error("Error en la eliminación:", error);
        document.getElementById("status-message").innerText = "❌ Error al conectar con el servidor";
        statusMessage.style.color = "red";
        button.innerText = "Intentar de nuevo";
        button.disabled = false;
    });


// Función para obtener el CSRF Token de las cookies
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
