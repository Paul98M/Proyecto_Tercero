async function buscadorLibros(tableId) {
  const url = "/buscando-libro"; // Ruta Flask para buscar libros
  const input = document.getElementById("search");
  const busqueda = input.value.trim().toUpperCase();

  const dataPeticion = { busqueda };
  const headers = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
  };

  try {
    const response = await axios.post(url, dataPeticion, { headers });

    if (!response.status || response.data.fin === 0) {
      $(`#${tableId} tbody`).html(`
        <tr>
          <td colspan="8" style="text-align:center;color: red;font-weight: bold;">
            No hay resultados para: 
            <strong style="color: #222;">${busqueda}</strong>
          </td>
        </tr>`);
      return;
    }

    if (response.data) {
      $(`#${tableId} tbody`).html(response.data);
    }
  } catch (error) {
    console.error("Error al buscar libros:", error);
  }
}
