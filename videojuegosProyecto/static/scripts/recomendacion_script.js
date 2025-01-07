document.addEventListener("DOMContentLoaded", function () {
    document.addEventListener("click", function (event) {
        if (event.target.classList.contains("recomendar-btn")) {
            let juegoBase = event.target.getAttribute("data-title"); // Obtener el nombre del juego
            window.location.href = `/recomendaciones/?title=${encodeURIComponent(juegoBase)}`;
        }
    });
});

document.addEventListener("DOMContentLoaded", function () {
    // Obtener el parámetro del título del juego desde la URL
    const urlParams = new URLSearchParams(window.location.search);
    const juegoBase = urlParams.get("title");

    if (!juegoBase) {
        document.getElementById("resultado-recomendaciones").innerHTML = 
            "<p class='error-text'>❌ No se encontró el juego base para generar recomendaciones.</p>";
        return;
    }

    // Mostrar el nombre del juego base en la página
    document.getElementById("juego-base").innerText = juegoBase;

    // Hacer la petición para obtener recomendaciones
    fetch(`/obtener_recomendaciones/?title=${encodeURIComponent(juegoBase)}`, {
        method: "GET",
        headers: {
            "X-Requested-With": "XMLHttpRequest"
        }
    })
    .then(response => response.json())
    .then(data => {
        let resultadoDiv = document.getElementById("resultado-recomendaciones");
        resultadoDiv.innerHTML = ""; // Limpiar el mensaje de carga

        if (data.length === 0) {
            resultadoDiv.innerHTML = "<p class='error-text'>❌ No se encontraron recomendaciones.</p>";
        } else {
            let lista = document.createElement("ul");
            lista.style.listStyle = "none";
            lista.style.padding = "0";

            data.forEach(juego => {
                let item = document.createElement("li");
                item.innerHTML = `
                    <p style="font-size: 14px; line-height: 1.4em;">
                        <strong style="color: #D100D1;">Nombre:</strong> <span style="color: #00BFFF;">${juego.title}</span> <br>
                        <strong style="color: #D100D1;">Similitud:</strong> <span style="color: #00BFFF;">${juego.similitud}%</span> <br>
                        <strong style="color: #D100D1;">Año:</strong> <span style="color: #00BFFF;">${juego.year}</span> <br>
                        <strong style="color: #D100D1;">Compañías:</strong> <span style="color: #00BFFF;">${juego.companies}</span> <br>
                        <strong style="color: #D100D1;">Plataformas:</strong> <span style="color: #00BFFF;">${juego.platforms}</span> <br>
                        <strong style="color: #D100D1;">Desarrolladores:</strong> <span style="color: #00BFFF;">${juego.developers}</span> <br>
                        <strong style="color: #D100D1;">Opinión:</strong> <span style="color: #00BFFF;">${juego.description}</span>
                    </p>
                    <hr style="border: 0; height: 1px; background: rgba(255,255,255,0.3); margin: 5px 0;">
                `;
                lista.appendChild(item);
            });

            resultadoDiv.appendChild(lista);
        }
    })
    .catch(error => {
        console.error("Error en la carga de recomendaciones:", error);
        document.getElementById("resultado-recomendaciones").innerHTML = "<p class='error-text'>❌ Error al conectar con el servidor.</p>";
    });
});
