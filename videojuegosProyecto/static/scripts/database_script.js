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
                statusMessage.innerText = "✅ " + data.message;
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
