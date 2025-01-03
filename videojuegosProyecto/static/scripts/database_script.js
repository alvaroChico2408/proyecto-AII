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
