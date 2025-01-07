//Buscar por nombre
document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("buscar-btn").addEventListener("click", function () {
        let inputBusqueda = document.getElementById("busqueda-nombre").value.trim();

        if (inputBusqueda === "") {
            alert("Por favor, introduce un nombre para buscar.");
            return;
        }

        fetch(`/buscarPorNombre/?q=${encodeURIComponent(inputBusqueda)}`, {
            method: "GET",
            headers: {
                "X-Requested-With": "XMLHttpRequest"
            }
        })
        .then(response => response.json())
        .then(data => {
            let resultadoDiv = document.getElementById("resultado-busqueda");
            resultadoDiv.innerHTML = ""; // Limpiar resultados anteriores

            if (data.length === 0) {
                resultadoDiv.innerHTML = "<p style='color: red; text-align: center;'>No se encontraron resultados.</p>";
            } else {
                let lista = document.createElement("ul");
                lista.style.listStyle = "none";
                lista.style.padding = "0";

                data.forEach(juego => {
                    let item = document.createElement("li");
                    item.innerHTML = `
                        <p style="font-size: 14px; line-height: 1.3em;">
                            <strong style="color: #D100D1;">Nombre:</strong> <span style="color: #00BFFF;">${juego.title}</span> <br>
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
            console.error("Error en la búsqueda:", error);
            document.getElementById("resultado-busqueda").innerHTML = "<p style='color: red; text-align: center;'>Error al conectar con el servidor.</p>";
        });
    });
});
