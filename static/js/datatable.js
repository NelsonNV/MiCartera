$(document).ready(function () {
  $('table').DataTable({
    responsive: {
      details: {
        renderer: function (api, rowIdx, columns) {
          // Personaliza cómo se muestran las columnas ocultas
          return columns
            .filter(col => col.hidden) // Filtra solo las columnas ocultas
            .map(col => `
              <tr>
                <td><strong>${col.title}</strong></td>
                <td>${col.data}</td>
              </tr>
            `)
            .join('');
        }
      }
    },
    columnDefs: [
      {
        targets: -1, // Última columna (Acciones)
        responsivePriority: 1, // Asegura que esta columna tenga la mayor prioridad
        className: 'text-center', // Centra el contenido
        orderable: false // Deshabilita el ordenamiento para esta columna
      }
    ],
    language: {
      url: "https://cdn.datatables.net/plug-ins/1.13.5/i18n/es-ES.json"
    }
  });
});
