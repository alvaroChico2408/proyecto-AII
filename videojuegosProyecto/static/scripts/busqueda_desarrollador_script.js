
document.addEventListener("DOMContentLoaded", function () {
    let desarrolladorSelect = document.getElementById("busqueda-desarrollador");
    let buscarBtn = document.getElementById("buscar-btn");
    let resultadoDiv = document.getElementById("resultado-busqueda");

    // Cargar lista de desarrolladores al cargar la página
    fetch("/obtener_desarrolladores/", { 
        method: "GET",
        headers: {
            "X-Requested-With": "XMLHttpRequest"
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.length === 0) {
            let option = document.createElement("option");
            option.value = "";
            option.text = "No hay desarrolladores registrados";
            desarrolladorSelect.appendChild(option);
        } else {
            data.forEach(desarrollador => {
                let option = document.createElement("option");
                option.value = desarrollador;
                option.text = desarrollador;
                desarrolladorSelect.appendChild(option);
            });
        }
    })
    .catch(error => console.error("Error al cargar los desarrolladores:", error));

    // Evento de búsqueda
    buscarBtn.addEventListener("click", function () {
        let desarrolladorSeleccionado = desarrolladorSelect.value;

        if (!desarrolladorSeleccionado) {
            alert("Por favor, selecciona un desarrollador para buscar.");
            return;
        }

        fetch(`/buscarPorDesarrollador/?q=${encodeURIComponent(desarrolladorSeleccionado)}`, {
            method: "GET",
            headers: {
                "X-Requested-With": "XMLHttpRequest"
            }
        })
        .then(response => response.json())
        .then(data => {
            resultadoDiv.innerHTML = ""; // Limpiar resultados anteriores

            if (data.length === 0) {
                resultadoDiv.innerHTML = "<p style='color: red; text-align: center; font-size: 14px;'>No se encontraron resultados.</p>";
            } else {
                let lista = document.createElement("ul");
                lista.style.listStyle = "none";
                lista.style.padding = "0";

                data.forEach(juego => {
                    let item = document.createElement("li");
                    item.innerHTML = `
                        <p style="font-size: 14px; line-height: 1.4em;">
                            <strong style="color: #D100D1;">Nombre:</strong> <span style="color: #00BFFF;">${juego.title}</span> <br>
                            <strong style="color: #D100D1;">Año:</strong> <span style="color: #00BFFF;">${juego.year}</span> <br>
                            <strong style="color: #D100D1;">Compañías:</strong> <span style="color: #00BFFF;">${juego.companies}</span> <br>
                            <strong style="color: #D100D1;">Plataformas:</strong> <span style="color: #00BFFF;">${juego.platforms}</span> <br>
                            <strong style="color: #D100D1;">Desarrolladores:</strong> <span style="color: #00BFFF;">${juego.developers}</span> <br>
                            <strong style="color: #D100D1;">Opinión:</strong> <span style="color: #00BFFF;">${juego.opinion}</span>
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
            resultadoDiv.innerHTML = "<p style='color: red; text-align: center; font-size: 14px;'>Error al conectar con el servidor.</p>";
        });
    });
});
