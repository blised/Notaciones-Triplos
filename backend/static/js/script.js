function convertir() {
    let expresion = document.getElementById("expresion").value;
    
    fetch('/procesar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ expresion: expresion })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert("❌ Error: " + data.error);
        } else {
            document.getElementById("resultadoInfija").innerText = expresion;
            document.getElementById("resultadoPostfija").textContent = data.postfija;
            document.getElementById("resultadoPrefija").textContent = data.prefija;
            document.getElementById("resultadoFinal").textContent = data.resultado;
        }

        // Limpiar la tabla antes de agregar nuevos datos
        let triplosBody = document.getElementById("triplosBody");
        triplosBody.innerHTML = ""; 

        // Crear las filas dinámicamente según la cantidad de triplos
        data.triplos.forEach(triplo => {
            let row = triplosBody.insertRow();
            row.insertCell(0).textContent = `(${triplo[0]})`; // Índice
            row.insertCell(1).textContent = triplo[1];        // Operación
            row.insertCell(2).textContent = triplo[2];        // Arg1
            row.insertCell(3).textContent = triplo[3];        // Arg2
            row.insertCell(4).textContent = triplo[4];        // Resultado
        });


        // Hacer que la tabla sea visible si estaba oculta
        document.getElementById("triplosTable").style.display = "table";
    })
    .catch(error => console.error('Error:', error));
}